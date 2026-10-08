// D1 access. Lists travel as one JSON parameter through json_each, so a batch costs one query, not one per row.

const TABLES = [
  "CREATE TABLE IF NOT EXISTS accounts (id TEXT PRIMARY KEY, login TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'pending', checked_at INTEGER NOT NULL DEFAULT 0, removed_at INTEGER)",
  "CREATE INDEX IF NOT EXISTS accounts_login ON accounts(login)",
  "CREATE INDEX IF NOT EXISTS accounts_check ON accounts(status, checked_at)",
  "CREATE TABLE IF NOT EXISTS reports (account_id TEXT NOT NULL, category TEXT NOT NULL, install TEXT NOT NULL, net TEXT NOT NULL, reason TEXT NOT NULL, first_at INTEGER NOT NULL, last_at INTEGER NOT NULL, PRIMARY KEY (account_id, category, install))",
  "CREATE INDEX IF NOT EXISTS reports_last ON reports(last_at)",
  "CREATE TABLE IF NOT EXISTS voided (account_id TEXT NOT NULL, install TEXT NOT NULL, PRIMARY KEY (account_id, install))",
  "CREATE TABLE IF NOT EXISTS touched (account_id TEXT PRIMARY KEY, at INTEGER NOT NULL)",
  "CREATE TABLE IF NOT EXISTS published (category TEXT NOT NULL, account_id TEXT NOT NULL, login TEXT NOT NULL, reports INTEGER NOT NULL, first_at INTEGER NOT NULL, last_at INTEGER NOT NULL, reasons TEXT NOT NULL, PRIMARY KEY (category, account_id))",
  "CREATE INDEX IF NOT EXISTS published_account ON published(account_id)",
  "CREATE TABLE IF NOT EXISTS events (version INTEGER NOT NULL, at INTEGER NOT NULL, op TEXT NOT NULL, category TEXT NOT NULL, account_id TEXT NOT NULL, login TEXT, reports INTEGER, why TEXT)",
  "CREATE INDEX IF NOT EXISTS events_version ON events(version)",
  "CREATE TABLE IF NOT EXISTS removals (account_id TEXT NOT NULL, login TEXT NOT NULL, at INTEGER NOT NULL, issue INTEGER, by TEXT)",
  "CREATE TABLE IF NOT EXISTS meta (k TEXT PRIMARY KEY, v TEXT NOT NULL)",
  "CREATE TABLE IF NOT EXISTS hits (k TEXT PRIMARY KEY, at INTEGER NOT NULL, n INTEGER NOT NULL)",
];

const IDS = "SELECT value FROM json_each(?1)";

let schemaReady = null;

export function ensureSchema(db) {
  if (!schemaReady)
    schemaReady = db.batch(TABLES.map(sql => db.prepare(sql))).catch(err => {
      schemaReady = null;
      throw err;
    });
  return schemaReady;
}

const META_DEFAULTS = { version: 0, diff_at: 0, pending_commit: 0, changes_since: 0, prune_at: 0, commit: "", commit_at: 0, error: "", twitch_error: "" };

export async function readMeta(db) {
  const { results } = await db.prepare("SELECT k, v FROM meta").all();
  const meta = { ...META_DEFAULTS };
  for (const { k, v } of results)
    if (k in meta) meta[k] = typeof META_DEFAULTS[k] === "number" ? Number(v) : v;
  return meta;
}

export function writeMeta(db, values) {
  const rows = JSON.stringify(Object.entries(values).map(([k, v]) => ({ k, v: String(v) })));
  return db.prepare("INSERT INTO meta (k, v) SELECT json_extract(value, '$.k'), json_extract(value, '$.v') FROM json_each(?1) WHERE true ON CONFLICT(k) DO UPDATE SET v = excluded.v").bind(rows);
}

export async function takeLock(db, now, seconds) {
  const r = await db.prepare("INSERT INTO meta (k, v) VALUES ('lock', ?1) ON CONFLICT(k) DO UPDATE SET v = excluded.v WHERE CAST(meta.v AS INTEGER) < ?2")
    .bind(String(now + seconds), now).run();
  return r.meta.changes > 0;
}

export function releaseLock(db) {
  return db.prepare("UPDATE meta SET v = '0' WHERE k = 'lock'").run();
}

// One counter per key and hour; the answer is the count after this spend.
export async function spend(db, key, now, amount) {
  const row = await db.prepare("INSERT INTO hits (k, at, n) VALUES (?1, ?2, ?3) ON CONFLICT(k) DO UPDATE SET n = hits.n + excluded.n RETURNING n")
    .bind(`${key}:${Math.floor(now / 3600)}`, now, amount).first();
  return row ? Number(row.n) : amount;
}

export async function recordReports(db, { install, net, now, items }) {
  const ids = JSON.stringify([...new Set(items.map(i => i.id))]);
  const [known, voided] = await db.batch([
    db.prepare(`SELECT id, status FROM accounts WHERE id IN (${IDS})`).bind(ids),
    db.prepare(`SELECT account_id FROM voided WHERE install = ?2 AND account_id IN (${IDS})`).bind(ids, install),
  ]);
  const status = new Map(known.results.map(r => [r.id, r.status]));
  const isVoided = new Set(voided.results.map(r => r.account_id));

  const accepted = [];
  const ignored = [];
  for (const item of items) {
    if (status.get(item.id) === "protected") ignored.push({ i: item.i, why: "protected" });
    else if (isVoided.has(item.id)) ignored.push({ i: item.i, why: "removed" });
    else accepted.push(item);
  }
  if (accepted.length === 0) return { accepted: 0, ignored };

  const rows = JSON.stringify(accepted.map(a => ({ id: a.id, login: a.login, category: a.category, reason: a.reason })));
  await db.batch([
    db.prepare("INSERT INTO accounts (id, login) SELECT json_extract(value, '$.id'), json_extract(value, '$.login') FROM json_each(?1) WHERE true ON CONFLICT(id) DO UPDATE SET status = CASE WHEN accounts.status = 'gone' THEN 'pending' ELSE accounts.status END")
      .bind(rows),
    db.prepare("INSERT INTO reports (account_id, category, install, net, reason, first_at, last_at) SELECT json_extract(value, '$.id'), json_extract(value, '$.category'), ?2, ?3, json_extract(value, '$.reason'), ?4, ?4 FROM json_each(?1) WHERE true ON CONFLICT(account_id, category, install) DO UPDATE SET reason = excluded.reason, last_at = excluded.last_at")
      .bind(rows, install, net, now),
    touch(db, accepted.map(a => a.id)),
  ]);
  return { accepted: accepted.length, ignored };
}

export async function retractReports(db, { install, items }) {
  const rows = JSON.stringify(items.map(i => ({ id: i.id, category: i.category })));
  const [deleted] = await db.batch([
    db.prepare("DELETE FROM reports WHERE install = ?2 AND EXISTS (SELECT 1 FROM json_each(?1) AS j WHERE json_extract(j.value, '$.id') = reports.account_id AND (json_extract(j.value, '$.category') IS NULL OR json_extract(j.value, '$.category') = reports.category))")
      .bind(rows, install),
    touch(db, items.map(i => i.id)),
  ]);
  return deleted.meta.changes;
}

export function touch(db, ids) {
  return db.prepare(`INSERT INTO touched (account_id, at) SELECT DISTINCT value, ?2 FROM json_each(?1) WHERE true ON CONFLICT(account_id) DO UPDATE SET at = excluded.at`)
    .bind(JSON.stringify([...new Set(ids)]), Date.now());
}

export async function findAccounts(db, ids, logins) {
  const { results } = await db.prepare(`SELECT id, login, status, removed_at FROM accounts WHERE id IN (${IDS}) OR login IN (SELECT value FROM json_each(?2))`)
    .bind(JSON.stringify(ids), JSON.stringify(logins)).all();
  return results;
}

export async function listedIds(db, ids) {
  const { results } = await db.prepare(`SELECT DISTINCT account_id FROM published WHERE account_id IN (${IDS})`).bind(JSON.stringify(ids)).all();
  return new Set(results.map(r => r.account_id));
}

// The reporters of a removed account are remembered so their next report of it is ignored.
export async function removeAccounts(db, accounts, { now, issue, by }) {
  const ids = JSON.stringify(accounts.map(a => a.id));
  const rows = JSON.stringify(accounts.map(a => ({ id: a.id, login: a.login })));
  await db.batch([
    db.prepare(`INSERT INTO voided (account_id, install) SELECT account_id, install FROM reports WHERE account_id IN (${IDS}) ON CONFLICT DO NOTHING`).bind(ids),
    db.prepare(`DELETE FROM reports WHERE account_id IN (${IDS})`).bind(ids),
    db.prepare(`UPDATE accounts SET removed_at = ?2 WHERE id IN (${IDS})`).bind(ids, now),
    db.prepare("INSERT INTO removals (account_id, login, at, issue, by) SELECT json_extract(value, '$.id'), json_extract(value, '$.login'), ?2, ?3, ?4 FROM json_each(?1)")
      .bind(rows, now, issue, by),
    touch(db, accounts.map(a => a.id)),
  ]);
}

export async function accountsToCheck(db, now, staleBefore, limit) {
  const { results } = await db.prepare("SELECT id, login, status FROM accounts WHERE status = 'pending' OR (status IN ('ok', 'gone') AND checked_at < ?1) ORDER BY status = 'pending' DESC, checked_at LIMIT ?2")
    .bind(staleBefore, limit).all();
  return results;
}

export function setChecked(db, rows, now) {
  return db.prepare("UPDATE accounts SET status = j.status, login = COALESCE(j.login, accounts.login), checked_at = ?2 FROM (SELECT json_extract(value, '$.id') AS id, json_extract(value, '$.status') AS status, json_extract(value, '$.login') AS login FROM json_each(?1)) AS j WHERE accounts.id = j.id")
    .bind(JSON.stringify(rows), now);
}

export async function readTouched(db, limit) {
  const { results } = await db.prepare("SELECT account_id, at FROM touched ORDER BY at LIMIT ?1").bind(limit).all();
  return results;
}

export async function desiredRows(db, ids) {
  const { results } = await db.prepare(`SELECT r.category AS category, r.account_id AS id, a.login AS login, a.removed_at AS removed_at, COUNT(DISTINCT r.net) AS reports, MIN(r.first_at) AS first_at, MAX(r.last_at) AS last_at, GROUP_CONCAT(DISTINCT r.reason) AS reasons FROM reports AS r JOIN accounts AS a ON a.id = r.account_id WHERE a.status = 'ok' AND r.account_id IN (${IDS}) GROUP BY r.category, r.account_id`)
    .bind(JSON.stringify(ids)).all();
  return results;
}

export async function publishedRows(db, ids) {
  const sql = ids
    ? `SELECT category, account_id AS id, login, reports, first_at, last_at, reasons FROM published WHERE account_id IN (${IDS})`
    : "SELECT category, account_id AS id, login, reports, first_at, last_at, reasons FROM published";
  const stmt = db.prepare(sql);
  const { results } = await (ids ? stmt.bind(JSON.stringify(ids)) : stmt).all();
  return results;
}

export async function accountStates(db, ids) {
  const { results } = await db.prepare(`SELECT id, status, removed_at FROM accounts WHERE id IN (${IDS})`).bind(JSON.stringify(ids)).all();
  return new Map(results.map(r => [r.id, r]));
}

// Writes one diff: the published table, the events and the touched rows it consumed.
export function applyDiff(db, { desired, removedKeys, events, version, now, touchedIds, touchedUpTo }) {
  const stmts = [];
  if (desired.length)
    stmts.push(db.prepare("INSERT INTO published (category, account_id, login, reports, first_at, last_at, reasons) SELECT json_extract(value, '$.category'), json_extract(value, '$.id'), json_extract(value, '$.login'), json_extract(value, '$.reports'), json_extract(value, '$.first_at'), json_extract(value, '$.last_at'), json_extract(value, '$.reasons') FROM json_each(?1) WHERE true ON CONFLICT(category, account_id) DO UPDATE SET login = excluded.login, reports = excluded.reports, first_at = excluded.first_at, last_at = excluded.last_at, reasons = excluded.reasons")
      .bind(JSON.stringify(desired.map(r => ({ category: r.category, id: r.id, login: r.login, reports: r.reports, first_at: r.first_at, last_at: r.last_at, reasons: r.reasons || "" })))));
  if (removedKeys.length)
    stmts.push(db.prepare("DELETE FROM published WHERE category || ':' || account_id IN (SELECT value FROM json_each(?1))").bind(JSON.stringify(removedKeys)));
  if (events.length)
    stmts.push(db.prepare("INSERT INTO events (version, at, op, category, account_id, login, reports, why) SELECT ?2, ?3, json_extract(value, '$.op'), json_extract(value, '$.category'), json_extract(value, '$.id'), json_extract(value, '$.login'), json_extract(value, '$.reports'), json_extract(value, '$.why') FROM json_each(?1)")
      .bind(JSON.stringify(events), version, now));
  stmts.push(db.prepare(`DELETE FROM touched WHERE account_id IN (${IDS}) AND at <= ?2`).bind(JSON.stringify(touchedIds), touchedUpTo));
  const meta = { diff_at: now };
  if (events.length) Object.assign(meta, { version, pending_commit: 1 });
  stmts.push(writeMeta(db, meta));
  return db.batch(stmts);
}

export async function eventsSince(db, version) {
  const { results } = await db.prepare("SELECT version, at, op, category, account_id AS id, login, reports, why FROM events WHERE version > ?1 ORDER BY version, rowid").bind(version).all();
  return results;
}

export async function recentRemovals(db, since) {
  const { results } = await db.prepare("SELECT account_id, MAX(at) AS at FROM removals WHERE at >= ?1 GROUP BY account_id ORDER BY at, account_id").bind(since).all();
  return results;
}

// Hourly: expire old reports, trim the change log and forget what nothing points at any more.
export async function prune(db, now, meta, { keepDays, changesDays }) {
  const keepFrom = now - keepDays * 86400;
  const changesFrom = now - changesDays * 86400;
  const last = await db.prepare("SELECT MAX(version) AS v FROM events WHERE at < ?1").bind(changesFrom).first();
  const since = Math.max(meta.changes_since, Number(last?.v ?? 0));
  await db.batch([
    db.prepare("INSERT INTO touched (account_id, at) SELECT DISTINCT account_id, ?2 FROM reports WHERE last_at < ?1 ON CONFLICT(account_id) DO UPDATE SET at = excluded.at").bind(keepFrom, Date.now()),
    db.prepare("DELETE FROM reports WHERE last_at < ?1").bind(keepFrom),
    db.prepare("DELETE FROM events WHERE at < ?1").bind(changesFrom),
    db.prepare("DELETE FROM removals WHERE at < ?1").bind(keepFrom),
    db.prepare("DELETE FROM hits WHERE at < ?1").bind(now - 7200),
    db.prepare("DELETE FROM accounts WHERE removed_at IS NULL AND NOT EXISTS (SELECT 1 FROM reports WHERE reports.account_id = accounts.id) AND NOT EXISTS (SELECT 1 FROM published WHERE published.account_id = accounts.id) AND NOT EXISTS (SELECT 1 FROM touched WHERE touched.account_id = accounts.id)"),
    writeMeta(db, { changes_since: since, prune_at: now }),
  ]);
  return since;
}

export async function counts(db, banFrom) {
  const [byCategory, pending] = await db.batch([
    db.prepare("SELECT category, COUNT(*) AS n, SUM(reports >= ?1) AS confirmed FROM published GROUP BY category").bind(banFrom),
    db.prepare("SELECT COUNT(*) AS n FROM accounts WHERE status = 'pending'"),
  ]);
  const lists = {};
  for (const r of byCategory.results) lists[r.category] = { count: r.n, confirmed: r.confirmed };
  return { lists, pending: pending.results[0]?.n ?? 0 };
}
