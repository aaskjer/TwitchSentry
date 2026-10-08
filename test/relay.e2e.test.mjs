// The real Worker under `wrangler dev` with a local D1, against a fake GitHub and a fake Twitch.

import { test, before, after } from "node:test";
import assert from "node:assert/strict";
import http from "node:http";
import { spawn, execFileSync } from "node:child_process";
import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { randomUUID } from "node:crypto";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const T0 = 1790000000;
const DAY = 86400;

// ---- fake Twitch and GitHub ----

const twitch = { users: new Map(), tokenCalls: 0, lookups: [], failUsers: 0, bad: new Set() };
const github = { ref: null, trees: new Map(), commits: new Map(), failTrees: 0, n: 0, auth: [] };

function send(res, status, body) {
  res.writeHead(status, { "Content-Type": "application/json" });
  res.end(body === undefined ? "" : JSON.stringify(body));
}

async function bodyOf(req) {
  let text = "";
  for await (const chunk of req) text += chunk;
  return text ? JSON.parse(text) : null;
}

const fake = http.createServer(async (req, res) => {
  const url = new URL(req.url, "http://fake");
  const p = url.pathname;
  if (p === "/twitch/token" && req.method === "POST") {
    twitch.tokenCalls++;
    return send(res, 200, { access_token: "app-token", expires_in: 5000000, token_type: "bearer" });
  }
  if (p === "/twitch/helix/users") {
    if (req.headers.authorization !== "Bearer app-token" || req.headers["client-id"] !== "client-id") return send(res, 401, {});
    if (twitch.failUsers > 0) {
      twitch.failUsers--;
      return send(res, 503, { error: "Service Unavailable", status: 503, message: "try again" });
    }
    const ids = url.searchParams.getAll("id");
    const logins = url.searchParams.getAll("login");
    twitch.lookups.push({ ids, logins });
    if (ids.some(id => twitch.bad.has(id)))
      return send(res, 400, { error: "Bad Request", status: 400, message: "Invalid username(s), email(s), or ID(s). Bad Identifiers." });
    const data = [...twitch.users.values()].filter(u => ids.includes(u.id) || logins.includes(u.login));
    return send(res, 200, { data });
  }
  const repo = "/github/repos/aaskjer/TwitchSentry";
  if (p.startsWith(repo)) {
    github.auth.push(req.headers.authorization);
    const rest = p.slice(repo.length);
    const body = await bodyOf(req);
    if (rest === "/git/ref/heads/botlist" && req.method === "GET")
      return github.ref ? send(res, 200, { object: { sha: github.ref } }) : send(res, 404, { message: "Not Found" });
    if (rest === "/git/trees" && req.method === "POST") {
      if (github.failTrees > 0) {
        github.failTrees--;
        return send(res, 500, { message: "Server Error" });
      }
      const sha = "tree" + ++github.n;
      github.trees.set(sha, Object.fromEntries(body.tree.map(e => [e.path, e.content])));
      return send(res, 201, { sha });
    }
    if (rest === "/git/commits" && req.method === "POST") {
      const sha = "commit" + ++github.n;
      github.commits.set(sha, body);
      return send(res, 201, { sha });
    }
    if (rest === "/git/refs/heads/botlist" && req.method === "PATCH") {
      if (github.commits.get(body.sha).parents[0] !== github.ref) return send(res, 422, { message: "Update is not a fast forward" });
      github.ref = body.sha;
      return send(res, 200, { object: { sha: body.sha } });
    }
    if (rest === "/git/refs" && req.method === "POST") {
      if (github.ref) return send(res, 422, { message: "Reference already exists" });
      github.ref = body.sha;
      return send(res, 201, { object: { sha: body.sha } });
    }
  }
  send(res, 404, { message: "fake has no " + p });
});

function branch() {
  const files = github.trees.get(github.commits.get(github.ref).tree);
  const read = name => JSON.parse(files[name]);
  return {
    raw: files,
    index: read("index.json"), spam: read("spam.json"), lurkbots: read("lurkbots.json"), botwaves: read("botwaves.json"),
    changes: read("changes.json"), removed: read("removed.json"),
  };
}

function commitCount() {
  let n = 0;
  for (let sha = github.ref; sha; sha = github.commits.get(sha).parents[0]) n++;
  return n;
}

// ---- the Worker ----

let child;
let base;
let persist;
let log = "";

function freePort() {
  return new Promise(resolve => {
    const s = http.createServer().listen(0, "127.0.0.1", () => {
      const { port } = s.address();
      s.close(() => resolve(port));
    });
  });
}

before(async () => {
  await new Promise(resolve => fake.listen(0, "127.0.0.1", resolve));
  const f = `http://127.0.0.1:${fake.address().port}`;
  const port = await freePort();
  persist = mkdtempSync(path.join(tmpdir(), "ts-relay-"));
  const vars = {
    TEST_MODE: "1", GITHUB_API: f + "/github", TWITCH_API: f + "/twitch/helix", TWITCH_AUTH: f + "/twitch/token",
    GITHUB_TOKEN: "gh-token", TWITCH_CLIENT_ID: "client-id", TWITCH_CLIENT_SECRET: "client-secret",
    REMOVAL_KEY: "removal-key", HASH_SALT: "salt",
  };
  const args = [path.join(root, "node_modules", "wrangler", "bin", "wrangler.js"), "dev", "--local", "--ip", "127.0.0.1",
    "--port", String(port), "--persist-to", persist, "--show-interactive-dev-session=false", "--log-level", "warn"];
  for (const [k, v] of Object.entries(vars)) args.push("--var", `${k}:${v}`);
  child = spawn(process.execPath, args, { cwd: root, env: { ...process.env, WRANGLER_SEND_METRICS: "false", CI: "1" } });
  child.stdout.on("data", d => { log += d; });
  child.stderr.on("data", d => { log += d; });
  base = `http://127.0.0.1:${port}`;
  const deadline = Date.now() + 90000;
  while (Date.now() < deadline) {
    try {
      const r = await fetch(base + "/v1/health");
      if (r.status === 200) return;
    } catch { /* not up yet */ }
    await new Promise(r => setTimeout(r, 500));
  }
  throw new Error("wrangler dev did not come up:\n" + log);
});

after(() => {
  if (child && child.exitCode === null) {
    if (process.platform === "win32") {
      try { execFileSync("taskkill", ["/pid", String(child.pid), "/T", "/F"], { stdio: "ignore" }); } catch { /* already gone */ }
    } else child.kill("SIGTERM");
  }
  fake.close();
  try { rmSync(persist, { recursive: true, force: true }); } catch { /* workerd may still hold it on Windows */ }
});

async function call(method, route, body, { ip = "198.51.100.7", now = T0, headers = {} } = {}) {
  const h = { "X-Test-IP": ip, "X-Test-Now": String(now), ...headers };
  if (body !== undefined && !("Content-Type" in h)) h["Content-Type"] = "application/json";
  const res = await fetch(base + route, { method, headers: h, body: body === undefined ? undefined : typeof body === "string" ? body : JSON.stringify(body) });
  const text = await res.text();
  let json = null;
  try { json = JSON.parse(text); } catch { /* not JSON */ }
  return { status: res.status, body: json, text, headers: res.headers };
}

const install = { A: randomUUID(), B: randomUUID(), C: randomUUID(), D: randomUUID(), E: randomUUID(), F: randomUUID() };
const report = (who, items, opts) => call("POST", "/v1/report", { install: install[who], version: "v3.2.0", reports: items }, opts);
const retract = (who, items, opts) => call("POST", "/v1/retract", { install: install[who], version: "v3.2.0", retract: items }, opts);
const publish = (now, force = false) => call("POST", "/__test/publish", { force }, { now });
const removal = (body, key = "removal-key", now) => call("POST", "/v1/remove", body, { headers: { Authorization: "Bearer " + key }, now });
const user = (id, login, extra = {}) => twitch.users.set(id, { id, login, display_name: login, type: "", broadcaster_type: "", ...extra });

// ---- the story ----

test("an empty relay creates the branch on its first pass", async () => {
  const h = await call("GET", "/v1/health");
  assert.equal(h.status, 200);
  assert.deepEqual(h.body.configured, { github: true, twitch: true, salt: true, removals: true });
  assert.equal(h.body.version, 0);

  const p = await publish(T0);
  assert.equal(p.body.ok, true, p.text);
  assert.equal(p.body.committed, true);
  assert.equal(github.commits.get(github.ref).parents.length, 0);
  const b = branch();
  assert.equal(b.index.version, 0);
  assert.deepEqual(b.spam.accounts, []);
  assert.match(b.raw["README.md"], /TwitchSentry Bot List/);
  assert.ok(github.auth.every(a => a === "Bearer gh-token"));

  const again = await publish(T0 + 120);
  assert.equal(again.body.changed, false);
  assert.equal(commitCount(), 1);
});

test("one report lists an account once Twitch knows it", async () => {
  user("1001", "spambot_one");
  const r = await report("A", [{ category: "spam", id: "1001", login: "SpamBot_One", reason: "spam_domain" }], { now: T0 + 150 });
  assert.equal(r.status, 200, r.text);
  assert.equal(r.body.accepted, 1);
  assert.equal((await call("GET", "/v1/health")).body.pendingChecks, 1);

  const p = await publish(T0 + 200);
  assert.equal(p.body.committed, true, p.text);
  assert.equal(p.body.version, 1);
  const b = branch();
  assert.deepEqual(b.spam.accounts, [{ id: "1001", login: "spambot_one", reports: 1, first: "2026-09-21", last: "2026-09-21", reasons: ["spam_domain"] }]);
  assert.equal(b.raw["spam.txt"], "");
  assert.deepEqual(b.changes.changes.map(c => [c.v, c.op, c.id, c.reports]), [[1, "add", "1001", 1]]);
  assert.equal(github.commits.get(github.ref).message, "Bot list v1: +1 spam");
});

test("the same install, or another one in the same network, never counts twice", async () => {
  const before = commitCount();
  const lookups = twitch.lookups.length;
  assert.equal((await report("A", [{ category: "spam", id: "1001", login: "spambot_one", reason: "keyword" }], { ip: "203.0.113.9", now: T0 + 300 })).body.accepted, 1);
  assert.equal((await report("B", [{ category: "spam", id: "1001", login: "spambot_one", reason: "keyword" }], { ip: "198.51.100.77", now: T0 + 300 })).body.accepted, 1);
  const p = await publish(T0 + 400);
  assert.equal(p.body.changed, false, p.text);
  assert.equal(commitCount(), before);
  assert.equal(branch().spam.accounts[0].reports, 1);
  assert.equal(twitch.lookups.length, lookups, "a checked account is not looked up again for a new report");
});

test("a second network confirms it and the txt list takes it", async () => {
  await report("C", [{ category: "spam", id: "1001", login: "spambot_one", reason: "keyword" }], { ip: "192.0.2.10", now: T0 + 500 });
  const p = await publish(T0 + 600);
  assert.equal(p.body.version, 2, p.text);
  const b = branch();
  assert.equal(b.spam.accounts[0].reports, 2);
  assert.deepEqual(b.spam.accounts[0].reasons, ["keyword"], "an install's later report replaces its reason");
  assert.equal(b.raw["spam.txt"], "spambot_one\n");
  assert.deepEqual(b.index.lists.spam, { file: "spam.json", text: "spam.txt", count: 1, confirmed: 1 });
  assert.deepEqual(b.changes.changes.at(-1), { v: 2, at: "2026-09-21T14:23:20Z", op: "update", category: "spam", id: "1001", login: "spambot_one", reports: 2 });
});

test("partners, affiliates and service bots never get on", async () => {
  user("1002", "some_affiliate", { broadcaster_type: "affiliate" });
  const r = await report("A", [
    { category: "spam", id: "1002", login: "some_affiliate", reason: "keyword" },
    { category: "spam", id: "1009", login: "Nightbot", reason: "keyword" },
  ], { now: T0 + 700 });
  assert.equal(r.body.accepted, 1);
  assert.deepEqual(r.body.ignored, [{ i: 1, why: "service_bot" }]);
  const p = await publish(T0 + 800);
  assert.equal(p.body.changed, false, p.text);
  assert.ok(!branch().spam.accounts.some(a => a.id === "1002"));
  const again = await report("C", [{ category: "spam", id: "1002", login: "some_affiliate", reason: "keyword" }], { ip: "192.0.2.10", now: T0 + 900 });
  assert.deepEqual(again.body.ignored, [{ i: 0, why: "protected" }]);
});

test("bad requests are refused", async () => {
  assert.equal((await call("POST", "/v1/report", "{}", { headers: { "Content-Type": "text/plain" } })).status, 415);
  assert.equal((await call("POST", "/v1/report", "{nope")).status, 400);
  const badInstall = await call("POST", "/v1/report", { install: "x", version: "v3.2.0", reports: [{}] });
  assert.equal(badInstall.status, 400);
  assert.match(badInstall.body.error, /UUID/);
  const many = Array.from({ length: 51 }, (_, i) => ({ category: "spam", id: String(5000 + i), login: "a", reason: "keyword" }));
  assert.equal((await report("A", many)).status, 400);
  assert.equal((await call("GET", "/v1/report")).status, 405);
  assert.equal((await call("GET", "/nope")).status, 404);
  assert.equal((await call("POST", "/v1/remove", { names: ["x"] })).status, 401);
  assert.equal((await removal({ names: ["x"] }, "wrong-key")).status, 401);
  const big = await call("POST", "/v1/report", JSON.stringify({ pad: "x".repeat(70000) }));
  assert.equal(big.status, 413);
});

test("the three lists are kept apart", async () => {
  user("1003", "lurk_bot77");
  await report("A", [{ category: "lurkbot", id: "1003", login: "lurk_bot77", reason: "known_day" }], { now: T0 + 1000 });
  await report("C", [{ category: "botwave", id: "1003", login: "lurk_bot77", reason: "follow_wave" }], { ip: "192.0.2.10", now: T0 + 1000 });
  const p = await publish(T0 + 1100);
  assert.equal(p.body.committed, true, p.text);
  const b = branch();
  assert.deepEqual(b.lurkbots.accounts.map(a => [a.id, a.reports, a.reasons]), [["1003", 1, ["known_day"]]]);
  assert.deepEqual(b.botwaves.accounts.map(a => [a.id, a.reports, a.reasons]), [["1003", 1, ["follow_wave"]]]);
  assert.equal(b.spam.accounts.length, 1);
  assert.equal(github.commits.get(github.ref).message, "Bot list v3: +1 lurkbot, +1 botwave");
});

test("a retraction takes one report back", async () => {
  const r = await retract("C", [{ id: "1001", category: "spam" }], { ip: "192.0.2.10", now: T0 + 1200 });
  assert.equal(r.body.retracted, 1, r.text);
  await publish(T0 + 1300);
  const b = branch();
  assert.equal(b.spam.accounts[0].reports, 1);
  assert.equal(b.raw["spam.txt"], "");
  assert.equal(b.botwaves.accounts.length, 1, "the retraction named spam only");
});

test("a removal takes an account off at once and keeps its reporters out", async () => {
  const r = await removal({ names: ["@SpamBot_One", "never_seen"], issue: 77, by: "aaskjer" }, "removal-key", T0 + 1400);
  assert.equal(r.status, 200, r.text);
  assert.deepEqual(r.body.removed, [{ id: "1001", login: "spambot_one" }]);
  assert.deepEqual(r.body.unlisted, ["never_seen"]);
  assert.equal(r.body.committed, true);
  const b = branch();
  assert.deepEqual(b.spam.accounts, []);
  assert.deepEqual(b.changes.changes.at(-1), { v: 5, at: "2026-09-21T14:36:40Z", op: "remove", category: "spam", id: "1001", why: "removed" });
  assert.deepEqual(b.removed.removed, [{ id: "1001", at: "2026-09-21" }]);

  for (const who of ["A", "B"]) {
    const again = await report(who, [{ category: "spam", id: "1001", login: "spambot_one", reason: "keyword" }], { now: T0 + 1500 });
    assert.deepEqual(again.body.ignored, [{ i: 0, why: "removed" }], who);
  }
});

test("a removed account needs three fresh networks to come back", async () => {
  const item = [{ category: "spam", id: "1001", login: "spambot_one", reason: "spam_domain" }];
  await report("D", item, { ip: "100.64.1.1", now: T0 + 1600 });
  await report("E", item, { ip: "100.64.2.1", now: T0 + 1600 });
  await publish(T0 + 1700);
  assert.deepEqual(branch().spam.accounts, []);
  await report("F", item, { ip: "100.64.3.1", now: T0 + 1800 });
  await publish(T0 + 1900);
  assert.deepEqual(branch().spam.accounts.map(a => [a.id, a.reports]), [["1001", 3]]);
  assert.equal(branch().changes.changes.at(-1).op, "add");
});

test("a rename is followed and a deleted account leaves", async () => {
  user("1003", "renamed_bot");
  await publish(T0 + 8 * DAY);
  let b = branch();
  assert.equal(b.lurkbots.accounts[0].login, "renamed_bot");
  assert.equal(b.botwaves.accounts[0].login, "renamed_bot");
  assert.deepEqual(b.changes.changes.filter(c => c.op === "update" && c.id === "1003").map(c => [c.category, c.login]),
    [["botwave", "renamed_bot"], ["lurkbot", "renamed_bot"]]);

  twitch.users.delete("1003");
  await publish(T0 + 16 * DAY);
  b = branch();
  assert.deepEqual(b.lurkbots.accounts, []);
  assert.deepEqual(b.botwaves.accounts, []);
  assert.deepEqual(b.changes.changes.filter(c => c.op === "remove" && c.id === "1003").map(c => c.why), ["gone", "gone"]);

  user("1003", "renamed_bot");
  await report("A", [{ category: "lurkbot", id: "1003", login: "renamed_bot", reason: "known_day" }], { now: T0 + 16 * DAY + 50 });
  await publish(T0 + 16 * DAY + 60);
  b = branch();
  assert.deepEqual(b.lurkbots.accounts.map(a => a.login), ["renamed_bot"], "a report has a gone account checked again");
  assert.deepEqual(b.botwaves.accounts.map(a => a.login), ["renamed_bot"]);
});

test("a removal finds a renamed account through Twitch", async () => {
  user("1004", "old_name");
  await report("A", [{ category: "spam", id: "1004", login: "old_name", reason: "keyword" }], { now: T0 + 16 * DAY + 100 });
  await publish(T0 + 16 * DAY + 200);
  assert.ok(branch().spam.accounts.some(a => a.id === "1004"));
  user("1004", "new_name");
  const r = await removal({ names: ["new_name"] }, "removal-key", T0 + 16 * DAY + 300);
  assert.deepEqual(r.body.removed, [{ id: "1004", login: "old_name" }], r.text);
  assert.deepEqual(r.body.unlisted, []);
  assert.ok(!branch().spam.accounts.some(a => a.id === "1004"));
});

test("a failed Twitch check shows in health and the account waits for the next pass", async () => {
  user("1006", "bot_six");
  await report("A", [{ category: "spam", id: "1006", login: "bot_six", reason: "keyword" }], { now: T0 + 16 * DAY + 330 });
  twitch.failUsers = 1;
  await publish(T0 + 16 * DAY + 340);
  let h = await call("GET", "/v1/health");
  assert.equal(h.body.ok, false);
  assert.match(h.body.twitchError, /Twitch Get Users answered 503: .*try again/);
  assert.equal(h.body.pendingChecks, 1);
  assert.ok(!branch().spam.accounts.some(a => a.id === "1006"));
  await publish(T0 + 16 * DAY + 350);
  h = await call("GET", "/v1/health");
  assert.equal(h.body.twitchError, null);
  assert.equal(h.body.pendingChecks, 0);
  assert.ok(branch().spam.accounts.some(a => a.id === "1006"));
});

test("an id Twitch calls bad is set aside instead of blocking every other check", async () => {
  user("1007", "bot_seven");
  twitch.bad.add("99999999999");
  const before = twitch.lookups.length;
  const r = await report("A", [
    { category: "spam", id: "99999999999", login: "no_such_account", reason: "keyword" },
    { category: "spam", id: "1007", login: "bot_seven", reason: "keyword" },
  ], { now: T0 + 16 * DAY + 360 });
  assert.equal(r.body.accepted, 2);
  await publish(T0 + 16 * DAY + 370);
  const h = await call("GET", "/v1/health");
  assert.equal(h.body.twitchError, null);
  assert.equal(h.body.pendingChecks, 0);
  assert.equal(twitch.lookups.length - before, 3, "one refused lookup, then each id alone");
  const accounts = branch().spam.accounts.map(a => a.id);
  assert.ok(accounts.includes("1007"));
  assert.ok(!accounts.includes("99999999999"));
  const again = await report("C", [{ category: "spam", id: "99999999999", login: "no_such_account", reason: "keyword" }], { ip: "192.0.2.10", now: T0 + 16 * DAY + 380 });
  assert.deepEqual(again.body.ignored, [{ i: 0, why: "invalid" }]);
});

test("a refused commit is kept and retried on the next pass", async () => {
  user("1005", "bot_five");
  await report("A", [{ category: "spam", id: "1005", login: "bot_five", reason: "keyword" }], { now: T0 + 16 * DAY + 400 });
  github.failTrees = 1;
  const p = await publish(T0 + 16 * DAY + 500);
  assert.equal(p.body.committed, false);
  assert.match(p.body.error, /GitHub refused the tree \(500\)/);
  let h = await call("GET", "/v1/health");
  assert.equal(h.body.waitingToCommit, true);
  assert.equal(h.body.ok, false);
  const retry = await publish(T0 + 16 * DAY + 620);
  assert.equal(retry.body.committed, true, retry.text);
  assert.ok(branch().spam.accounts.some(a => a.id === "1005"));
  h = await call("GET", "/v1/health");
  assert.equal(h.body.waitingToCommit, false);
  assert.equal(h.body.ok, true);
});

test("one network is held to its hourly limit", async () => {
  const at = T0 + 20 * DAY;
  for (let i = 0; i < 120; i++) {
    const r = await call("POST", "/v1/retract", "{nope", { ip: "10.20.30.40", now: at });
    assert.equal(r.status, 400, `request ${i + 1}`);
  }
  const over = await call("POST", "/v1/retract", "{nope", { ip: "10.20.30.99", now: at });
  assert.equal(over.status, 429);
  assert.equal(over.headers.get("Retry-After"), String(3600 - (at % 3600)));
  const elsewhere = await call("POST", "/v1/retract", "{nope", { ip: "10.20.31.1", now: at });
  assert.equal(elsewhere.status, 400);
  const nextHour = await call("POST", "/v1/retract", "{nope", { ip: "10.20.30.40", now: at + 3600 });
  assert.equal(nextHour.status, 400);
});

test("reports expire after a year and the change log keeps a week", async () => {
  await publish(T0 + 400 * DAY);
  const b = branch();
  assert.deepEqual(b.spam.accounts, []);
  assert.ok(b.changes.since > 0);
  assert.equal(b.index.changes.since, b.changes.since);
  assert.ok(b.changes.changes.every(c => c.v > b.changes.since));
  assert.ok(b.changes.changes.length > 0 && b.changes.changes.every(c => c.op === "remove" && c.why === "dropped"));
  assert.deepEqual(b.removed.removed, []);
  assert.equal(twitch.tokenCalls, 1, "the app token is cached");
});
