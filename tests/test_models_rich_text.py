"""
Tests for notion_database.models.rich_text
"""
import unittest

from notion_database.models.rich_text import RichText, _normalize


class TestNormalize(unittest.TestCase):
    def test_string_becomes_single_element_list(self):
        result = _normalize("hello")
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["text"]["content"], "hello")

    def test_list_passthrough(self):
        items = [RichText.text("a"), RichText.text("b")]
        self.assertIs(_normalize(items), items)


class TestRichTextText(unittest.TestCase):
    def test_plain(self):
        rt = RichText.text("hello")
        self.assertEqual(rt["type"], "text")
        self.assertEqual(rt["text"]["content"], "hello")
        self.assertNotIn("annotations", rt)
        self.assertIsNone(rt["text"].get("link"))

    def test_bold(self):
        rt = RichText.text("bold", bold=True)
        self.assertTrue(rt["annotations"]["bold"])

    def test_italic(self):
        rt = RichText.text("italic", italic=True)
        self.assertTrue(rt["annotations"]["italic"])

    def test_underline(self):
        rt = RichText.text("u", underline=True)
        self.assertTrue(rt["annotations"]["underline"])

    def test_strikethrough(self):
        rt = RichText.text("s", strikethrough=True)
        self.assertTrue(rt["annotations"]["strikethrough"])

    def test_code(self):
        rt = RichText.text("code", code=True)
        self.assertTrue(rt["annotations"]["code"])

    def test_color(self):
        rt = RichText.text("c", color="red")
        self.assertEqual(rt["annotations"]["color"], "red")

    def test_default_color_no_annotation(self):
        rt = RichText.text("c", color="default")
        self.assertNotIn("annotations", rt)

    def test_link(self):
        rt = RichText.text("click", link="https://example.com")
        self.assertEqual(rt["text"]["link"]["url"], "https://example.com")

    def test_multiple_annotations(self):
        rt = RichText.text("multi", bold=True, italic=True, color="blue")
        self.assertTrue(rt["annotations"]["bold"])
        self.assertTrue(rt["annotations"]["italic"])
        self.assertEqual(rt["annotations"]["color"], "blue")


class TestRichTextMentions(unittest.TestCase):
    def test_mention_page(self):
        rt = RichText.mention_page("page-id")
        self.assertEqual(rt["type"], "mention")
        self.assertEqual(rt["mention"]["type"], "page")
        self.assertEqual(rt["mention"]["page"]["id"], "page-id")

    def test_mention_database(self):
        rt = RichText.mention_database("db-id")
        self.assertEqual(rt["mention"]["type"], "database")
        self.assertEqual(rt["mention"]["database"]["id"], "db-id")

    def test_mention_user(self):
        rt = RichText.mention_user("user-id")
        self.assertEqual(rt["mention"]["type"], "user")
        self.assertEqual(rt["mention"]["user"]["id"], "user-id")

    def test_mention_date(self):
        rt = RichText.mention_date("2024-01-01")
        self.assertEqual(rt["mention"]["type"], "date")
        self.assertEqual(rt["mention"]["date"]["start"], "2024-01-01")
        self.assertNotIn("end", rt["mention"]["date"])

    def test_mention_date_with_end(self):
        rt = RichText.mention_date("2024-01-01", end="2024-01-31")
        self.assertEqual(rt["mention"]["date"]["end"], "2024-01-31")

    def test_equation(self):
        rt = RichText.equation("E=mc^2")
        self.assertEqual(rt["type"], "equation")
        self.assertEqual(rt["equation"]["expression"], "E=mc^2")


if __name__ == "__main__":
    unittest.main()
