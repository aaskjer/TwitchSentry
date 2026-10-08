import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import botlist_removal as r  # noqa: E402


def ticket(accounts, state="open", labels=("botlist: removal",), login="someone"):
    body = "### Accounts\n\n%s\n\n### Why is it not a bot?\n\n_No response_\n" % accounts
    return {"issue": {"number": 7, "state": state, "body": body, "user": {"login": login},
                      "labels": [{"name": l} for l in labels]}}


class Recorder:
    def __init__(self):
        self.calls = []
        self.texts = []

    def __call__(self, args):
        self.calls.append(args[:3])
        if "--body-file" in args:
            with open(args[args.index("--body-file") + 1], encoding="utf-8") as f:
                self.texts.append(f.read())


class Names(unittest.TestCase):
    def test_logins_are_read_whatever_way_they_are_written(self):
        names, bad = r.names_of("@Some_Bot\nhttps://www.twitch.tv/Other_Bot/videos, `third_bot`; some_bot\n12345")
        self.assertEqual(names, ["some_bot", "other_bot", "third_bot", "12345"])
        self.assertEqual(bad, [])

    def test_anything_else_is_left_out_and_named(self):
        names, bad = r.names_of("good_one\nnot-a-login\nüber\n" + "x" * 26)
        self.assertEqual(names, ["good_one"])
        self.assertEqual(bad, ["not-a-login", "über", "x" * 26])

    def test_nothing_in_nothing_out(self):
        self.assertEqual(r.names_of(None), ([], []))
        self.assertEqual(r.names_of("  @ \n"), ([], []))

    def test_the_form_is_read_by_its_headings(self):
        values = r.parse_form("### Accounts\n\na\nb\n\n### Why is it not a bot?\n\n_No response_", r.FIELDS)
        self.assertEqual(values, {"accounts": "a\nb", "why": ""})

    def test_quoted_text_cannot_break_out_of_a_code_span(self):
        self.assertEqual(r.printable("a`b‮c"), "a'b?c")


class Answer(unittest.TestCase):
    def test_every_outcome_is_named(self):
        text = r.answer({"removed": [{"id": "1", "login": "bot_a"}], "cleared": [{"id": "2", "login": "bot_b"}],
                         "unlisted": ["bot_c"], "committed": True}, ["no!"])
        self.assertIn("Taken off the shared bot list: `bot_a`.", text)
        self.assertIn("lifts that ban within minutes", text)
        self.assertIn("Reported but not on the list yet: `bot_b`.", text)
        self.assertIn("Not on the list at all: `bot_c`.", text)
        self.assertIn("Not Twitch names, so left alone: `no!`.", text)
        self.assertNotIn("written again", text)

    def test_a_list_not_yet_written_is_said(self):
        text = r.answer({"removed": [{"id": "1", "login": "bot_a"}], "committed": False}, [])
        self.assertIn("written again within a few minutes", text)


class Handling(unittest.TestCase):
    def run_ticket(self, event, status=200, result=None, key="secret"):
        gh = Recorder()
        asked = []

        def relay(names, number, by, k):
            asked.append((names, number, by, k))
            return status, result

        code = r.handle(event, "aaskjer/TwitchSentry", key, relay=relay, gh=gh)
        return code, gh, asked

    def test_a_removal_is_asked_for_answered_and_closed(self):
        result = {"ok": True, "removed": [{"id": "1", "login": "bot_a"}], "cleared": [], "unlisted": ["bot_z"], "committed": True}
        code, gh, asked = self.run_ticket(ticket("@Bot_A\nbot_z"), result=result)
        self.assertEqual(code, 0)
        self.assertEqual(asked, [(["bot_a", "bot_z"], 7, "someone", "secret")])
        self.assertEqual(gh.calls, [["gh", "issue", "comment"], ["gh", "issue", "close"]])
        self.assertIn("`bot_a`", gh.texts[0])

    def test_an_author_github_would_never_name_is_not_passed_on(self):
        result = {"ok": True, "removed": [], "cleared": [], "unlisted": ["bot_a"], "committed": False}
        _, _, asked = self.run_ticket(ticket("bot_a", login="bad login`"), result=result)
        self.assertIsNone(asked[0][2])

    def test_no_readable_name_asks_for_an_edit_and_stays_open(self):
        code, gh, asked = self.run_ticket(ticket("not-a-login!\n@"))
        self.assertEqual(code, 0)
        self.assertEqual(asked, [])
        self.assertEqual(gh.calls, [["gh", "issue", "comment"]])
        self.assertIn("Edit it", gh.texts[0])

    def test_too_many_names_are_turned_away(self):
        code, gh, asked = self.run_ticket(ticket("\n".join("bot_%d" % i for i in range(51))))
        self.assertEqual(asked, [])
        self.assertIn("at most 50", gh.texts[0])

    def test_an_unreachable_relay_keeps_the_ticket_open_and_fails_the_run(self):
        code, gh, asked = self.run_ticket(ticket("bot_a"), status=0, result=None)
        self.assertEqual(code, 1)
        self.assertEqual(gh.calls, [["gh", "issue", "comment"]])
        self.assertIn("Nothing was removed yet", gh.texts[0])

    def test_a_refusing_relay_is_no_success_either(self):
        code, gh, _ = self.run_ticket(ticket("bot_a"), status=401, result={"ok": False, "error": "not allowed"})
        self.assertEqual(code, 1)
        self.assertNotIn(["gh", "issue", "close"], gh.calls)

    def test_without_the_key_nothing_is_asked_or_said(self):
        for key in ("", " \n"):
            code, gh, asked = self.run_ticket(ticket("bot_a"), key=key)
            self.assertEqual((code, gh.calls, asked), (1, [], []))

    def test_a_key_pasted_with_spaces_or_a_line_break_still_fits(self):
        result = {"ok": True, "removed": [], "cleared": [], "unlisted": ["bot_a"], "committed": False}
        _, _, asked = self.run_ticket(ticket("bot_a"), result=result, key=" secret\n")
        self.assertEqual(asked[0][3], "secret")

    def test_other_tickets_are_left_alone(self):
        for event in (ticket("bot_a", state="closed"), ticket("bot_a", labels=("bug",)), {"issue": {}}):
            code, gh, asked = self.run_ticket(event)
            self.assertEqual((code, gh.calls, asked), (0, [], []))


if __name__ == "__main__":
    unittest.main()
