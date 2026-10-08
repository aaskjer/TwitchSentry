// Pure rules of the bot list relay: no I/O, so the tests run them directly.

export const SCHEMA = 1;
export const CATEGORIES = ["spam", "lurkbot", "botwave"];
export const FILE_OF = { spam: "spam", lurkbot: "lurkbots", botwave: "botwaves" };

export const LIMITS = {
  maxBody: 64 * 1024,
  maxItems: 50,
  maxNames: 50,
  netRequestsPerHour: 120,
  netItemsPerHour: 3000,
  installItemsPerHour: 2000,
  publishFrom: 1,
  banFrom: 2,
  // A removal is a mistake undone: the installs that reported it are ignored for that account from then on,
  // and it needs this many fresh, independent reporters to return.
  afterRemoval: 3,
  keepDays: 365,
  changesDays: 7,
  recheckDays: 7,
  lockSeconds: 110,
};

export const REASONS = new Set([
  "spam_domain", "keyword", "handoff", "service_offer", "custom_pattern", "conversation_scam",
  "search_redirect", "offer_quantity", "offer_repeated", "offer_catalogue", "campaign_tag",
  "assembly_instruction", "redemption_code", "voucher_code", "voucher_pattern",
  "lurkbot_name", "known_day", "same_day", "bare_profile",
  "follow_wave", "raid_swarm", "raid_content",
]);

// Accounts channels rely on; a misreport must never put one of them on everybody's ban list.
export const SERVICE_BOTS = new Set([
  "nightbot", "streamelements", "moobot", "fossabot", "wizebot", "streamlabs", "sery_bot", "soundalerts",
  "pretzelrocks", "kofistreambot", "blerp", "botrixoficial", "own3d", "tangiabot", "frostytoolsdotcom",
  "streamstickers", "stay_hydrated_bot", "lumiastream", "mixitupbot", "creatisbot", "streamerbot",
  "songlistbot", "deepbot", "phantombot", "coebot", "vivbot", "botisimo", "stream_elements",
]);

const INSTALL_RE = /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/;
const VERSION_RE = /^v\d{1,3}\.\d{1,3}\.\d{1,3}(-[a-z]{1,10}\.\d{1,3})?$/;
const ID_RE = /^[1-9][0-9]{0,19}$/;
const LOGIN_RE = /^[a-z0-9_]{1,25}$/;
const REASON_RE = /^[a-z][a-z0-9_]{1,31}$/;
const GITHUB_LOGIN_RE = /^[A-Za-z0-9](?:[A-Za-z0-9-]{0,38})$/;

export function normaliseLogin(value) {
  if (typeof value !== "string") return null;
  const login = value.trim().replace(/^@/, "").toLowerCase();
  return LOGIN_RE.test(login) ? login : null;
}

function isObject(value) {
  return value !== null && typeof value === "object" && !Array.isArray(value);
}

function headerOf(body) {
  if (!isObject(body)) return { error: "body is not a JSON object" };
  const install = typeof body.install === "string" ? body.install.toLowerCase() : "";
  if (!INSTALL_RE.test(install)) return { error: "install is not a version 4 UUID" };
  const version = typeof body.version === "string" ? body.version : "";
  if (!VERSION_RE.test(version)) return { error: "version is not a TwitchSentry release tag" };
  return { install, version };
}

export function parseReport(body) {
  const head = headerOf(body);
  if (head.error) return { error: head.error };
  if (!Array.isArray(body.reports) || body.reports.length === 0) return { error: "reports is empty" };
  if (body.reports.length > LIMITS.maxItems) return { error: `more than ${LIMITS.maxItems} reports` };

  const items = [];
  const ignored = [];
  const seen = new Set();
  body.reports.forEach((r, i) => {
    if (!isObject(r)) return ignored.push({ i, why: "not_an_object" });
    if (!CATEGORIES.includes(r.category)) return ignored.push({ i, why: "category" });
    const id = typeof r.id === "string" ? r.id.trim() : "";
    if (!ID_RE.test(id)) return ignored.push({ i, why: "id" });
    const login = normaliseLogin(r.login);
    if (!login) return ignored.push({ i, why: "login" });
    if (SERVICE_BOTS.has(login)) return ignored.push({ i, why: "service_bot" });
    const raw = typeof r.reason === "string" ? r.reason : "";
    if (!REASON_RE.test(raw)) return ignored.push({ i, why: "reason" });
    const key = r.category + ":" + id;
    if (seen.has(key)) return ignored.push({ i, why: "duplicate" });
    seen.add(key);
    items.push({ i, category: r.category, id, login, reason: REASONS.has(raw) ? raw : "other" });
  });
  return { install: head.install, version: head.version, items, ignored };
}

export function parseRetract(body) {
  const head = headerOf(body);
  if (head.error) return { error: head.error };
  if (!Array.isArray(body.retract) || body.retract.length === 0) return { error: "retract is empty" };
  if (body.retract.length > LIMITS.maxItems) return { error: `more than ${LIMITS.maxItems} retractions` };

  const items = [];
  const ignored = [];
  body.retract.forEach((r, i) => {
    if (!isObject(r)) return ignored.push({ i, why: "not_an_object" });
    const id = typeof r.id === "string" ? r.id.trim() : "";
    if (!ID_RE.test(id)) return ignored.push({ i, why: "id" });
    if (r.category !== undefined && !CATEGORIES.includes(r.category)) return ignored.push({ i, why: "category" });
    items.push({ i, id, category: r.category ?? null });
  });
  return { install: head.install, version: head.version, items, ignored };
}

// A name may be a login (with or without @) or a numeric id; all-digit logins exist, so digits are tried as both.
export function parseRemoval(body) {
  if (!isObject(body)) return { error: "body is not a JSON object" };
  if (!Array.isArray(body.names) || body.names.length === 0) return { error: "names is empty" };
  if (body.names.length > LIMITS.maxNames) return { error: `more than ${LIMITS.maxNames} names` };
  const ids = new Set();
  const logins = new Set();
  const unreadable = [];
  for (const raw of body.names) {
    const text = typeof raw === "string" ? raw.trim() : "";
    if (ID_RE.test(text)) ids.add(text);
    const login = normaliseLogin(text);
    if (login) logins.add(login);
    else if (!ID_RE.test(text)) unreadable.push(String(raw).slice(0, 40));
  }
  const issue = Number.isInteger(body.issue) && body.issue > 0 ? body.issue : null;
  const by = typeof body.by === "string" && GITHUB_LOGIN_RE.test(body.by) ? body.by : null;
  return { ids: [...ids], logins: [...logins], unreadable, issue, by };
}

function expandIPv6(ip) {
  const zone = ip.indexOf("%");
  if (zone >= 0) ip = ip.slice(0, zone);
  let tail = [];
  const v4 = ip.match(/(\d+)\.(\d+)\.(\d+)\.(\d+)$/);
  if (v4) {
    const n = v4.slice(1).map(Number);
    tail = [((n[0] << 8) | n[1]).toString(16), ((n[2] << 8) | n[3]).toString(16)];
    ip = ip.slice(0, ip.length - v4[0].length) + "0:0";
  }
  const halves = ip.split("::");
  if (halves.length > 2) return null;
  const left = halves[0] ? halves[0].split(":") : [];
  const right = halves.length === 2 && halves[1] ? halves[1].split(":") : [];
  const missing = 8 - left.length - right.length;
  if (halves.length === 1 ? missing !== 0 : missing < 0) return null;
  const groups = [...left, ...Array(halves.length === 2 ? missing : 0).fill("0"), ...right];
  if (groups.length !== 8 || groups.some(g => !/^[0-9a-f]{1,4}$/i.test(g))) return null;
  if (tail.length) groups.splice(6, 2, ...tail);
  return groups.map(g => parseInt(g, 16).toString(16));
}

// Reporters count as independent per network, not per address: an IPv4 /24 or an IPv6 /48.
export function networkOf(ip) {
  if (typeof ip !== "string" || ip.length === 0) return null;
  const v4 = ip.match(/^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$/);
  if (v4) {
    const n = v4.slice(1).map(Number);
    if (n.some(x => x > 255)) return null;
    return `v4:${n[0]}.${n[1]}.${n[2]}`;
  }
  const groups = expandIPv6(ip);
  if (!groups) return null;
  if (groups.slice(0, 5).every(g => g === "0") && groups[5] === "ffff") {
    const a = parseInt(groups[6], 16), b = parseInt(groups[7], 16);
    return `v4:${a >> 8}.${a & 255}.${b >> 8}`;
  }
  return "v6:" + groups.slice(0, 3).join(":");
}

export async function hashKey(salt, kind, value) {
  const data = new TextEncoder().encode(`${salt}\u0000${kind}\u0000${value}`);
  const digest = await crypto.subtle.digest("SHA-256", data);
  return [...new Uint8Array(digest)].slice(0, 16).map(b => b.toString(16).padStart(2, "0")).join("");
}

export function constantTimeEqual(a, b) {
  if (typeof a !== "string" || typeof b !== "string") return false;
  const x = new TextEncoder().encode(a), y = new TextEncoder().encode(b);
  let diff = x.length ^ y.length;
  for (let i = 0; i < Math.max(x.length, y.length); i++) diff |= (x[i] ?? 0) ^ (y[i] ?? 0);
  return diff === 0;
}

// What Twitch says about an account decides whether it may be listed at all.
export function verdictOf(user) {
  if (!user) return "gone";
  if (user.type || user.broadcaster_type) return "protected";
  if (SERVICE_BOTS.has(String(user.login).toLowerCase())) return "protected";
  return "ok";
}

export function isPublishable(reports, removed) {
  return reports >= (removed ? LIMITS.afterRemoval : LIMITS.publishFrom);
}

export function keyOf(category, id) {
  return category + ":" + id;
}

// Old and new rows of the touched accounts -> the events a client applies; a row is {category, id, login, reports}.
export function diff(previous, desired, whyGone) {
  const before = new Map(previous.map(r => [keyOf(r.category, r.id), r]));
  const after = new Map(desired.map(r => [keyOf(r.category, r.id), r]));
  const events = [];
  for (const [key, row] of after) {
    const old = before.get(key);
    if (!old) events.push({ op: "add", category: row.category, id: row.id, login: row.login, reports: row.reports });
    else if (old.login !== row.login || old.reports !== row.reports)
      events.push({ op: "update", category: row.category, id: row.id, login: row.login, reports: row.reports });
  }
  for (const [key, row] of before) {
    if (!after.has(key))
      events.push({ op: "remove", category: row.category, id: row.id, why: whyGone(row) });
  }
  const order = { add: 0, update: 1, remove: 2 };
  events.sort((a, b) => order[a.op] - order[b.op] || a.category.localeCompare(b.category) || compareIds(a.id, b.id));
  return events;
}

// removed: by request; gone: Twitch no longer has it; protected: partner, affiliate, staff or a service bot;
// dropped: its reports were retracted or expired. A removal concerns the row when the row's reports predate it,
// since a returning account only counts reports made after its removal.
export function whyGoneOf(account, row) {
  if (!account) return "dropped";
  if (account.removed_at != null && account.removed_at >= row.first_at) return "removed";
  if (account.status === "gone") return "gone";
  if (account.status === "protected") return "protected";
  return "dropped";
}

export function compareIds(a, b) {
  return a.length - b.length || (a < b ? -1 : a > b ? 1 : 0);
}

function day(seconds) {
  return new Date(seconds * 1000).toISOString().slice(0, 10);
}

function stamp(seconds) {
  return new Date(seconds * 1000).toISOString().replace(/\.\d{3}Z$/, "Z");
}

function json(value) {
  return JSON.stringify(value, null, 1) + "\n";
}

// published rows: {category, id, login, reports, first_at, last_at, reasons}; events: {version, at, op, ...}.
export function buildFiles({ version, now, published, events, changesSince, removals, repo, form }) {
  const files = {};
  const lists = {};
  for (const category of CATEGORIES) {
    const rows = published
      .filter(r => r.category === category)
      .sort((a, b) => a.login.localeCompare(b.login) || compareIds(a.id, b.id));
    const name = FILE_OF[category];
    files[name + ".json"] = json({
      schema: SCHEMA, version, updated: stamp(now), category, banFrom: LIMITS.banFrom,
      accounts: rows.map(r => ({
        id: r.id, login: r.login, reports: r.reports, first: day(r.first_at), last: day(r.last_at),
        reasons: String(r.reasons || "").split(",").filter(Boolean).sort(),
      })),
    });
    const confirmed = rows.filter(r => r.reports >= LIMITS.banFrom).map(r => r.login);
    files[name + ".txt"] = confirmed.length ? confirmed.join("\n") + "\n" : "";
    lists[category] = { file: name + ".json", text: name + ".txt", count: rows.length, confirmed: confirmed.length };
  }
  files["changes.json"] = json({
    schema: SCHEMA, version, since: changesSince,
    changes: events.map(e => {
      const out = { v: e.version, at: stamp(e.at), op: e.op, category: e.category, id: e.id };
      if (e.op === "remove") out.why = e.why;
      else { out.login = e.login; out.reports = e.reports; }
      return out;
    }),
  });
  files["removed.json"] = json({
    schema: SCHEMA, version,
    removed: removals.map(r => ({ id: r.account_id, at: day(r.at) })),
  });
  files["index.json"] = json({
    schema: SCHEMA, version, updated: stamp(now), banFrom: LIMITS.banFrom, lists,
    changes: { file: "changes.json", since: changesSince },
    removed: { file: "removed.json", count: removals.length },
  });
  files["README.md"] = readme(repo, form);
  return files;
}

export function readme(repo, form) {
  const removal = `https://github.com/${repo}/issues/new?template=${form}`;
  return `# TwitchSentry Bot List

Twitch accounts that [TwitchSentry](https://github.com/${repo}) installations identified as bots, in three lists:

| List | What put an account there |
|---|---|
| \`spam.json\` / \`spam.txt\` | Spam Filter: a decisive hit (known spam domain, spam keyword, conversation scam, ...) |
| \`lurkbots.json\` / \`lurkbots.txt\` | LurkBot Filter: a bot-shaped name created on a known bot day, or with others the same day |
| \`botwaves.json\` / \`botwaves.txt\` | Follow Protection follow waves and Raid Protection spam swarms |

This branch is written automatically every few minutes and holds nothing else. Use it freely: the data is
dedicated to the public domain under [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/).

## Was an account listed by mistake?

[Request its removal](${removal}). It comes off the list as soon as the request is read, every TwitchSentry
installation that banned it through this list lifts that ban, and the installations that reported it are
not counted for it again.

## Reading the lists

- \`*.txt\`: one login per line, only accounts at least **${LIMITS.banFrom} independent channels** reported.
  This is the list to import into a ban tool.
- \`*.json\`: every listed account, with \`reports\` (independent channels), \`first\`/\`last\` report day
  and \`reasons\`. One report is enough to appear here; TwitchSentry only bans from \`banFrom\` reports.
  Twitch ids are stable, logins are refreshed when an account renames.
- \`index.json\`: the current \`version\` and counts. Poll this file; the others only change with it.
  GitHub serves raw files with a five-minute cache, so polling faster gains nothing.
- \`changes.json\`: every change since version \`since\`, oldest first (\`add\`, \`update\`, \`remove\` with
  \`why\`: \`removed\` on request, \`gone\` from Twitch, \`protected\`, \`dropped\` when its reports were
  retracted or expired). A reader at \`since\` or later can catch up from this file alone.
- \`removed.json\`: ids removed on request in the last ${LIMITS.keepDays} days.

Partners, affiliates, Twitch staff and well-known service bots are never listed. Neither the reporting
channels nor any chat message are published.
`;
}
