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

    def test_the_language_dropdown_offers_exactly_the_published_languages(self):
        with open(TEMPLATES["translation"], encoding="utf-8") as f:
            text = f.read()
        offered = re.findall(r"^\s+- .*\(([A-Za-z-]+)\)\s*$", text, re.M)
        with open(os.path.join(REPO_ROOT, "Language", "index.json"), encoding="utf-8-sig") as f:
            index = json.load(f)
        self.assertEqual(sorted(offered), sorted(e["code"] for e in index if e["code"] != "en"))


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
        self.root = workspace({"schema": 1, "version": 1,
                               "lists": {"spamDomains": ["smmgen"], "strongKeywords": ["botrush"]},
                               "retracted": {"keywords": ["old offer"]}})

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
        self.assertEqual(r.path, "Submissions/spam/42.json")
        self.assertEqual(r.title, "Spam wording from #42 (3 entries)")

    def test_entries_already_in_the_feed_are_left_out(self):
        r = self.build("spamDomains: smmgen\nspamDomains: newsite")
        self.assertEqual(r.document["entries"], {"spamDomains": ["newsite"]})
        self.assertIn("Already in the feed", r.summary)

    def test_nothing_new_opens_no_pull_request(self):
        r = self.build("spamDomains: smmgen\nstrongKeywords: BotRush")
        self.assertIsNone(r.document)
        self.assertEqual(r.nothing_new, {"spamDomains": ["smmgen"], "strongKeywords": ["botrush"]})

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
        self.assertEqual(r.document["profile"], {"twitchSentryProfile": 1, "name": "Small chat, strict links",
                                                 "twitchSentry": "v2.1.0",
                                                 "settings": {"spamScoreThreshold": 1.0, "discordWebhookEnabled": True,
                                                              "timeoutDurationSeconds": 300, "autoModCategories": []}})
        self.assertEqual(r.path, "Submissions/profiles/42.json")
        self.assertEqual(r.title, "Profile \"Small chat, strict links\" from #42")

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
        self.assertEqual(r.path, "Submissions/translations/42.json")

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
    """Stands in for subprocess: records every call and answers from a script of responses."""

    def __init__(self, answers):
        self.calls = []
        self.answers = answers

    def __call__(self, args, check=True):
        self.calls.append(list(args))
        key = " ".join(args[:3])
        code, out = 0, ""
        for prefix, answer in self.answers:
            if key.startswith(prefix):
                code, out = answer
                break
        if check and code != 0:
            raise subprocess.CalledProcessError(code, args, output=out, stderr="failed")
        return subprocess.CompletedProcess(args, code, stdout=out, stderr="")

    def commands(self):
        return [" ".join(c[:3]) for c in self.calls]


class TheWorkflowRun(unittest.TestCase):
    def run_main(self, issue, answers, root=None):
        root = root or workspace()
        event = tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".json", delete=False)
        with event:
            json.dump({"issue": issue, "repository": {"default_branch": "main"}}, event)
        recorder = Recorder(answers)
        env = {"GITHUB_EVENT_PATH": event.name, "GITHUB_REPOSITORY": "aaskjer/TwitchSentry", "GITHUB_WORKSPACE": root}
        with mock.patch.dict(os.environ, env), mock.patch.object(s, "run", recorder), \
                mock.patch("sys.stdout"), mock.patch("sys.stderr"):
            code = s.main()
        return code, recorder, root

    def test_a_new_ticket_becomes_a_branch_a_file_and_a_pull_request(self):
        issue = ticket("spam", spam_pairs("spamDomains: newsite"))
        code, rec, root = self.run_main(issue, [
            ("git fetch --depth=1", (1, "")),
            ("gh pr list", (0, "[]")),
            ("gh pr create", (0, "https://github.com/aaskjer/TwitchSentry/pull/7\n")),
        ])
        self.assertEqual(code, 0)
        self.assertEqual(rec.commands(), [
            "git fetch --depth=1", "git checkout -B", "git add Submissions/spam/42.json", "git -c user.name=github-actions[bot]",
            "git push --force", "gh pr list", "gh pr create", "gh issue comment"])
        self.assertIn("submission/42", rec.calls[1])
        with open(os.path.join(root, "Submissions", "spam", "42.json"), encoding="utf-8") as f:
            self.assertEqual(json.load(f)["entries"], {"spamDomains": ["newsite"]})

    def test_no_call_carries_the_ticket_text_on_its_command_line(self):
        issue = ticket("spam", spam_pairs("spamDomains: newsite", context="$(rm -rf /) `whoami`"))
        _, rec, _ = self.run_main(issue, [("git fetch --depth=1", (1, "")), ("gh pr list", (0, "[]")),
                                          ("gh pr create", (0, "https://example/pull/7"))])
        for call in rec.calls:
            self.assertFalse(any("rm -rf" in part or "whoami" in part for part in call), call)

    def test_an_edit_that_changes_nothing_pushes_nothing_and_says_nothing(self):
        issue = ticket("spam", spam_pairs("spamDomains: newsite"))
        root = workspace()
        result = s.build("spam", issue, root)
        content = json.dumps(result.document, ensure_ascii=False, indent=2) + "\n"
        _, rec, _ = self.run_main(issue, [
            ("git fetch --depth=1", (0, "")),
            ("git show origin/submission/42:Submissions/spam/42.json", (0, content)),
            ("gh pr list", (0, '[{"number": 7, "url": "https://github.com/aaskjer/TwitchSentry/pull/7"}]')),
        ], root)
        self.assertEqual(rec.commands(), ["git fetch --depth=1", "git show origin/submission/42:Submissions/spam/42.json",
                                          "gh pr list", "gh pr edit"])
        self.assertEqual(rec.calls[-1][3], "7")

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

    def test_a_pull_request_github_refuses_fails_the_run_and_tells_the_ticket(self):
        issue = ticket("spam", spam_pairs("spamDomains: newsite"))
        code, rec, _ = self.run_main(issue, [("git fetch --depth=1", (1, "")), ("gh pr list", (0, "[]")),
                                             ("gh pr create", (1, ""))])
        self.assertEqual(code, 1)
        self.assertEqual(rec.commands()[-1], "gh issue comment")


if __name__ == "__main__":
    unittest.main()
