"""
Tests for notion_database.models.icons
"""
import unittest

from notion_database.models.icons import Cover, Icon


class TestIcon(unittest.TestCase):
    def test_emoji(self):
        icon = Icon.emoji("🚀")
        self.assertEqual(icon, {"type": "emoji", "emoji": "🚀"})

    def test_external(self):
        icon = Icon.external("https://example.com/icon.png")
        self.assertEqual(icon["type"], "external")
        self.assertEqual(icon["external"]["url"], "https://example.com/icon.png")


class TestCover(unittest.TestCase):
    def test_external(self):
        cover = Cover.external("https://example.com/cover.jpg")
        self.assertEqual(cover["type"], "external")
        self.assertEqual(cover["external"]["url"], "https://example.com/cover.jpg")


if __name__ == "__main__":
    unittest.main()
