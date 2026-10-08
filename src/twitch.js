// Twitch app access (client credentials): only Get Users, which is all the relay needs to judge an account.

import { writeMeta } from "./store.js";

export function twitchConfigured(env) {
  return Boolean(env.TWITCH_CLIENT_ID && env.TWITCH_CLIENT_SECRET);
}

async function newToken(env) {
  const url = new URL(env.TWITCH_AUTH || "https://id.twitch.tv/oauth2/token");
  url.searchParams.set("client_id", env.TWITCH_CLIENT_ID);
  url.searchParams.set("client_secret", env.TWITCH_CLIENT_SECRET);
  url.searchParams.set("grant_type", "client_credentials");
  const res = await fetch(url, { method: "POST" });
  if (!res.ok) throw new Error(`Twitch refused an app token (${res.status})`);
  const body = await res.json();
  if (!body.access_token) throw new Error("Twitch answered without an app token");
  return { token: body.access_token, expires: Math.floor(Date.now() / 1000) + Number(body.expires_in || 3600) };
}

async function token(env, db, renew) {
  if (!renew) {
    const row = await db.prepare("SELECT v FROM meta WHERE k = 'twitch_token'").first();
    if (row) {
      try {
        const cached = JSON.parse(row.v);
        if (cached.token && cached.expires - 3600 > Math.floor(Date.now() / 1000)) return cached.token;
      } catch { /* a broken cache is simply renewed */ }
    }
  }
  const fresh = await newToken(env);
  await writeMeta(db, { twitch_token: JSON.stringify(fresh) }).run();
  return fresh.token;
}

// Up to 100 ids and logins together; the answer maps id -> {id, login, type, broadcaster_type}.
export async function getUsers(env, db, { ids = [], logins = [] }) {
  const found = new Map();
  if (ids.length + logins.length === 0) return found;
  if (ids.length + logins.length > 100) throw new Error("Get Users takes at most 100 names");
  const url = new URL((env.TWITCH_API || "https://api.twitch.tv/helix") + "/users");
  for (const id of ids) url.searchParams.append("id", id);
  for (const login of logins) url.searchParams.append("login", login);

  for (let attempt = 0; attempt < 2; attempt++) {
    const res = await fetch(url, {
      headers: { "Client-Id": env.TWITCH_CLIENT_ID, Authorization: "Bearer " + await token(env, db, attempt > 0) },
    });
    if (res.status === 401 && attempt === 0) continue;
    if (!res.ok) throw new Error(`Twitch Get Users answered ${res.status}`);
    const body = await res.json();
    for (const u of body.data || [])
      found.set(String(u.id), { id: String(u.id), login: String(u.login).toLowerCase(), type: u.type || "", broadcaster_type: u.broadcaster_type || "" });
    return found;
  }
  throw new Error("Twitch kept refusing the app token");
}
