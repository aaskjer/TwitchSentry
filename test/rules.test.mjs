import { test } from "node:test";
import assert from "node:assert/strict";
import {
  parseReport, parseRetract, parseRemoval, networkOf, hashKey, constantTimeEqual, verdictOf,
  isPublishable, diff, whyGoneOf, buildFiles, compareIds, normaliseLogin, LIMITS,
} from "../src/rules.js";

const INSTALL = "3f2b8c1e-9d4a-4b7e-8a1c-2e5f6a7b8c9d";
const base = { install: INSTALL, version: "v3.2.0" };

test("a report keeps what is readable and says why the rest was left out", () => {
  const r = parseReport({
    ...base,
    reports: [
      { category: "spam", id: "1001", login: "@SpamBot_One", reason: "spam_domain" },
      { category: "spam", id: "1001", login: "spambot_one", reason: "keyword" },
      { category: "lurkbot", id: "1001", login: "spambot_one", reason: "known_day" },
      { category: "nonsense", id: "1002", login: "x", reason: "keyword" },
      { category: "spam", id: "01", login: "x", reason: "keyword" },
      { category: "spam", id: "1003", login: "has space", reason: "keyword" },
      { category: "spam", id: "1004", login: "nightbot", reason: "keyword" },
      { category: "spam", id: "1005", login: "ok_name", reason: "Not-A-Code" },
      { category: "botwave", id: "1006", login: "wave_bot", reason: "brand_new_code" },
      "text",
    ],
  });
  assert.equal(r.error, undefined);
  assert.deepEqual(r.items.map(i => [i.category, i.id, i.login, i.reason]), [
    ["spam", "1001", "spambot_one", "spam_domain"],
    ["lurkbot", "1001", "spambot_one", "known_day"],
    ["botwave", "1006", "wave_bot", "other"],
  ]);
  assert.deepEqual(r.ignored.map(x => [x.i, x.why]), [
    [1, "duplicate"], [3, "category"], [4, "id"], [5, "login"], [6, "service_bot"], [7, "reason"], [9, "not_an_object"],
  ]);
});

test("a report without a proper header is refused whole", () => {
  assert.match(parseReport(null).error, /JSON object/);
  assert.match(parseReport({ ...base, install: "not-a-uuid", reports: [{}] }).error, /UUID/);
  assert.match(parseReport({ ...base, install: "3f2b8c1e-9d4a-3b7e-8a1c-2e5f6a7b8c9d", reports: [{}] }).error, /UUID/);
  assert.match(parseReport({ ...base, version: "3.2.0", reports: [{}] }).error, /release tag/);
  assert.ok(parseReport({ ...base, version: "v3.2.0-beta.1", reports: [{ category: "spam", id: "1", login: "a", reason: "keyword" }] }).items.length === 1);
  assert.match(parseReport({ ...base, reports: [] }).error, /empty/);
  const many = Array.from({ length: LIMITS.maxItems + 1 }, (_, i) => ({ category: "spam", id: String(i + 1), login: "a", reason: "keyword" }));
  assert.match(parseReport({ ...base, reports: many }).error, /more than/);
});

test("an install id is read case-insensitively", () => {
  const r = parseReport({ ...base, install: INSTALL.toUpperCase(), reports: [{ category: "spam", id: "1", login: "a", reason: "keyword" }] });
  assert.equal(r.install, INSTALL);
});

test("a retraction may name a category or leave it open", () => {
  const r = parseRetract({ ...base, retract: [{ id: "1001", category: "spam" }, { id: "1002" }, { id: "x" }, { id: "3", category: "foo" }] });
  assert.deepEqual(r.items.map(i => [i.id, i.category]), [["1001", "spam"], ["1002", null]]);
  assert.deepEqual(r.ignored.map(x => x.why), ["id", "category"]);
});

test("a removal reads logins and ids, digits as both", () => {
  const r = parseRemoval({ names: ["@Some_Bot", " 12345 ", "bad name!", 7, "x".repeat(30)], issue: 42, by: "aaskjer" });
  assert.deepEqual(r.ids, ["12345"]);
  assert.deepEqual(r.logins, ["some_bot", "12345"]);
  assert.deepEqual(r.unreadable, ["bad name!", "7", "x".repeat(30)]);
  assert.equal(r.issue, 42);
  assert.equal(r.by, "aaskjer");
  assert.equal(parseRemoval({ names: ["a"], issue: -1, by: "<script>" }).by, null);
  assert.equal(parseRemoval({ names: ["a"], issue: -1 }).issue, null);
  assert.match(parseRemoval({ names: [] }).error, /empty/);
});

test("reporters count per network: IPv4 /24, IPv6 /48", () => {
  assert.equal(networkOf("198.51.100.7"), "v4:198.51.100");
  assert.equal(networkOf("198.51.100.250"), "v4:198.51.100");
  assert.equal(networkOf("256.1.1.1"), null);
  assert.equal(networkOf("2001:db8:abcd:12::1"), "v6:2001:db8:abcd");
  assert.equal(networkOf("2001:0db8:abcd:0012:0000:0000:0000:0001"), "v6:2001:db8:abcd");
  assert.equal(networkOf("2001:db8::"), "v6:2001:db8:0");
  assert.equal(networkOf("::ffff:198.51.100.9"), "v4:198.51.100");
  assert.equal(networkOf("fe80::1%eth0"), "v6:fe80:0:0");
  assert.equal(networkOf("1:2:3:4:5:6:7:8:9"), null);
  assert.equal(networkOf("1::2::3"), null);
  assert.equal(networkOf(""), null);
  assert.equal(networkOf(null), null);
});

test("hashes depend on salt and kind, and never show the input", async () => {
  const a = await hashKey("salt", "net", "v4:1.2.3");
  assert.match(a, /^[0-9a-f]{32}$/);
  assert.notEqual(a, await hashKey("other", "net", "v4:1.2.3"));
  assert.notEqual(a, await hashKey("salt", "install", "v4:1.2.3"));
  assert.equal(a, await hashKey("salt", "net", "v4:1.2.3"));
});

test("the removal key is compared in full", () => {
  assert.ok(constantTimeEqual("Bearer abc", "Bearer abc"));
  assert.ok(!constantTimeEqual("Bearer abc", "Bearer abd"));
  assert.ok(!constantTimeEqual("Bearer ab", "Bearer abc"));
  assert.ok(!constantTimeEqual(null, "x"));
});

test("Twitch decides who may be listed", () => {
  assert.equal(verdictOf(undefined), "gone");
  assert.equal(verdictOf({ login: "a", type: "", broadcaster_type: "" }), "ok");
  assert.equal(verdictOf({ login: "a", type: "", broadcaster_type: "affiliate" }), "protected");
  assert.equal(verdictOf({ login: "a", type: "", broadcaster_type: "partner" }), "protected");
  assert.equal(verdictOf({ login: "a", type: "staff", broadcaster_type: "" }), "protected");
  assert.equal(verdictOf({ login: "StreamElements", type: "", broadcaster_type: "" }), "protected");
});

test("one reporter lists an account, a removed one needs three fresh ones", () => {
  assert.ok(!isPublishable(0, false));
  assert.ok(isPublishable(1, false));
  assert.ok(!isPublishable(2, true));
  assert.ok(isPublishable(3, true));
});

test("the diff names adds, changes and removals, in a stable order", () => {
  const prev = [
    { category: "spam", id: "2", login: "b", reports: 1, first_at: 10 },
    { category: "spam", id: "10", login: "c", reports: 2, first_at: 10 },
    { category: "lurkbot", id: "3", login: "d", reports: 1, first_at: 10 },
    { category: "spam", id: "4", login: "e", reports: 1, first_at: 10 },
  ];
  const next = [
    { category: "spam", id: "2", login: "b", reports: 2 },
    { category: "spam", id: "10", login: "c2", reports: 2 },
    { category: "spam", id: "4", login: "e", reports: 1 },
    { category: "botwave", id: "9", login: "w", reports: 1 },
  ];
  const events = diff(prev, next, row => "why-" + row.id);
  assert.deepEqual(events, [
    { op: "add", category: "botwave", id: "9", login: "w", reports: 1 },
    { op: "update", category: "spam", id: "2", login: "b", reports: 2 },
    { op: "update", category: "spam", id: "10", login: "c2", reports: 2 },
    { op: "remove", category: "lurkbot", id: "3", why: "why-3" },
  ]);
  assert.deepEqual(diff(prev, prev, () => "x"), []);
});

test("why an account left the list", () => {
  const row = { first_at: 100 };
  assert.equal(whyGoneOf(undefined, row), "dropped");
  assert.equal(whyGoneOf({ status: "ok", removed_at: 150 }, row), "removed");
  assert.equal(whyGoneOf({ status: "ok", removed_at: 100 }, row), "removed");
  assert.equal(whyGoneOf({ status: "ok", removed_at: 50 }, row), "dropped");
  assert.equal(whyGoneOf({ status: "gone", removed_at: null }, row), "gone");
  assert.equal(whyGoneOf({ status: "protected", removed_at: null }, row), "protected");
  assert.equal(whyGoneOf({ status: "ok", removed_at: null }, row), "dropped");
});

test("ids sort as numbers", () => {
  assert.deepEqual(["10", "9", "100", "11"].sort(compareIds), ["9", "10", "11", "100"]);
});

test("logins are normalised or refused", () => {
  assert.equal(normaliseLogin(" @Foo_Bar "), "foo_bar");
  assert.equal(normaliseLogin("a".repeat(26)), null);
  assert.equal(normaliseLogin("foo-bar"), null);
  assert.equal(normaliseLogin(5), null);
});

test("the branch files: one list per category, txt only from banFrom, change log and removals", () => {
  const now = Date.UTC(2026, 9, 8, 12, 0, 0) / 1000;
  const files = buildFiles({
    version: 7, now, changesSince: 3, repo: "aaskjer/TwitchSentry", form: "botlist-removal.yml",
    published: [
      { category: "spam", id: "2", login: "zed", reports: 2, first_at: now - 86400, last_at: now, reasons: "spam_domain,keyword" },
      { category: "spam", id: "1", login: "alpha", reports: 1, first_at: now, last_at: now, reasons: "keyword" },
      { category: "lurkbot", id: "5", login: "lurk_one", reports: 3, first_at: now, last_at: now, reasons: "known_day" },
    ],
    events: [
      { version: 6, at: now - 60, op: "add", category: "spam", id: "1", login: "alpha", reports: 1, why: null },
      { version: 7, at: now, op: "remove", category: "botwave", id: "8", login: null, reports: null, why: "removed" },
    ],
    removals: [{ account_id: "8", at: now }],
  });
  assert.deepEqual(Object.keys(files).sort(), [
    "README.md", "botwaves.json", "botwaves.txt", "changes.json", "index.json", "lurkbots.json", "lurkbots.txt",
    "removed.json", "spam.json", "spam.txt",
  ]);
  const spam = JSON.parse(files["spam.json"]);
  assert.equal(spam.version, 7);
  assert.equal(spam.banFrom, LIMITS.banFrom);
  assert.deepEqual(spam.accounts, [
    { id: "1", login: "alpha", reports: 1, first: "2026-10-08", last: "2026-10-08", reasons: ["keyword"] },
    { id: "2", login: "zed", reports: 2, first: "2026-10-07", last: "2026-10-08", reasons: ["keyword", "spam_domain"] },
  ]);
  assert.equal(files["spam.txt"], "zed\n");
  assert.equal(files["lurkbots.txt"], "lurk_one\n");
  assert.equal(files["botwaves.txt"], "");
  assert.deepEqual(JSON.parse(files["botwaves.json"]).accounts, []);
  const changes = JSON.parse(files["changes.json"]);
  assert.equal(changes.since, 3);
  assert.deepEqual(changes.changes, [
    { v: 6, at: "2026-10-08T11:59:00Z", op: "add", category: "spam", id: "1", login: "alpha", reports: 1 },
    { v: 7, at: "2026-10-08T12:00:00Z", op: "remove", category: "botwave", id: "8", why: "removed" },
  ]);
  assert.deepEqual(JSON.parse(files["removed.json"]).removed, [{ id: "8", at: "2026-10-08" }]);
  const index = JSON.parse(files["index.json"]);
  assert.deepEqual(index.lists.spam, { file: "spam.json", text: "spam.txt", count: 2, confirmed: 1 });
  assert.equal(index.updated, "2026-10-08T12:00:00Z");
  assert.match(files["README.md"], /issues\/new\?template=botlist-removal\.yml/);
  assert.match(files["README.md"], /CC0 1\.0/);
  for (const [name, text] of Object.entries(files)) if (text) assert.ok(text.endsWith("\n"), name + " ends with a newline");
});
