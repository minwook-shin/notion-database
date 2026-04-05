"""
Tests for notion_database.models.blocks
"""
import unittest

from notion_database.models.blocks import BlockContent
from notion_database.models.rich_text import RichText


class TestBlockContentText(unittest.TestCase):
    def _check(self, block, expected_type):
        self.assertEqual(block["object"], "block")
        self.assertEqual(block["type"], expected_type)
        self.assertIn(expected_type, block)

    def test_paragraph_string(self):
        b = BlockContent.paragraph("hello")
        self._check(b, "paragraph")
        self.assertEqual(b["paragraph"]["rich_text"][0]["text"]["content"], "hello")
        self.assertEqual(b["paragraph"]["color"], "default")

    def test_paragraph_rich_text_list(self):
        rt = [RichText.text("bold", bold=True)]
        b = BlockContent.paragraph(rt)
        self.assertIs(b["paragraph"]["rich_text"], rt)

    def test_paragraph_with_color(self):
        b = BlockContent.paragraph("text", color="red")
        self.assertEqual(b["paragraph"]["color"], "red")

    def test_paragraph_with_children(self):
        child = BlockContent.paragraph("child")
        b = BlockContent.paragraph("parent", children=[child])
        self.assertEqual(b["paragraph"]["children"][0], child)

    def test_heading_1(self):
        b = BlockContent.heading_1("Title")
        self._check(b, "heading_1")
        self.assertFalse(b["heading_1"]["is_toggleable"])

    def test_heading_1_toggleable(self):
        b = BlockContent.heading_1("Toggle", is_toggleable=True)
        self.assertTrue(b["heading_1"]["is_toggleable"])

    def test_heading_2(self):
        self._check(BlockContent.heading_2("h2"), "heading_2")

    def test_heading_3(self):
        self._check(BlockContent.heading_3("h3"), "heading_3")

    def test_callout(self):
        b = BlockContent.callout("Note")
        self._check(b, "callout")
        self.assertEqual(b["callout"]["rich_text"][0]["text"]["content"], "Note")

    def test_callout_with_icon(self):
        icon = {"type": "emoji", "emoji": "💡"}
        b = BlockContent.callout("Note", icon=icon)
        self.assertEqual(b["callout"]["icon"], icon)

    def test_quote(self):
        self._check(BlockContent.quote("q"), "quote")

    def test_bulleted_list_item(self):
        self._check(BlockContent.bulleted_list_item("item"), "bulleted_list_item")

    def test_numbered_list_item(self):
        self._check(BlockContent.numbered_list_item("1"), "numbered_list_item")

    def test_to_do_unchecked(self):
        b = BlockContent.to_do("task")
        self._check(b, "to_do")
        self.assertFalse(b["to_do"]["checked"])

    def test_to_do_checked(self):
        b = BlockContent.to_do("done", checked=True)
        self.assertTrue(b["to_do"]["checked"])

    def test_toggle(self):
        b = BlockContent.toggle("click me")
        self._check(b, "toggle")

    def test_toggle_with_children(self):
        b = BlockContent.toggle("toggle", children=[BlockContent.paragraph("hidden")])
        self.assertEqual(len(b["toggle"]["children"]), 1)


class TestBlockContentCode(unittest.TestCase):
    def test_code_default_language(self):
        b = BlockContent.code("print('hello')")
        self.assertEqual(b["type"], "code")
        self.assertEqual(b["code"]["language"], "plain text")
        self.assertEqual(b["code"]["rich_text"][0]["text"]["content"], "print('hello')")

    def test_code_python(self):
        b = BlockContent.code("x = 1", language="python")
        self.assertEqual(b["code"]["language"], "python")

    def test_code_with_caption(self):
        b = BlockContent.code("x", caption="snippet")
        self.assertIn("caption", b["code"])
        self.assertEqual(b["code"]["caption"][0]["text"]["content"], "snippet")


class TestBlockContentMedia(unittest.TestCase):
    def test_image(self):
        b = BlockContent.image("https://example.com/img.png")
        self.assertEqual(b["type"], "image")
        self.assertEqual(b["image"]["type"], "external")
        self.assertEqual(b["image"]["external"]["url"], "https://example.com/img.png")

    def test_image_with_caption(self):
        b = BlockContent.image("https://example.com/img.png", caption="fig 1")
        self.assertIn("caption", b["image"])

    def test_video(self):
        b = BlockContent.video("https://example.com/vid.mp4")
        self.assertEqual(b["type"], "video")

    def test_file(self):
        b = BlockContent.file("https://example.com/doc.pdf")
        self.assertEqual(b["type"], "file")

    def test_pdf(self):
        b = BlockContent.pdf("https://example.com/report.pdf")
        self.assertEqual(b["type"], "pdf")

    def test_embed(self):
        b = BlockContent.embed("https://example.com")
        self.assertEqual(b["type"], "embed")
        self.assertEqual(b["embed"]["url"], "https://example.com")

    def test_bookmark(self):
        b = BlockContent.bookmark("https://example.com")
        self.assertEqual(b["type"], "bookmark")
        self.assertEqual(b["bookmark"]["url"], "https://example.com")

    def test_bookmark_with_caption(self):
        b = BlockContent.bookmark("https://example.com", caption="link")
        self.assertIn("caption", b["bookmark"])


class TestBlockContentStructural(unittest.TestCase):
    def test_divider(self):
        b = BlockContent.divider()
        self.assertEqual(b["type"], "divider")
        self.assertEqual(b["divider"], {})

    def test_table_of_contents(self):
        b = BlockContent.table_of_contents()
        self.assertEqual(b["type"], "table_of_contents")

    def test_table_of_contents_color(self):
        b = BlockContent.table_of_contents(color="gray")
        self.assertEqual(b["table_of_contents"]["color"], "gray")

    def test_breadcrumb(self):
        b = BlockContent.breadcrumb()
        self.assertEqual(b["type"], "breadcrumb")

    def test_equation(self):
        b = BlockContent.equation("E=mc^2")
        self.assertEqual(b["type"], "equation")
        self.assertEqual(b["equation"]["expression"], "E=mc^2")

    def test_column_list(self):
        left = [BlockContent.paragraph("left")]
        right = [BlockContent.paragraph("right")]
        b = BlockContent.column_list([left, right])
        self.assertEqual(b["type"], "column_list")
        columns = b["column_list"]["children"]
        self.assertEqual(len(columns), 2)
        self.assertEqual(columns[0]["type"], "column")
        self.assertEqual(columns[0]["column"]["children"], left)
        self.assertEqual(columns[1]["column"]["children"], right)


if __name__ == "__main__":
    unittest.main()
