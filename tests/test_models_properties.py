"""
Tests for notion_database.models.properties
"""
import unittest

from notion_database.models.properties import PropertySchema, PropertyValue


class TestPropertyValue(unittest.TestCase):
    def test_title_string(self):
        pv = PropertyValue.title("My Page")
        self.assertIn("title", pv)
        self.assertEqual(pv["title"][0]["text"]["content"], "My Page")

    def test_title_rich_text_list(self):
        from notion_database.models.rich_text import RichText
        rt = [RichText.text("bold", bold=True)]
        pv = PropertyValue.title(rt)
        self.assertIs(pv["title"], rt)

    def test_rich_text(self):
        pv = PropertyValue.rich_text("hello")
        self.assertIn("rich_text", pv)
        self.assertEqual(pv["rich_text"][0]["text"]["content"], "hello")

    def test_number_int(self):
        pv = PropertyValue.number(42)
        self.assertEqual(pv, {"number": 42})

    def test_number_float(self):
        pv = PropertyValue.number(3.14)
        self.assertEqual(pv, {"number": 3.14})

    def test_select(self):
        pv = PropertyValue.select("Active")
        self.assertEqual(pv, {"select": {"name": "Active"}})

    def test_multi_select(self):
        pv = PropertyValue.multi_select(["a", "b"])
        self.assertEqual(pv["multi_select"], [{"name": "a"}, {"name": "b"}])

    def test_status(self):
        pv = PropertyValue.status("In progress")
        self.assertEqual(pv, {"status": {"name": "In progress"}})

    def test_date_start_only(self):
        pv = PropertyValue.date("2024-01-01")
        self.assertEqual(pv["date"]["start"], "2024-01-01")
        self.assertNotIn("end", pv["date"])

    def test_date_with_end(self):
        pv = PropertyValue.date("2024-01-01", end="2024-01-31")
        self.assertEqual(pv["date"]["end"], "2024-01-31")

    def test_date_with_timezone(self):
        pv = PropertyValue.date("2024-01-01", time_zone="Asia/Seoul")
        self.assertEqual(pv["date"]["time_zone"], "Asia/Seoul")

    def test_checkbox_true(self):
        pv = PropertyValue.checkbox(True)
        self.assertEqual(pv, {"checkbox": True})

    def test_checkbox_false(self):
        pv = PropertyValue.checkbox(False)
        self.assertEqual(pv, {"checkbox": False})

    def test_url(self):
        pv = PropertyValue.url("https://example.com")
        self.assertEqual(pv, {"url": "https://example.com"})

    def test_email(self):
        pv = PropertyValue.email("test@example.com")
        self.assertEqual(pv, {"email": "test@example.com"})

    def test_phone_number(self):
        pv = PropertyValue.phone_number("+82-10-1234-5678")
        self.assertEqual(pv, {"phone_number": "+82-10-1234-5678"})

    def test_people(self):
        pv = PropertyValue.people(["uid1", "uid2"])
        self.assertEqual(pv["people"], [{"id": "uid1"}, {"id": "uid2"}])

    def test_files_url_list(self):
        pv = PropertyValue.files(["https://example.com/file.pdf"])
        self.assertEqual(pv["files"][0]["type"], "external")
        self.assertEqual(pv["files"][0]["external"]["url"], "https://example.com/file.pdf")

    def test_files_dict_list(self):
        pv = PropertyValue.files([{"name": "report", "url": "https://example.com/r.pdf"}])
        self.assertEqual(pv["files"][0]["name"], "report")
        self.assertEqual(pv["files"][0]["external"]["url"], "https://example.com/r.pdf")

    def test_relation(self):
        pv = PropertyValue.relation(["page1", "page2"])
        self.assertEqual(pv["relation"], [{"id": "page1"}, {"id": "page2"}])


class TestPropertySchema(unittest.TestCase):
    def test_title(self):
        self.assertEqual(PropertySchema.title(), {"title": {}})

    def test_rich_text(self):
        self.assertEqual(PropertySchema.rich_text(), {"rich_text": {}})

    def test_number_default(self):
        s = PropertySchema.number()
        self.assertEqual(s["number"]["format"], "number")

    def test_number_custom_format(self):
        s = PropertySchema.number("dollar")
        self.assertEqual(s["number"]["format"], "dollar")

    def test_select_no_options(self):
        s = PropertySchema.select()
        self.assertEqual(s["select"]["options"], [])

    def test_select_with_options(self):
        opts = [{"name": "Active", "color": "green"}]
        s = PropertySchema.select(opts)
        self.assertEqual(s["select"]["options"], opts)

    def test_multi_select(self):
        s = PropertySchema.multi_select()
        self.assertEqual(s["multi_select"]["options"], [])

    def test_status(self):
        self.assertEqual(PropertySchema.status(), {"status": {}})

    def test_date(self):
        self.assertEqual(PropertySchema.date(), {"date": {}})

    def test_checkbox(self):
        self.assertEqual(PropertySchema.checkbox(), {"checkbox": {}})

    def test_url(self):
        self.assertEqual(PropertySchema.url(), {"url": {}})

    def test_email(self):
        self.assertEqual(PropertySchema.email(), {"email": {}})

    def test_phone_number(self):
        self.assertEqual(PropertySchema.phone_number(), {"phone_number": {}})

    def test_people(self):
        self.assertEqual(PropertySchema.people(), {"people": {}})

    def test_files(self):
        self.assertEqual(PropertySchema.files(), {"files": {}})

    def test_created_time(self):
        self.assertEqual(PropertySchema.created_time(), {"created_time": {}})

    def test_created_by(self):
        self.assertEqual(PropertySchema.created_by(), {"created_by": {}})

    def test_last_edited_time(self):
        self.assertEqual(PropertySchema.last_edited_time(), {"last_edited_time": {}})

    def test_last_edited_by(self):
        self.assertEqual(PropertySchema.last_edited_by(), {"last_edited_by": {}})

    def test_formula(self):
        s = PropertySchema.formula("prop('Score') * 2")
        self.assertEqual(s["formula"]["expression"], "prop('Score') * 2")

    def test_relation_single_property(self):
        s = PropertySchema.relation("db-id")
        self.assertEqual(s["relation"]["database_id"], "db-id")
        self.assertEqual(s["relation"]["type"], "single_property")
        self.assertIn("single_property", s["relation"])

    def test_relation_dual_property(self):
        s = PropertySchema.relation("db-id", type="dual_property", synced_property_name="Mirror")
        self.assertEqual(s["relation"]["type"], "dual_property")
        self.assertEqual(s["relation"]["dual_property"]["synced_property_name"], "Mirror")

    def test_rollup(self):
        s = PropertySchema.rollup("Tasks", "Count", "count")
        self.assertEqual(s["rollup"]["relation_property_name"], "Tasks")
        self.assertEqual(s["rollup"]["rollup_property_name"], "Count")
        self.assertEqual(s["rollup"]["function"], "count")

    def test_unique_id(self):
        self.assertIn("unique_id", PropertySchema.unique_id())

    def test_unique_id_with_prefix(self):
        s = PropertySchema.unique_id(prefix="TASK")
        self.assertEqual(s["unique_id"]["prefix"], "TASK")


if __name__ == "__main__":
    unittest.main()
