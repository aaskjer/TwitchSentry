// The second witness: the groups of an external ban list repository (EXTERNAL_REPO), read through GitHub's API
// with the relay's token. The tree is read every half hour, then one changed file per pass.

import { LIMITS, EXTERNAL_LISTS, parseExternalList, nextExternal } from "./rules.js";
import * as store from "./store.js";

async function get(env, path, accept) {
  const res = await fetch((env.GITHUB_API || "https://api.github.com") + "/repos/" + env.EXTERNAL_REPO + path, {
    headers: {
      ...(env.GITHUB_TOKEN ? { Authorization: "Bearer " + env.GITHUB_TOKEN } : {}),
      Accept: accept,
      "X-GitHub-Api-Version": "2022-11-28",
      "User-Agent": "TwitchSentry-BotList-Relay",
    },
  });
  if (!res.ok) throw new Error(`${env.EXTERNAL_REPO} answered ${res.status} for ${path}`);
  return res;
}

async function readTree(env) {
  const branch = encodeURIComponent(env.EXTERNAL_BRANCH || "main");
  const body = await (await get(env, `/git/trees/${branch}`, "application/vnd.github+json")).json();
  if (!Array.isArray(body.tree)) throw new Error(`${env.EXTERNAL_REPO} answered without a file tree`);
  const want = {};
  for (const entry of body.tree)
    if (entry.type === "blob" && Object.hasOwn(EXTERNAL_LISTS, entry.path)) want[entry.path] = entry.sha;
  return want;
}

function parsed(text) {
  try {
    const value = JSON.parse(text);
    return value && typeof value === "object" && !Array.isArray(value) ? value : {};
  } catch {
    return {};
  }
}

// Never throws: a source that cannot be read keeps the last lists it gave and says so in health.
// At most one batch per pass, and none while nothing is due. Without EXTERNAL_REPO the lists it left are emptied.
export async function refreshExternal(env, db, meta, now) {
  const configured = Boolean(env.EXTERNAL_REPO);
  if (!configured && meta.ext_have === "{}" && !meta.ext_error) return { configured: false };
  try {
    const update = {};
    let want = configured ? parsed(meta.ext_want) : {};
    if (configured && now - meta.ext_checked_at >= LIMITS.externalCheckSeconds) {
      want = await readTree(env);
      Object.assign(update, { ext_want: JSON.stringify(want), ext_checked_at: now });
    }
    const have = parsed(meta.ext_have);
    const next = nextExternal(want, have);
    const stmts = [];
    let names = 0;
    if (next) {
      const logins = next.sha
        ? parseExternalList(await (await get(env, `/git/blobs/${next.sha}`, "application/vnd.github.raw")).text())
        : [];
      if (next.clear) stmts.push(...store.replaceExternal(db, { list: next.list, category: next.clear, logins: [] }));
      stmts.push(...store.replaceExternal(db, { list: next.list, category: next.category, logins }));
      if (next.sha) have[next.list] = { sha: next.sha, category: next.category, n: logins.length };
      else delete have[next.list];
      update.ext_have = JSON.stringify(have);
      names = logins.length;
    }
    if (meta.ext_error) update.ext_error = "";
    if (Object.keys(update).length) stmts.push(store.writeMeta(db, update));
    if (stmts.length) await db.batch(stmts);
    return next ? { imported: next.list, names } : { imported: null };
  } catch (err) {
    const error = String(err.message || err).slice(0, 300);
    await store.writeMeta(db, { ext_error: error }).run();
    return { error };
  }
}
