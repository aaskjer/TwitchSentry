// Writes the whole bot list branch as one commit: tree with inline contents, commit, ref.
// Three content-creating requests per publish keeps far under GitHub's 80 per minute and 500 per hour.

function api(env) {
  return (env.GITHUB_API || "https://api.github.com") + "/repos/" + env.GITHUB_REPO;
}

async function call(env, method, path, body) {
  const res = await fetch(api(env) + path, {
    method,
    headers: {
      Authorization: "Bearer " + env.GITHUB_TOKEN,
      Accept: "application/vnd.github+json",
      "X-GitHub-Api-Version": "2022-11-28",
      "User-Agent": "TwitchSentry-BotList-Relay",
      ...(body ? { "Content-Type": "application/json" } : {}),
    },
    body: body ? JSON.stringify(body) : undefined,
  });
  const text = await res.text();
  let data = null;
  try { data = text ? JSON.parse(text) : null; } catch { data = null; }
  return { status: res.status, data, text };
}

function failure(step, r) {
  const said = r.data && r.data.message ? r.data.message : r.text.slice(0, 200);
  return new Error(`GitHub refused ${step} (${r.status}): ${said}`);
}

export async function commitFiles(env, files, message) {
  const branch = env.GITHUB_BRANCH;
  const tree = Object.entries(files).map(([path, content]) => ({ path, mode: "100644", type: "blob", content }));

  for (let attempt = 0; attempt < 3; attempt++) {
    const ref = await call(env, "GET", `/git/ref/heads/${branch}`);
    if (ref.status !== 200 && ref.status !== 404) throw failure("reading the branch", ref);
    const parent = ref.status === 200 ? ref.data.object.sha : null;

    const t = await call(env, "POST", "/git/trees", { tree });
    if (t.status !== 201) throw failure("the tree", t);
    const c = await call(env, "POST", "/git/commits", { message, tree: t.data.sha, parents: parent ? [parent] : [] });
    if (c.status !== 201) throw failure("the commit", c);

    const moved = parent
      ? await call(env, "PATCH", `/git/refs/heads/${branch}`, { sha: c.data.sha, force: false })
      : await call(env, "POST", "/git/refs", { ref: `refs/heads/${branch}`, sha: c.data.sha });
    if (moved.status === 200 || moved.status === 201) return c.data.sha;
    // Somebody else moved the branch in between: build on the new tip.
    if (moved.status !== 422) throw failure("moving the branch", moved);
  }
  throw new Error("GitHub kept moving the branch while the list was being written");
}
