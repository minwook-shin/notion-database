"""
Tests for notion_database.models.filters
"""
import unittest

from notion_database.models.filters import Filter


class TestCompoundFilters(unittest.TestCase):
    def test_and(self):
        f = Filter.and_([{"a": 1}, {"b": 2}])
        self.assertEqual(f, {"and": [{"a": 1}, {"b": 2}]})

    def test_or(self):
        f = Filter.or_([{"a": 1}, {"b": 2}])
        self.assertEqual(f, {"or": [{"a": 1}, {"b": 2}]})

    def test_nested(self):
        inner = Filter.or_([Filter.text("Name").equals("a"), Filter.text("Name").equals("b")])
        outer = Filter.and_([inner, Filter.checkbox("Active").equals(True)])
        self.assertIn("and", outer)
        self.assertIn("or", outer["and"][0])


class TestTextFilter(unittest.TestCase):
    def _f(self, method, *args):
        return getattr(Filter.text("Name"), method)(*args)

    def test_equals(self):
        f = self._f("equals", "Alice")
        self.assertEqual(f, {"property": "Name", "rich_text": {"equals": "Alice"}})

    def test_does_not_equal(self):
        f = self._f("does_not_equal", "Bob")
        self.assertIn("does_not_equal", f["rich_text"])

    def test_contains(self):
        f = self._f("contains", "Al")
        self.assertIn("contains", f["rich_text"])

    def test_does_not_contain(self):
        f = self._f("does_not_contain", "Al")
        self.assertIn("does_not_contain", f["rich_text"])

    def test_starts_with(self):
        f = self._f("starts_with", "Al")
        self.assertIn("starts_with", f["rich_text"])

    def test_ends_with(self):
        f = self._f("ends_with", "ce")
        self.assertIn("ends_with", f["rich_text"])

    def test_is_empty(self):
        f = self._f("is_empty")
        self.assertEqual(f["rich_text"], {"is_empty": True})

    def test_is_not_empty(self):
        f = self._f("is_not_empty")
        self.assertEqual(f["rich_text"], {"is_not_empty": True})


class TestTitleFilter(unittest.TestCase):
    def test_title_type(self):
        f = Filter.title("Name").equals("Test")
        self.assertIn("title", f)
        self.assertEqual(f["title"]["equals"], "Test")


class TestNumberFilter(unittest.TestCase):
    def _f(self, method, *args):
        return getattr(Filter.number("Score"), method)(*args)

    def test_equals(self):
        f = self._f("equals", 100)
        self.assertEqual(f["number"]["equals"], 100)

    def test_greater_than(self):
        f = self._f("greater_than", 50)
        self.assertEqual(f["number"]["greater_than"], 50)

    def test_less_than(self):
        f = self._f("less_than", 50)
        self.assertIn("less_than", f["number"])

    def test_gte(self):
        f = self._f("greater_than_or_equal_to", 50)
        self.assertIn("greater_than_or_equal_to", f["number"])

    def test_lte(self):
        f = self._f("less_than_or_equal_to", 50)
        self.assertIn("less_than_or_equal_to", f["number"])

    def test_is_empty(self):
        f = self._f("is_empty")
        self.assertEqual(f["number"]["is_empty"], True)


class TestCheckboxFilter(unittest.TestCase):
    def test_equals_true(self):
        f = Filter.checkbox("Done").equals(True)
        self.assertEqual(f["checkbox"]["equals"], True)

    def test_equals_false(self):
        f = Filter.checkbox("Done").equals(False)
        self.assertEqual(f["checkbox"]["equals"], False)


class TestSelectFilter(unittest.TestCase):
    def test_equals(self):
        f = Filter.select("Status").equals("Active")
        self.assertEqual(f["select"]["equals"], "Active")

    def test_does_not_equal(self):
        f = Filter.select("Status").does_not_equal("Done")
        self.assertIn("does_not_equal", f["select"])

    def test_is_empty(self):
        f = Filter.select("Status").is_empty()
        self.assertEqual(f["select"]["is_empty"], True)


class TestMultiSelectFilter(unittest.TestCase):
    def test_contains(self):
        f = Filter.multi_select("Tags").contains("python")
        self.assertEqual(f["multi_select"]["contains"], "python")

    def test_does_not_contain(self):
        f = Filter.multi_select("Tags").does_not_contain("java")
        self.assertIn("does_not_contain", f["multi_select"])


class TestDateFilter(unittest.TestCase):
    def test_equals(self):
        f = Filter.date("Due").equals("2024-01-01")
        self.assertEqual(f["date"]["equals"], "2024-01-01")

    def test_before(self):
        f = Filter.date("Due").before("2024-01-01")
        self.assertIn("before", f["date"])

    def test_after(self):
        f = Filter.date("Due").after("2024-01-01")
        self.assertIn("after", f["date"])

    def test_past_week(self):
        f = Filter.date("Due").past_week()
        self.assertEqual(f["date"]["past_week"], {})

    def test_next_month(self):
        f = Filter.date("Due").next_month()
        self.assertEqual(f["date"]["next_month"], {})

    def test_this_week(self):
        f = Filter.date("Due").this_week()
        self.assertEqual(f["date"]["this_week"], {})


class TestTimestampFilter(unittest.TestCase):
    def test_created_time_before(self):
        f = Filter.created_time().before("2024-01-01")
        self.assertEqual(f["timestamp"], "created_time")
        self.assertIn("before", f["created_time"])

    def test_last_edited_time_after(self):
        f = Filter.last_edited_time().after("2024-01-01")
        self.assertEqual(f["timestamp"], "last_edited_time")
        self.assertIn("after", f["last_edited_time"])

    def test_created_time_past_week(self):
        f = Filter.created_time().past_week()
        self.assertEqual(f["created_time"]["past_week"], {})


class TestRawFilter(unittest.TestCase):
    def test_passthrough(self):
        raw = {"property": "X", "formula": {"string": {"equals": "y"}}}
        self.assertIs(Filter.raw(raw), raw)


if __name__ == "__main__":
    unittest.main()
