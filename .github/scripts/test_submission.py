"""Tests for submission.py.

    python -m unittest discover -s .github/scripts

The tickets here are rendered the way GitHub renders an issue form - a heading per field, the value
under it, "_No response_" for an empty one - and the workflow's calls to git and gh are recorded
rather than made, so nothing touches GitHub.
"""

import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import submission as s  # noqa: E402

REPO_ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
TEMPLATES = {
    "spam": os.path.join(REPO_ROOT, ".github", "ISSUE_TEMPLATE", "share-spam-list.yml"),
    "profile": os.path.join(REPO_ROOT, ".github", "ISSUE_TEMPLATE", "share-profile.yml"),
    "translation": os.path.join(REPO_ROOT, ".github", "ISSUE_TEMPLATE", "share-translation.yml"),
}
LABEL = {"spam": "share: spam list", "profile": "share: profile", "translation": "share: translation"}
TICKED = "- [X] Nothing above is a chat message, a username, or anything else that identifies a person."


def render(pairs):
    return "\n\n".join("### %s\n\n%s" % (label, value if value else "_No response_") for label, value in pairs)


def ticket(kind, pairs, number=42, state="open"):
    return {"number": number, "state": state, "body": render(pairs), "labels": [{"name": LABEL[kind]}],
            "user": {"login": "somestreamer"}, "created_at": "2026-09-14T12:00:00Z"}


def workspace(feed=None, en=None):
    root = tempfile.mkdtemp(prefix="ts-submission-")
    os.makedirs(os.path.join(root, "Feed"))
    os.makedirs(os.path.join(root, "Language"))
    with open(os.path.join(root, "Feed", "spam.json"), "w", encoding="utf-8") as f:
        json.dump(feed or {"schema": 1, "version": 1, "lists": {"spamDomains": ["smmgen"]}, "retracted": {}}, f)
    with open(os.path.join(root, "Language", "index.json"), "w", encoding="utf-8") as f:
        json.dump([{"code": "en", "name": "English"}, {"code": "de", "name": "Deutsch"},
                   {"code": "pt-BR", "name": "Portugu\u00eas (Brasil)"}], f)
    with open(os.path.join(root, "Language", "en.json"), "w", encoding="utf-8") as f:
        json.dump(en if en is not None else {"Save": "Save"}, f)
    return root


def spam_pairs(entries, context="", version="v2.1.0", privacy=TICKED):
    return [("Entries", entries), ("Where did it show up?", context), ("TwitchSentry version", version),
            ("Before you submit", privacy)]


def profile_pairs(name="Small chat, strict links", purpose="For small English chats.", settings=None, raw=None,
                  privacy="- [X] The profile came from TwitchSentry's own export and holds no key, webhook or list of people."):
    if raw is None:
        export = {"twitchSentryProfile": 1, "name": name, "created": "2026-09-14T10:00:00Z", "twitchSentry": "v2.1.0",
                  "settings": settings if settings is not None else {"spamScoreThreshold": 1.0, "discordWebhookEnabled": True,
                                                                     "timeoutDurationSeconds": 300, "autoModCategories": []}}
        raw = json.dumps(export, indent=2)
    return [("Profile name", name), ("What is it for?", purpose), ("Profile file", "```json\n%s\n```" % raw),
            ("Before you submit", privacy)]


def translation_pairs(language="Deutsch (de)", english="Save", current="Speichern!", suggestion="Speichern", why=""):
    return [("Language", language), ("The English text", english), ("What it says now", current),
            ("What it should say", suggestion), ("Why is it better?", why)]


class TemplatesMatchTheScript(unittest.TestCase):
    def test_every_heading_the_script_reads_is_a_label_in_its_form(self):
        for kind, path in TEMPLATES.items():
            with open(path, encoding="utf-8") as f:
                text = f.read()
            labels = set(re.findall(r"^\s+(?:- )?label:\s*(.+?)\s*$", text, re.M))
            for _, label in s.FIELDS[kind]:
                self.assertIn(label, labels, "%s has no field labelled %r" % (os.path.basename(path), label))

    def test_every_form_carries_the_label_the_workflow_routes_on(self):
        with open(os.path.join(REPO_ROOT, ".github", "workflows", "community-submissions.yml"), encoding="utf-8") as f:
            workflow = f.read()
        for kind, path in TEMPLATES.items():
            with open(path, encoding="utf-8") as f:
                text = f.read()
            self.assertRegex(text, r'(?m)^labels:\s*\["%s"\]\s*$' % re.escape(LABEL[kind]))
            self.assertEqual(s.KIND_BY_LABEL[LABEL[kind]], kind)
            self.assertIn("'%s'" % LABEL[kind], workflow)

    def test_the_workflow_closes_tickets_for_the_branch_the_script_opens_pull_requests_into(self):
        with open(os.path.join(REPO_ROOT, ".github", "workflows", "community-submissions.yml"), encoding="utf-8") as f:
            workflow = f.read()
        self.assertIn("branches: [%s]" % s.SUBMISSION_BRANCH, workflow)
        self.assertIn("github.event.pull_request.base.ref == '%s'" % s.SUBMISSION_BRANCH, workflow)
        self.assertIn("startsWith(github.event.pull_request.head.ref, 'submission/')", workflow)
        self.assertTrue(s.TICKET_BRANCH.match("submission/42"))

    def test_the_language_dropdown_offers_exactly_the_published_languages(self):
        with open(TEMPLATES["translation"], encoding="utf-8") as f:
            text = f.read()
        offered = re.findall(r"^\s+- .*\(([A-Za-z-]+)\)\s*$", text, re.M)
        with open(os.path.join(REPO_ROOT, "Language", "index.json"), encoding="utf-8-sig") as f:
            index = json.load(f)
        self.assertEqual(sorted(offered), sorted(e["code"] for e in index))


class ReadingTheTicket(unittest.TestCase):
    def test_values_come_from_under_their_headings(self):
        values = s.parse_form(render(spam_pairs("spamDomains: smmgen")), s.FIELDS["spam"])
        self.assertEqual(values["entries"], "spamDomains: smmgen")
        self.assertEqual(values["context"], "")
        self.assertEqual(values["version"], "v2.1.0")
        self.assertTrue(s.is_checked(values["privacy"]))

    def test_a_missing_heading_reads_as_none(self):
        values = s.parse_form("### Entries\n\nspamDomains: smmgen", s.FIELDS["spam"])
        self.assertIsNone(values["version"])

    def test_windows_line_endings_are_read_the_same(self):
        values = s.parse_form(render(spam_pairs("a: b\nc: d")).replace("\n", "\r\n"), s.FIELDS["spam"])
        self.assertEqual(values["entries"], "a: b\nc: d")

    def test_a_json_textarea_loses_its_fence(self):
        self.assertEqual(s.unfence("```json\n{\"a\": 1}\n```"), "{\"a\": 1}")

    def test_a_fence_outlasts_every_backtick_run_inside_it(self):
        fenced = s.fence("x ```` y")
        self.assertTrue(fenced.startswith("````` text\n"))
        self.assertTrue(fenced.rstrip("\n").endswith("`````"))


class SpamWording(unittest.TestCase):
    def setUp(self):
        self.root = workspace({"schema": 1, "version": 2,
                               "lists": {"spamDomains": ["smmgen"], "strongKeywords": ["botrush"]},
                               "retracted": {"keywords": ["old offer"]},
                               "shipped": {"releases": ["v1.0.1", "v2.0.0"],
                                           "lists": {"keywords": ["cheap"], "spamDomains": ["streamboo"]}}})

    def build(self, entries, **kw):
        return s.build("spam", ticket("spam", spam_pairs(entries, **kw)), self.root)

    def test_entries_are_stored_the_way_installs_store_them(self):
        r = self.build("spamDomains: NewSite\nhandoffPhrases:  !add me on discord \nhandoffphrases: add me on discord\n\n"
                       "keywords: old offer | users=4 clean=0")
        self.assertEqual(r.problems, [])
        self.assertEqual(r.document["entries"], {"keywords": ["old offer"], "spamDomains": ["newsite"],
                                                 "handoffPhrases": ["add me on discord"]})
        self.assertEqual(r.document["counts"], {"keywords": {"old offer": {"users": 4, "clean": 0}}})
        self.assertEqual(r.document["twitchSentry"], "v2.1.0")
        self.assertEqual(r.path, "spam/42.json")
        self.assertEqual(r.title, "Spam wording from #42 (3 entries)")

    def test_entries_already_in_the_feed_are_left_out(self):
        r = self.build("spamDomains: smmgen\nspamDomains: newsite")
        self.assertEqual(r.document["entries"], {"spamDomains": ["newsite"]})
        self.assertIn("Already in the feed", r.summary)

    def test_nothing_new_opens_no_pull_request(self):
        r = self.build("spamDomains: smmgen\nstrongKeywords: BotRush")
        self.assertIsNone(r.document)
        self.assertEqual(r.nothing_new, {"spamDomains": ["smmgen"], "strongKeywords": ["botrush"]})

    def test_defaults_a_release_shipped_are_left_out(self):
        # An install that started on an older version still carries that version's defaults, so the
        # window may offer one; the feed could never hand it over.
        r = self.build("keywords: !Cheap\nspamDomains: streamboo\nspamDomains: newsite")
        self.assertEqual(r.document["entries"], {"spamDomains": ["newsite"]})
        self.assertIn("| `keywords` | 0 | 0 | 1 |", r.summary)
        self.assertIn("Built-in defaults of a TwitchSentry release", r.summary)
        self.assertIn("spamDomains: streamboo\nkeywords: cheap", r.summary)
        self.assertIn("and the defaults releases shipped", r.summary)

    def test_a_default_is_not_a_default_in_another_list(self):
        r = self.build("strongKeywords: cheap")
        self.assertEqual(r.document["entries"], {"strongKeywords": ["cheap"]})

    def test_nothing_but_known_entries_and_defaults_opens_no_pull_request(self):
        r = self.build("spamDomains: smmgen\nkeywords: cheap")
        self.assertIsNone(r.document)
        self.assertEqual(r.nothing_new, {"spamDomains": ["smmgen"]})
        self.assertEqual(r.already_shipped, {"keywords": ["cheap"]})

    def test_a_feed_without_the_shipped_block_is_not_claimed_to_be_checked(self):
        r = s.build("spam", ticket("spam", spam_pairs("spamDomains: newsite")), workspace())
        self.assertIn("has no `shipped` block yet", r.summary)
        self.assertNotIn("and the defaults releases shipped", r.summary)

    def test_an_entry_retracted_before_is_kept_and_pointed_out(self):
        r = self.build("keywords: old offer")
        self.assertEqual(r.document["entries"], {"keywords": ["old offer"]})
        self.assertIn("Retracted from the feed before", r.summary)

    def test_mistakes_are_reported_by_line_and_nothing_is_built(self):
        r = self.build("spamDomains: smm gen\nnot a list line\ncustomPatterns: (a+)+$\nstrongKeywords: bot")
        self.assertIsNone(r.document)
        self.assertEqual(len(r.problems), 4)
        self.assertTrue(r.problems[0].startswith("Line 1: `smm gen` is not a bare site name"))
        self.assertIn("Line 2 is not written as `list: entry`", r.problems[1])
        self.assertIn("Line 3: `customPatterns` is not one of the lists", r.problems[2])
        self.assertIn("Line 4: `bot` is shorter than 4 characters", r.problems[3])

    def test_the_privacy_box_has_to_be_ticked(self):
        r = self.build("spamDomains: newsite", privacy="- [ ] Nothing above is a chat message")
        self.assertTrue(any("not ticked" in p for p in r.problems))

    def test_too_many_entries_in_one_ticket(self):
        r = self.build("\n".join("keywords: filler phrase %d" % i for i in range(s.MAX_ENTRIES + 1)))
        self.assertTrue(any("one ticket takes up to" in p for p in r.problems))

    def test_quoted_text_cannot_break_out_of_its_code_span(self):
        r = self.build("spamDomains: bad`site")
        self.assertIn("`bad'site`", r.problems[0])

    def test_the_context_goes_into_a_fence(self):
        r = self.build("spamDomains: newsite", context="raid ``` @someone")
        self.assertIn("```` text\nraid ``` @someone\n````", r.summary)


class Profiles(unittest.TestCase):
    def setUp(self):
        self.root = workspace()

    def build(self, **kw):
        return s.build("profile", ticket("profile", profile_pairs(**kw)), self.root)

    def test_an_export_is_accepted_and_only_its_known_parts_are_kept(self):
        r = self.build()
        self.assertEqual(r.problems, [])
        self.assertEqual(r.document, {"twitchSentryProfile": 1, "name": "Small chat, strict links", "twitchSentry": "v2.1.0",
                                      "purpose": "For small English chats.", "issue": 42, "submittedBy": "somestreamer",
                                      "submittedAt": "2026-09-14T12:00:00Z",
                                      "settings": {"spamScoreThreshold": 1.0, "discordWebhookEnabled": True,
                                                   "timeoutDurationSeconds": 300, "autoModCategories": []}})
        self.assertEqual(r.path, "42.json")

    def test_the_stored_file_is_a_profile_the_window_imports_as_it_is(self):
        # ReadProfileFile wants the marker, a settings object and a name, and passes over everything else.
        document = self.build().document
        self.assertEqual(document["twitchSentryProfile"], 1)
        self.assertIsInstance(document["settings"], dict)
        self.assertEqual(document["name"], "Small chat, strict links")
        self.assertEqual(list(document)[0], "twitchSentryProfile")

    def test_the_custom_slider_stops_an_export_carries_are_accepted(self):
        # The four Dictionary<string, double> settings. Ticket #9, the first profile shared for real, was
        # turned away over exactly these, empty or filled.
        r = self.build(settings={"mgCustomPreset": {"mgScoreThreshold": 0.8, "mgMinAccountAgeDays": 14.0},
                                 "rfCustomPreset": {}, "fgCustomPreset": {"fgScoreThreshold": 2},
                                 "spamCustomPreset": {"spamScoreThreshold": 1.75}})
        self.assertEqual(r.problems, [])

    def test_a_custom_slider_stop_holding_anything_but_numbers_is_turned_away(self):
        for value in ({"mgScoreThreshold": "high"}, {"mgScoreThreshold": True}, {"mgScoreThreshold": {"x": 1}},
                      {"not a name": 1}, [0.8], "0.8"):
            r = self.build(settings={"mgCustomPreset": value})
            self.assertTrue(any("`mgCustomPreset` holds a value no setting has" in p for p in r.problems), value)

    def test_a_number_map_on_any_other_setting_is_turned_away(self):
        r = self.build(settings={"mgScoreThreshold": {"mgScoreThreshold": 0.8}})
        self.assertTrue(any("holds a value no setting has" in p for p in r.problems))

    def test_a_setting_a_profile_never_carries_is_turned_away(self):
        r = self.build(settings={"discordWebhookUrl": "https://discord.com/api/webhooks/1/abc"})
        self.assertTrue(any("`discordWebhookUrl`" in p for p in r.problems))

    def test_the_feed_switch_never_travels_in_a_profile(self):
        r = self.build(settings={"spamFeedEnabled": False})
        self.assertTrue(any("`spamFeedEnabled`" in p for p in r.problems))

    def test_a_text_setting_named_like_a_secret_is_turned_away(self):
        r = self.build(settings={"twitchToken": "abc"})
        self.assertTrue(any("`twitchToken`" in p for p in r.problems))

    def test_a_webhook_address_anywhere_is_turned_away(self):
        r = self.build(settings={"someMessage": "see discordapp.com/api/webhooks/1/abc"})
        self.assertTrue(any("does not belong in a shared profile" in p for p in r.problems))

    def test_a_value_no_setting_has_is_turned_away(self):
        r = self.build(settings={"spamScoreThreshold": {"nested": 1}})
        self.assertTrue(any("holds a value no setting has" in p for p in r.problems))

    def test_a_key_twice_is_not_a_profile(self):
        raw = '{"twitchSentryProfile": 1, "settings": {"a": 1, "a": 2}}'
        r = self.build(raw=raw)
        self.assertTrue(any("not valid JSON" in p for p in r.problems))

    def test_something_that_is_not_an_export(self):
        r = self.build(raw='{"spamScoreThreshold": 1.0}')
        self.assertTrue(any("not a TwitchSentry profile" in p for p in r.problems))

    def test_the_built_in_stance_names_are_taken(self):
        r = self.build(name="under attack")
        self.assertTrue(any("built-in stances" in p for p in r.problems))

    def test_a_name_that_cannot_be_a_file_name(self):
        r = self.build(name="a/b")
        self.assertTrue(any("file name cannot" in p for p in r.problems))


class Translations(unittest.TestCase):
    def setUp(self):
        self.root = workspace(en={"Save": "Save"})

    def build(self, **kw):
        return s.build("translation", ticket("translation", translation_pairs(**kw)), self.root)

    def test_a_fix_is_accepted(self):
        r = self.build()
        self.assertEqual(r.problems, [])
        self.assertEqual(r.document["language"], "de")
        self.assertEqual(r.document["suggestion"], "Speichern")
        self.assertIn("is in the published", r.summary)
        self.assertEqual(r.path, "translations/42.json")

    def test_english_is_a_language_like_the_others(self):
        r = self.build(language="English (en)", english="Save", current="Save", suggestion="Save changes")
        self.assertEqual(r.problems, [])
        self.assertEqual(r.document["language"], "en")
        self.assertEqual(r.title, "Translation (en) from #42")

    def test_a_language_with_brackets_in_its_name(self):
        r = self.build(language="Portugu\u00eas (Brasil) (pt-BR)", current="Salvar!", suggestion="Salvar")
        self.assertEqual(r.document["language"], "pt-BR")

    def test_english_the_published_file_does_not_have_is_pointed_out(self):
        r = self.build(english="A newer string")
        self.assertIn("**not** in the published", r.summary)

    def test_a_language_twitchsentry_does_not_have(self):
        r = self.build(language="Nederlands (nl)")
        self.assertTrue(any("languages TwitchSentry has" in p for p in r.problems))

    def test_a_suggestion_that_changes_nothing(self):
        r = self.build(current="Speichern", suggestion="Speichern")
        self.assertTrue(any("same as what it says now" in p for p in r.problems))

    def test_an_invisible_character_in_the_suggestion(self):
        r = self.build(suggestion="Spei\u200bchern")
        self.assertTrue(any("invisible character" in p for p in r.problems))


class AwkwardCharacters(unittest.TestCase):
    def test_a_lone_surrogate_in_an_entry_is_refused_not_thrown(self):
        self.assertIsNotNone(s.entry_problem("keywords", chr(0xD835) + " viewers"))

    def test_a_lone_surrogate_anywhere_in_the_ticket_cannot_stop_the_file_being_written(self):
        issue = ticket("spam", spam_pairs("spamDomains: newsite", context="raid " + chr(0xDC00) + " wave"))
        r = s.build("spam", issue, workspace())
        self.assertEqual(r.problems, [])
        json.dumps(r.document, ensure_ascii=False).encode("utf-8")


class ATicketWithoutItsForm(unittest.TestCase):
    def test_edited_away_headings_are_reported(self):
        issue = ticket("spam", spam_pairs("spamDomains: newsite"))
        issue["body"] = "spamDomains: newsite"
        r = s.build("spam", issue, workspace())
        self.assertTrue(r.problems and "no longer has the form's parts" in r.problems[0])


class Recorder:
    """Stands in for subprocess: records every call and answers from a script of responses.

    An answer is (code, stdout) or (code, stdout, stderr). One given as a list is used up one call at a
    time, and its last entry answers every call after."""

    def __init__(self, answers):
        self.calls = []
        self.dirs = []
        self.answers = answers

    def __call__(self, args, check=True, cwd=None):
        self.calls.append(list(args))
        self.dirs.append(cwd)
        key = " ".join(args[:3])
        code, out, err = 0, "", ""
        for prefix, answer in self.answers:
            if key.startswith(prefix):
                if isinstance(answer, list):
                    answer = answer.pop(0) if len(answer) > 1 else answer[0]
                code, out = answer[0], answer[1]
                err = answer[2] if len(answer) > 2 else ""
                break
        if check and code != 0:
            raise subprocess.CalledProcessError(code, args, output=out, stderr=err or "failed")
        return subprocess.CompletedProcess(args, code, stdout=out, stderr=err)

    def commands(self):
        return [" ".join(c[:3]) for c in self.calls]


README = s.submissions_readme("aaskjer/TwitchSentry")


class WorkflowHarness(unittest.TestCase):
    """Runs main() on an event, with every call to git and gh recorded instead of made."""

    def run_event(self, event, answers, root=None):
        root = root or workspace()
        handle = tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".json", delete=False)
        with handle:
            json.dump(event, handle)
        recorder = Recorder(answers)
        env = {"GITHUB_EVENT_PATH": handle.name, "GITHUB_REPOSITORY": "aaskjer/TwitchSentry", "GITHUB_WORKSPACE": root}
        with mock.patch.dict(os.environ, env), mock.patch.object(s, "run", recorder), \
                mock.patch("sys.stdout"), mock.patch("sys.stderr"):
            code = s.main()
        return code, recorder, root

    def run_main(self, issue, answers, root=None):
        return self.run_event({"issue": issue, "repository": {"default_branch": "main"}}, answers, root)

    def worktrees(self, rec):
        return [c[4] for c in rec.calls if c[:3] == ["git", "worktree", "add"]]


class TheWorkflowRun(WorkflowHarness):
    def test_a_new_ticket_becomes_a_file_in_a_pull_request_into_the_submissions_branch(self):
        issue = ticket("spam", spam_pairs("spamDomains: newsite"))
        code, rec, root = self.run_main(issue, [
            ("git fetch origin", [(0, ""), (1, "")]),
            ("git show origin/submissions:README.md", (0, README)),
            ("gh pr list", (0, "[]")),
            ("gh pr create", (0, "https://github.com/aaskjer/TwitchSentry/pull/7\n")),
        ])
        self.assertEqual(code, 0)
        self.assertEqual(rec.commands(), [
            "git fetch origin", "git show origin/submissions:README.md", "git fetch origin", "git worktree add",
            "git add --all", "git -c user.name=github-actions[bot]", "git push --force", "git worktree remove",
            "gh pr list", "gh pr create", "gh issue comment"])
        self.assertIn("+refs/heads/submissions:refs/remotes/origin/submissions", rec.calls[0])
        self.assertIn("+refs/heads/submission/42:refs/remotes/origin/submission/42", rec.calls[2])
        self.assertEqual(rec.calls[3][-1], "refs/remotes/origin/submissions", "the branch starts from submissions, not from main")
        self.assertEqual(rec.calls[5][-2:], ["-m", "Add submission #42 (spam) from somestreamer"])
        self.assertEqual(rec.calls[6][-1], "HEAD:refs/heads/submission/42")
        work = self.worktrees(rec)[0]
        self.assertEqual(rec.dirs[6], work, "the push goes out from the worktree")
        with open(os.path.join(work, "spam", "42.json"), encoding="utf-8") as f:
            self.assertEqual(json.load(f)["entries"], {"spamDomains": ["newsite"]})
        self.assertEqual(sorted(os.listdir(root)), ["Feed", "Language"], "main's checkout is left as it was")

        created = rec.calls[9]
        self.assertEqual(created[created.index("--base") + 1], "submissions")
        with open(created[created.index("--body-file") + 1], encoding="utf-8") as f:
            body = f.read()
        self.assertTrue(body.startswith("Merging this accepts the submission and closes #42.\n"))
        self.assertNotIn("Closes #", body, "GitHub ignores it outside main, so it would promise what never happens")

    def test_the_first_submission_starts_the_branch_with_its_front_page(self):
        issue = ticket("translation", translation_pairs())
        _, rec, _ = self.run_main(issue, [
            ("git fetch origin", [(128, ""), (0, ""), (0, ""), (1, "")]),
            ("git -c user.name=github-actions[bot]", (0, "0123abcd\n")),
            ("git show origin/submissions:README.md", (128, "")),
            ("gh pr list", (0, "[]")),
            ("gh pr create", (0, "https://github.com/aaskjer/TwitchSentry/pull/8\n")),
        ], workspace(en={"Save": "Save"}))
        self.assertEqual(rec.commands(), [
            "git fetch origin", "git -c user.name=github-actions[bot]", "git push origin",
            "git fetch origin", "git show origin/submissions:README.md", "git worktree add", "git add --all",
            "git -c user.name=github-actions[bot]", "git push origin", "git worktree remove",
            "git fetch origin", "git fetch origin", "git worktree add", "git add --all", "git -c user.name=github-actions[bot]",
            "git push --force", "git worktree remove", "gh pr list", "gh pr create", "gh issue comment"])
        self.assertIn("commit-tree", rec.calls[1])
        self.assertIn(s.EMPTY_TREE, rec.calls[1], "it shares nothing with main")
        self.assertEqual(rec.calls[2][-1], "0123abcd:refs/heads/submissions")
        self.assertEqual(rec.calls[7][-2:], ["-m", "Describe the submissions branch"])
        self.assertEqual(rec.calls[8][-1], "HEAD:refs/heads/submissions")
        self.assertIn("+refs/heads/submissions:refs/remotes/origin/submissions", rec.calls[10],
                      "fetched again, so the pull request's branch starts from the front page just pushed")
        self.assertIn("+refs/heads/submission/42:refs/remotes/origin/submission/42", rec.calls[11])
        front, pull = self.worktrees(rec)
        self.assertEqual(os.listdir(front), ["README.md"], "the front page goes onto the branch by itself, not into a pull request")
        with open(os.path.join(front, "README.md"), encoding="utf-8") as f:
            self.assertEqual(f.read(), README)
        self.assertEqual(os.listdir(pull), ["translations"])

    def test_a_front_page_worded_differently_is_written_again_first(self):
        issue = ticket("spam", spam_pairs("spamDomains: newsite"))
        _, rec, _ = self.run_main(issue, [
            ("git fetch origin", [(0, ""), (0, ""), (1, "")]),
            ("git show origin/submissions:README.md", (0, "# Submissions\n\nOlder wording.\n")),
            ("gh pr list", (0, "[]")),
            ("gh pr create", (0, "https://example/pull/7")),
        ])
        self.assertEqual(rec.commands()[:8], [
            "git fetch origin", "git show origin/submissions:README.md", "git worktree add", "git add --all",
            "git -c user.name=github-actions[bot]", "git push origin", "git worktree remove", "git fetch origin"])
        self.assertEqual(rec.calls[4][-2:], ["-m", "Describe the submissions branch"])
        self.assertEqual(rec.commands()[-2:], ["gh pr create", "gh issue comment"])

    def test_a_submissions_branch_github_will_not_take_opens_no_pull_request(self):
        issue = ticket("spam", spam_pairs("spamDomains: newsite"))
        code, rec, _ = self.run_main(issue, [
            ("git fetch origin", (128, "")),
            ("git -c user.name=github-actions[bot]", (0, "0123abcd\n")),
            ("git push origin", (1, "", "remote: error: GH013: Repository rule violations found for refs/heads/submissions.")),
        ])
        self.assertEqual(code, 1)
        self.assertEqual(rec.commands().count("git push origin"), 1, "a rule does not change by asking again")
        self.assertFalse(any(c[:2] == ["gh", "pr"] for c in rec.calls))
        with open(rec.calls[-1][rec.calls[-1].index("--body-file") + 1], encoding="utf-8") as f:
            self.assertIn("Something went wrong turning this ticket into a pull request", f.read())

    def test_no_call_carries_the_ticket_text_on_its_command_line(self):
        issue = ticket("spam", spam_pairs("spamDomains: newsite", context="$(rm -rf /) `whoami`"))
        _, rec, _ = self.run_main(issue, [("git fetch origin", [(0, ""), (1, "")]),
                                          ("git show origin/submissions:README.md", (0, README)),
                                          ("gh pr list", (0, "[]")), ("gh pr create", (0, "https://example/pull/7"))])
        self.assertIn("gh pr create", rec.commands())
        for call in rec.calls:
            self.assertFalse(any("rm -rf" in part or "whoami" in part for part in call), call)

    def test_an_edit_that_changes_nothing_pushes_nothing_and_says_nothing(self):
        issue = ticket("spam", spam_pairs("spamDomains: newsite"))
        root = workspace()
        result = s.build("spam", issue, root)
        content = json.dumps(result.document, ensure_ascii=False, indent=2) + "\n"
        _, rec, _ = self.run_main(issue, [
            ("git fetch origin", (0, "")),
            ("git show origin/submissions:README.md", (0, README)),
            ("git show origin/submission/42:spam/42.json", (0, content)),
            ("gh pr list", (0, '[{"number": 7, "url": "https://github.com/aaskjer/TwitchSentry/pull/7"}]')),
        ], root)
        self.assertEqual(rec.commands(), ["git fetch origin", "git show origin/submissions:README.md", "git fetch origin",
                                          "git show origin/submission/42:spam/42.json", "gh pr list", "gh pr edit"])
        self.assertEqual(rec.calls[-1][3], "7")

    def test_a_ticket_the_feed_can_add_nothing_from_only_gets_a_comment_saying_why(self):
        root = workspace({"schema": 1, "version": 2, "lists": {"spamDomains": ["smmgen"]}, "retracted": {},
                          "shipped": {"releases": ["v2.0.0"], "lists": {"keywords": ["cheap"]}}})
        issue = ticket("spam", spam_pairs("spamDomains: smmgen\nkeywords: cheap"))
        code, rec, _ = self.run_main(issue, [], root)
        self.assertEqual(code, 0)
        self.assertEqual(rec.commands(), ["gh issue comment"])
        with open(rec.calls[0][rec.calls[0].index("--body-file") + 1], encoding="utf-8") as f:
            body = f.read()
        self.assertIn("Already in the spam feed:\n``` text\nspamDomains: smmgen\n```", body)
        self.assertIn("Built-in defaults of a TwitchSentry release", body)
        self.assertIn("``` text\nkeywords: cheap\n```", body)

    def test_a_ticket_with_mistakes_only_gets_a_comment(self):
        issue = ticket("spam", spam_pairs("spamDomains: smm gen"))
        _, rec, _ = self.run_main(issue, [])
        self.assertEqual(rec.commands(), ["gh issue comment"])
        self.assertEqual(rec.calls[0][3], "42")

    def test_closed_tickets_and_other_labels_are_left_alone(self):
        _, rec, _ = self.run_main(ticket("spam", spam_pairs("spamDomains: newsite"), state="closed"), [])
        self.assertEqual(rec.calls, [])
        other = ticket("spam", spam_pairs("spamDomains: newsite"))
        other["labels"] = [{"name": "bug"}]
        _, rec, _ = self.run_main(other, [])
        self.assertEqual(rec.calls, [])

    def test_a_profile_is_committed_to_its_own_branch_and_the_ticket_closed(self):
        issue = ticket("profile", profile_pairs())
        code, rec, _ = self.run_main(issue, [("git fetch origin", (0, "")), ("git show origin/profiles:42.json", (128, ""))])
        self.assertEqual(code, 0)
        self.assertEqual(rec.commands(), [
            "git fetch origin", "git show origin/profiles:42.json", "git worktree add", "git add --all",
            "git -c user.name=github-actions[bot]", "git push origin", "git worktree remove", "gh issue comment", "gh issue close"])
        self.assertFalse(any(c[:2] == ["gh", "pr"] for c in rec.calls), "no pull request, ever")
        self.assertIn("+refs/heads/profiles:refs/remotes/origin/profiles", rec.calls[0])
        self.assertIn("HEAD:refs/heads/profiles", rec.calls[5])
        self.assertEqual(rec.dirs[5], self.worktrees(rec)[0], "the push goes out from the profiles worktree")
        self.assertEqual(rec.calls[-1][-2:], ["--reason", "completed"])

        work = self.worktrees(rec)[0]
        with open(os.path.join(work, "42.json"), encoding="utf-8") as f:
            stored = json.load(f)
        self.assertEqual((stored["twitchSentryProfile"], stored["name"], stored["issue"]), (1, "Small chat, strict links", 42))
        with open(os.path.join(work, "README.md"), encoding="utf-8") as f:
            readme = f.read()
        self.assertIn("| [`Small chat, strict links`](42.json) | [somestreamer](https://github.com/somestreamer) "
                      "| [#42](https://github.com/aaskjer/TwitchSentry/issues/42) | v2.1.0 |", readme)
        self.assertEqual(rec.calls[4][-2:], ["-m", "Store profile #42 from somestreamer"],
                         "the file list shows who shared it beside the file")
        with open(rec.calls[7][rec.calls[7].index("--body-file") + 1], encoding="utf-8") as f:
            body = f.read()
        self.assertIn("https://github.com/aaskjer/TwitchSentry/blob/profiles/42.json", body)
        self.assertIn("https://raw.githubusercontent.com/aaskjer/TwitchSentry/profiles/42.json", body)

    def test_the_first_profile_starts_a_branch_that_shares_nothing_with_main(self):
        issue = ticket("profile", profile_pairs())
        _, rec, _ = self.run_main(issue, [
            ("git fetch origin", [(128, ""), (0, "")]),
            ("git -c user.name=github-actions[bot]", (0, "0123abcd\n")),
            ("git show origin/profiles:42.json", (128, "")),
        ])
        self.assertEqual(rec.commands()[:4], ["git fetch origin", "git -c user.name=github-actions[bot]",
                                              "git push origin", "git fetch origin"])
        self.assertIn("commit-tree", rec.calls[1])
        self.assertIn(s.EMPTY_TREE, rec.calls[1])
        self.assertEqual(rec.calls[2][-1], "0123abcd:refs/heads/profiles")
        self.assertEqual(rec.commands()[-1], "gh issue close")

    def test_a_push_that_loses_a_race_starts_over_from_the_branch_as_it_is(self):
        issue = ticket("profile", profile_pairs())
        code, rec, _ = self.run_main(issue, [("git fetch origin", (0, "")), ("git show origin/profiles:42.json", (128, "")),
                                             ("git push origin", [(1, ""), (0, "")])])
        self.assertEqual(code, 0)
        self.assertEqual(rec.commands().count("git fetch origin"), 2)
        self.assertEqual(rec.commands().count("git worktree remove"), 2, "every worktree is removed, the refused one too")
        self.assertEqual(rec.commands()[-1], "gh issue close")

    def test_a_branch_that_never_holds_still_fails_the_run_and_says_so(self):
        issue = ticket("profile", profile_pairs())
        code, rec, _ = self.run_main(issue, [("git fetch origin", (0, "")), ("git show origin/profiles:42.json", (128, "")),
                                             ("git push origin", (1, ""))])
        self.assertEqual(code, 1)
        self.assertEqual(rec.commands().count("git push origin"), s.PUSH_ATTEMPTS)
        self.assertEqual(rec.commands()[-1], "gh issue comment")
        with open(rec.calls[-1][rec.calls[-1].index("--body-file") + 1], encoding="utf-8") as f:
            self.assertIn("Something went wrong storing this profile", f.read())

    def test_a_push_the_repository_rules_refuse_is_not_retried_and_github_is_quoted(self):
        # What happened to #13 and #14: the ruleset covered every branch with "Restrict updates", so the
        # branch could be created and never written to. The log said the branch kept moving.
        issue = ticket("profile", profile_pairs())
        result = s.build("profile", issue, workspace())
        said = ("remote: error: GH013: Repository rule violations found for refs/heads/profiles.\n"
                "remote: - Cannot update this protected ref.")
        recorder = Recorder([("git fetch origin", (0, "")), ("git show origin/profiles:42.json", (128, "")),
                             ("git push origin", (1, "", said))])
        with mock.patch.object(s, "run", recorder):
            with self.assertRaises(subprocess.CalledProcessError) as caught:
                s.store_profile(result, issue, "aaskjer/TwitchSentry")
        self.assertEqual(recorder.commands().count("git push origin"), 1, "a rule does not change by asking again")
        self.assertIn("GH013", caught.exception.stderr)
        self.assertIn("Cannot update this protected ref", caught.exception.stderr)

    def test_a_ruleset_that_refuses_creating_the_branch_is_quoted_too(self):
        issue = ticket("profile", profile_pairs())
        result = s.build("profile", issue, workspace())
        recorder = Recorder([("git fetch origin", (128, "")), ("git -c user.name=github-actions[bot]", (0, "0123abcd\n")),
                             ("git push origin", (1, "", "remote: error: GH013: Repository rule violations found"))])
        with mock.patch.object(s, "run", recorder):
            with self.assertRaises(subprocess.CalledProcessError) as caught:
                s.store_profile(result, issue, "aaskjer/TwitchSentry")
        self.assertEqual(recorder.commands().count("git push origin"), 1)
        self.assertIn("GH013", caught.exception.stderr)

    def test_an_edit_that_changes_nothing_about_the_profile_writes_nothing(self):
        issue = ticket("profile", profile_pairs())
        stored = json.dumps(s.build("profile", issue, workspace()).document, ensure_ascii=False, indent=2) + "\n"
        _, rec, _ = self.run_main(issue, [("git fetch origin", (0, "")), ("git show origin/profiles:42.json", (0, stored))])
        self.assertEqual(rec.commands(), ["git fetch origin", "git show origin/profiles:42.json"])

    def test_a_profile_with_mistakes_only_gets_a_comment_and_stays_open(self):
        issue = ticket("profile", profile_pairs(settings={"discordWebhookUrl": "https://discord.com/api/webhooks/1/abc"}))
        _, rec, _ = self.run_main(issue, [])
        self.assertEqual(rec.commands(), ["gh issue comment"])
        with open(rec.calls[0][rec.calls[0].index("--body-file") + 1], encoding="utf-8") as f:
            self.assertTrue(f.read().startswith("This profile could not be stored yet:"))

    def test_the_branch_front_page_lists_every_profile_newest_first(self):
        folder = tempfile.mkdtemp(prefix="ts-profiles-test-")
        for number, name, login in ((9, "test", "aaskjer"), (12, "Late night", "night-owl-42"), (10, "odd `name`", None),
                                    (11, "sneaky", "x](https://evil.example)")):
            doc = {"twitchSentryProfile": 1, "name": name, "settings": {}}
            if login is not None:
                doc["submittedBy"] = login
            with open(os.path.join(folder, "%d.json" % number), "w", encoding="utf-8") as f:
                json.dump(doc, f)
        with open(os.path.join(folder, "notes.json"), "w", encoding="utf-8") as f:
            f.write("{}")
        readme = s.profiles_readme(folder, "aaskjer/TwitchSentry")
        rows = [line for line in readme.splitlines() if line.startswith("| [")]
        self.assertEqual([r.split("](")[1].split(")")[0] for r in rows], ["12.json", "11.json", "10.json", "9.json"])
        self.assertIn("[`odd 'name'`](10.json)", readme, "a backtick in a name cannot break out of its code span")
        self.assertIn("| [`Late night`](12.json) | [night-owl-42](https://github.com/night-owl-42) |", readme)
        self.assertIn("| [`test`](9.json) | [aaskjer](https://github.com/aaskjer) |", readme)
        self.assertIn("| [`odd 'name'`](10.json) | - |", readme, "a file from before the column says so")
        self.assertIn("| [`sneaky`](11.json) | - |", readme, "a name GitHub would never issue is left out, not linked")
        self.assertNotIn("evil.example", readme)

    def test_a_pull_request_github_refuses_fails_the_run_and_tells_the_ticket(self):
        issue = ticket("spam", spam_pairs("spamDomains: newsite"))
        code, rec, _ = self.run_main(issue, [("git fetch origin", [(0, ""), (1, "")]),
                                             ("git show origin/submissions:README.md", (0, README)),
                                             ("gh pr list", (0, "[]")), ("gh pr create", (1, ""))])
        self.assertEqual(code, 1)
        self.assertEqual(rec.commands()[-1], "gh issue comment")

    def test_neither_front_page_carries_anything_only_the_maintainer_needs(self):
        # Both pages are read by whoever finds the branch. What the repository is set to, which script writes
        # what, and which local tool gates a promotion are none of their business - and the Actions setting is
        # something a stranger has no reason to be told at all.
        folder = tempfile.mkdtemp(prefix="ts-profiles-front-")
        pages = [README, s.profiles_readme(folder, "aaskjer/TwitchSentry")]
        for page in pages:
            for leak in ("Settings → Actions", "Allow GitHub Actions", "submission.py", "community-submissions.yml",
                         "check-feed.ps1", "tools/", ".github"):
                self.assertNotIn(leak, page, leak)

    def test_the_submissions_front_page_links_out_of_the_branch(self):
        # The branch has no Feed folder and no profiles, so a relative link from it leads nowhere.
        self.assertIn("https://github.com/aaskjer/TwitchSentry/blob/main/Feed/README.md", README)
        self.assertIn("https://github.com/aaskjer/TwitchSentry/tree/profiles", README)
        self.assertNotIn("](../", README)
        for folder in s.FOLDER.values():
            self.assertIn("| `%s/` |" % folder, README)


OPEN_SPAM_TICKET = '{"state": "OPEN", "labels": [{"name": "share: spam list"}]}'


class AMergedSubmission(WorkflowHarness):
    """What the workflow does when a pull request is closed. GitHub reads "Closes #N" only in a pull request
    into main, so for one into the submissions branch the script closes the ticket itself."""

    def pull(self, merged=True, base="submissions", head="submission/42", head_repo="aaskjer/TwitchSentry"):
        return {"number": 50, "merged": merged, "base": {"ref": base},
                "head": {"ref": head, "repo": {"full_name": head_repo} if head_repo else None}}

    def closed(self, pull, answers):
        return self.run_event({"action": "closed", "pull_request": pull}, answers)

    def test_merging_it_closes_its_ticket_and_says_where_the_file_is(self):
        code, rec, _ = self.closed(self.pull(), [("gh issue view", (0, OPEN_SPAM_TICKET))])
        self.assertEqual(code, 0)
        self.assertEqual(rec.commands(), ["gh issue view", "gh issue comment", "gh issue close"])
        self.assertEqual(rec.calls[0][3], "42")
        self.assertEqual(rec.calls[2][3:], ["42", "--repo", "aaskjer/TwitchSentry", "--reason", "completed"])
        with open(rec.calls[1][rec.calls[1].index("--body-file") + 1], encoding="utf-8") as f:
            body = f.read()
        self.assertIn("#50 was merged", body)
        self.assertIn("https://github.com/aaskjer/TwitchSentry/blob/submissions/spam/42.json", body)
        self.assertIn("spam feed", body)

    def test_a_translation_is_told_where_it_goes_next(self):
        answer = '{"state": "OPEN", "labels": [{"name": "share: translation"}]}'
        _, rec, _ = self.closed(self.pull(), [("gh issue view", (0, answer))])
        with open(rec.calls[1][rec.calls[1].index("--body-file") + 1], encoding="utf-8") as f:
            body = f.read()
        self.assertIn("/blob/submissions/translations/42.json", body)
        self.assertIn("next language update", body)

    def test_closing_it_without_merging_leaves_the_ticket_open(self):
        code, rec, _ = self.closed(self.pull(merged=False), [])
        self.assertEqual((code, rec.calls), (0, []))

    def test_only_a_branch_of_this_workflow_merged_into_submissions_counts(self):
        for pull in (self.pull(base="main"), self.pull(head="claude/profiles-branch"), self.pull(head="submission/42/x"),
                     self.pull(head="submission/"), self.pull(head_repo="someone/TwitchSentry"), self.pull(head_repo=None)):
            code, rec, _ = self.closed(pull, [])
            self.assertEqual((code, rec.calls), (0, []), pull)

    def test_a_ticket_already_closed_or_of_another_kind_is_left_as_it_is(self):
        for answer in ('{"state": "CLOSED", "labels": [{"name": "share: spam list"}]}',
                       '{"state": "OPEN", "labels": [{"name": "bug"}]}',
                       '{"state": "OPEN", "labels": [{"name": "share: profile"}]}'):
            code, rec, _ = self.closed(self.pull(), [("gh issue view", (0, answer))])
            self.assertEqual((code, rec.commands()), (0, ["gh issue view"]), answer)

    def test_a_ticket_github_cannot_find_fails_the_run(self):
        code, rec, _ = self.closed(self.pull(), [("gh issue view", (1, "", "GraphQL: Could not resolve to an issue"))])
        self.assertEqual((code, rec.commands()), (1, ["gh issue view"]))


if __name__ == "__main__":
    unittest.main()
