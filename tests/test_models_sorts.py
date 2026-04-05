"""
Tests for notion_database.models.sorts
"""
import unittest

from notion_database.models.sorts import Sort


class TestSort(unittest.TestCase):
    def test_by_property_ascending(self):
        s = Sort.by_property("Name")
        self.assertEqual(s, {"property": "Name", "direction": "ascending"})

    def test_by_property_descending(self):
        s = Sort.by_property("Name", "descending")
        self.assertEqual(s["direction"], "descending")

    def test_by_timestamp_created(self):
        s = Sort.by_timestamp("created_time")
        self.assertEqual(s, {"timestamp": "created_time", "direction": "ascending"})

    def test_by_timestamp_last_edited_descending(self):
        s = Sort.by_timestamp("last_edited_time", "descending")
        self.assertEqual(s["direction"], "descending")

    def test_ascending_alias(self):
        s = Sort.ascending("Name")
        self.assertEqual(s, {"property": "Name", "direction": "ascending"})

    def test_descending_alias(self):
        s = Sort.descending("Name")
        self.assertEqual(s, {"property": "Name", "direction": "descending"})


if __name__ == "__main__":
    unittest.main()
