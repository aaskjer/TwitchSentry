// One publish pass: check accounts with Twitch, turn touched accounts into events, write the branch.

import { LIMITS, CATEGORIES, diff, isPublishable, keyOf, whyGoneOf, verdictOf, buildFiles } from "./rules.js";
import * as store from "./store.js";
import { getUsers, twitchConfigured } from "./twitch.js";
import { commitFiles } from "./github.js";

export const REMOVAL_FORM = "botlist-removal.yml";

const TOUCHED_PER_ROUND = 500;
const ROUNDS = 3;

export async function verifyAccounts(env, db, now) {
  if (!twitchConfigured(env)) return { checked: 0, error: "Twitch is not configured" };
  const rows = await store.accountsToCheck(db, now, now - LIMITS.recheckDays * 86400, 100);
  if (rows.length === 0) return { checked: 0 };
  let users;
  try {
    users = await getUsers(env, db, { ids: rows.map(r => r.id) });
  } catch (err) {
    return { checked: 0, error: String(err.message || err) };
  }
  const updates = rows.map(r => {
    const u = users.get(r.id);
    return { id: r.id, status: verdictOf(u), login: u ? u.login : null };
  });
  const changed = updates.filter((u, i) => u.status !== rows[i].status || (u.login && u.login !== rows[i].login)).map(u => u.id);
  const stmts = [store.setChecked(db, updates, now)];
  if (changed.length) stmts.push(store.touch(db, changed));
  await db.batch(stmts);
  return { checked: rows.length, changed: changed.length };
}

async function diffTouched(db, version, now) {
  const touched = await store.readTouched(db, TOUCHED_PER_ROUND);
  if (touched.length === 0) return { events: [], version, drained: true };
  const ids = touched.map(t => t.account_id);
  const upTo = Math.max(...touched.map(t => t.at));
  const [rows, previous, states] = await Promise.all([
    store.desiredRows(db, ids), store.publishedRows(db, ids), store.accountStates(db, ids),
  ]);
  const desired = rows.filter(r => isPublishable(r.reports, r.removed_at != null));
  const events = diff(previous, desired, row => whyGoneOf(states.get(row.id), row));
  const kept = new Set(desired.map(r => keyOf(r.category, r.id)));
  const removedKeys = previous.map(r => keyOf(r.category, r.id)).filter(k => !kept.has(k));
  const next = events.length ? version + 1 : version;
  await store.applyDiff(db, { desired, removedKeys, events, version: next, now, touchedIds: ids, touchedUpTo: upTo });
  return { events, version: next, drained: touched.length < TOUCHED_PER_ROUND };
}

export function commitMessage(version, events) {
  const parts = [];
  for (const category of CATEGORIES) {
    const added = events.filter(e => e.category === category && e.op === "add").length;
    const removed = events.filter(e => e.category === category && e.op === "remove").length;
    if (added) parts.push(`+${added} ${category}`);
    if (removed) parts.push(`-${removed} ${category}`);
  }
  const updated = events.filter(e => e.op === "update").length;
  if (updated) parts.push(`${updated} updated`);
  return `Bot list v${version}` + (parts.length ? ": " + parts.join(", ") : "");
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

export async function publish(env, { force = false, now = Math.floor(Date.now() / 1000), waitForLock = 0 } = {}) {
  const db = env.DB;
  await store.ensureSchema(db);
  let locked = await store.takeLock(db, now, LIMITS.lockSeconds);
  for (let i = 0; !locked && i < waitForLock; i++) {
    await sleep(2000);
    locked = await store.takeLock(db, now, LIMITS.lockSeconds);
  }
  if (!locked) return { ok: false, skipped: "another publish is running" };

  try {
    const meta = await store.readMeta(db);
    const verified = await verifyAccounts(env, db, now);
    let since = meta.changes_since;
    if (now - meta.prune_at >= 3600) since = await store.prune(db, now, meta, LIMITS);

    let version = meta.version;
    const events = [];
    for (let round = 0; round < ROUNDS; round++) {
      const r = await diffTouched(db, version, now);
      events.push(...r.events);
      version = r.version;
      if (r.drained) break;
    }

    const due = events.length > 0 || meta.pending_commit === 1 || !meta.commit || force;
    if (!due) return { ok: true, changed: false, version, verified };
    if (!env.GITHUB_TOKEN || !env.GITHUB_REPO || !env.GITHUB_BRANCH) {
      await store.writeMeta(db, { error: "GitHub is not configured" }).run();
      return { ok: false, changed: events.length > 0, committed: false, version, verified, error: "GitHub is not configured" };
    }

    const [published, changes, removals] = await Promise.all([
      store.publishedRows(db, null),
      store.eventsSince(db, since),
      store.recentRemovals(db, now - LIMITS.keepDays * 86400),
    ]);
    const files = buildFiles({
      version, now, published, events: changes, changesSince: since, removals,
      repo: env.GITHUB_REPO, form: REMOVAL_FORM,
    });
    try {
      const sha = await commitFiles(env, files, commitMessage(version, events));
      await store.writeMeta(db, { pending_commit: 0, commit: sha, commit_at: now, error: "" }).run();
      return { ok: true, changed: events.length > 0, committed: true, version, commit: sha, verified };
    } catch (err) {
      const error = String(err.message || err).slice(0, 300);
      await store.writeMeta(db, { pending_commit: 1, error }).run();
      return { ok: false, changed: events.length > 0, committed: false, version, verified, error };
    }
  } finally {
    await store.releaseLock(db);
  }
}

export { getUsers, twitchConfigured };
