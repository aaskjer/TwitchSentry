// TwitchSentry bot list relay: installs report here, the cron writes the public `botlist` branch.

import { LIMITS, parseReport, parseRetract, parseRemoval, networkOf, hashKey, constantTimeEqual } from "./rules.js";
import * as store from "./store.js";
import { publish, getUsers, twitchConfigured } from "./publish.js";

const HEADERS = { "Content-Type": "application/json; charset=utf-8", "Cache-Control": "no-store" };

function reply(status, body, extra = {}) {
  return new Response(JSON.stringify(body), { status, headers: { ...HEADERS, ...extra } });
}

function refuse(status, error, extra) {
  return reply(status, { ok: false, error }, extra);
}

// Tests set the clock and the address with headers; only with TEST_MODE, which production never has.
function clock(env, request) {
  if (env.TEST_MODE === "1" && request) {
    const t = request.headers.get("X-Test-Now");
    if (t && /^\d+$/.test(t)) return Number(t);
  }
  return Math.floor(Date.now() / 1000);
}

async function readJson(request) {
  const type = (request.headers.get("Content-Type") || "").toLowerCase();
  if (!type.startsWith("application/json")) return { status: 415, error: "send application/json" };
  if (Number(request.headers.get("Content-Length") || 0) > LIMITS.maxBody) return { status: 413, error: "body too large" };
  const text = await request.text();
  if (text.length > LIMITS.maxBody) return { status: 413, error: "body too large" };
  try {
    return { body: JSON.parse(text) };
  } catch {
    return { status: 400, error: "body is not JSON" };
  }
}

function untilNextHour(now) {
  return { "Retry-After": String(3600 - (now % 3600)) };
}

// Who is asking, as salted hashes: the network for independence and limits, never the address itself.
async function sender(env, request, now) {
  if (!env.HASH_SALT) return { response: refuse(503, "the relay is not configured yet") };
  const ip = (env.TEST_MODE === "1" && request.headers.get("X-Test-IP")) || request.headers.get("CF-Connecting-IP");
  const net = networkOf(ip);
  if (!net) return { response: refuse(400, "no client address") };
  const netKey = await hashKey(env.HASH_SALT, "net", net);
  if (await store.spend(env.DB, "req:" + netKey, now, 1) > LIMITS.netRequestsPerHour)
    return { response: refuse(429, "too many requests from this network", untilNextHour(now)) };
  return { netKey };
}

async function spendItems(env, netKey, installKey, now, n) {
  const byNet = await store.spend(env.DB, "items:" + netKey, now, n);
  const byInstall = await store.spend(env.DB, "inst:" + installKey, now, n);
  return byNet <= LIMITS.netItemsPerHour && byInstall <= LIMITS.installItemsPerHour;
}

async function report(env, request) {
  const now = clock(env, request);
  const who = await sender(env, request, now);
  if (who.response) return who.response;
  const read = await readJson(request);
  if (read.error) return refuse(read.status, read.error);
  const parsed = parseReport(read.body);
  if (parsed.error) return refuse(400, parsed.error);

  const installKey = await hashKey(env.HASH_SALT, "install", parsed.install);
  if (!await spendItems(env, who.netKey, installKey, now, parsed.items.length))
    return refuse(429, "too many reports this hour", untilNextHour(now));
  const result = parsed.items.length
    ? await store.recordReports(env.DB, { install: installKey, net: who.netKey, now, items: parsed.items })
    : { accepted: 0, ignored: [] };
  const ignored = [...parsed.ignored, ...result.ignored].sort((a, b) => a.i - b.i);
  return reply(200, { ok: true, accepted: result.accepted, ignored });
}

async function retract(env, request) {
  const now = clock(env, request);
  const who = await sender(env, request, now);
  if (who.response) return who.response;
  const read = await readJson(request);
  if (read.error) return refuse(read.status, read.error);
  const parsed = parseRetract(read.body);
  if (parsed.error) return refuse(400, parsed.error);

  const installKey = await hashKey(env.HASH_SALT, "install", parsed.install);
  if (!await spendItems(env, who.netKey, installKey, now, parsed.items.length))
    return refuse(429, "too many requests this hour", untilNextHour(now));
  const retracted = parsed.items.length ? await store.retractReports(env.DB, { install: installKey, items: parsed.items }) : 0;
  return reply(200, { ok: true, retracted, ignored: parsed.ignored });
}

// Called by the removal workflow only; a removal is written to the branch before this answers.
async function remove(env, request) {
  if (!env.REMOVAL_KEY) return refuse(503, "removals are not configured yet");
  const auth = request.headers.get("Authorization") || "";
  if (!constantTimeEqual(auth, "Bearer " + env.REMOVAL_KEY)) return refuse(401, "not allowed");
  const now = clock(env, request);
  const read = await readJson(request);
  if (read.error) return refuse(read.status, read.error);
  const parsed = parseRemoval(read.body);
  if (parsed.error) return refuse(400, parsed.error);

  const db = env.DB;
  const found = new Map((await store.findAccounts(db, parsed.ids, parsed.logins)).map(a => [a.id, a]));
  const knownLogins = new Set([...found.values()].map(a => a.login));
  const renamed = new Map();
  const unknown = parsed.logins.filter(l => !knownLogins.has(l));
  if (unknown.length && twitchConfigured(env)) {
    try {
      const users = await getUsers(env, db, { logins: unknown });
      for (const u of users.values()) renamed.set(u.login, u.id);
      for (const a of await store.findAccounts(db, [...renamed.values()], [])) found.set(a.id, a);
    } catch (err) {
      console.warn("removal: Twitch lookup failed", String(err.message || err));
    }
  }

  const accounts = [...found.values()];
  const listed = await store.listedIds(db, accounts.map(a => a.id));
  if (accounts.length) await store.removeAccounts(db, accounts, { now, issue: parsed.issue, by: parsed.by });

  const matched = new Set();
  for (const a of accounts) {
    matched.add(a.id);
    matched.add(a.login);
  }
  for (const [login, id] of renamed) if (found.has(id)) matched.add(login);
  const unlisted = [...new Set([...parsed.ids, ...parsed.logins])].filter(n => !matched.has(n));

  const result = accounts.length ? await publish(env, { now, waitForLock: 5 }) : { ok: true, committed: false };
  return reply(200, {
    ok: true,
    removed: accounts.filter(a => listed.has(a.id)).map(a => ({ id: a.id, login: a.login })),
    cleared: accounts.filter(a => !listed.has(a.id)).map(a => ({ id: a.id, login: a.login })),
    unlisted,
    unreadable: parsed.unreadable,
    version: result.version ?? null,
    committed: Boolean(result.committed),
    commit: result.commit ?? null,
    error: result.error ?? result.skipped ?? null,
  });
}

async function health(env) {
  const meta = await store.readMeta(env.DB);
  const { lists, pending } = await store.counts(env.DB, LIMITS.banFrom);
  return reply(200, {
    ok: !meta.error && !meta.twitch_error,
    version: meta.version,
    commit: meta.commit || null,
    committedAt: meta.commit_at ? new Date(meta.commit_at * 1000).toISOString() : null,
    waitingToCommit: meta.pending_commit === 1,
    error: meta.error || null,
    twitchError: meta.twitch_error || null,
    lists,
    pendingChecks: pending,
    configured: {
      github: Boolean(env.GITHUB_TOKEN && env.GITHUB_REPO && env.GITHUB_BRANCH),
      twitch: twitchConfigured(env),
      salt: Boolean(env.HASH_SALT),
      removals: Boolean(env.REMOVAL_KEY),
    },
  });
}

function home(env) {
  const branch = `https://github.com/${env.GITHUB_REPO}/tree/${env.GITHUB_BRANCH}`;
  return new Response(`TwitchSentry bot list relay.\nThe list itself: ${branch}\n`, {
    headers: { "Content-Type": "text/plain; charset=utf-8" },
  });
}

export default {
  async fetch(request, env) {
    try {
      await store.ensureSchema(env.DB);
      const { pathname } = new URL(request.url);
      const route = `${request.method} ${pathname}`;
      switch (route) {
        case "GET /": return home(env);
        case "GET /v1/health": return await health(env);
        case "POST /v1/report": return await report(env, request);
        case "POST /v1/retract": return await retract(env, request);
        case "POST /v1/remove": return await remove(env, request);
      }
      if (env.TEST_MODE === "1" && route === "POST /__test/publish") {
        const read = await readJson(request);
        return reply(200, await publish(env, { now: clock(env, request), force: Boolean(read.body && read.body.force) }));
      }
      return refuse(pathname.startsWith("/v1/") || pathname === "/" ? 405 : 404, "no such endpoint");
    } catch (err) {
      console.error("relay failed", err && err.stack ? err.stack : String(err));
      return refuse(500, "the relay failed; try again later");
    }
  },

  async scheduled(controller, env, ctx) {
    ctx.waitUntil(publish(env).then(
      r => console.log("publish", JSON.stringify(r)),
      err => console.error("publish failed", err && err.stack ? err.stack : String(err)),
    ));
  },
};
