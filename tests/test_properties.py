import unittest

from notion_database.service.properties import Properties


class TestPropertyMethods(unittest.TestCase):
    def test_title(self):
        properties_object = Properties()
        properties_object.set_title(col="col_name", text="test")
        api_value = {
            "col_name": {
                "title": [
                    {
                        "text": {
                            "content": "test"
                        }
                    }
                ]
            }
        }
        self.assertEqual(properties_object.result, api_value)

    def test_title_for_empty_string(self):
        properties_object = Properties()
        properties_object.set_title(col="col_name", text="")
        api_value = {
            "col_name": {
                "title": [
                    {
                        "text": {
                            "content": ""
                        }
                    }
                ]
            }
        }
        self.assertEqual(properties_object.result, api_value)

    def test_title_for_setting(self):
        properties_object = Properties()
        properties_object.set_title(col="col_name")
        api_value = {"col_name": {"title": {}}}
        self.assertEqual(properties_object.result, api_value)

    def test_rich_text(self):
        properties_object = Properties()
        properties_object.set_rich_text(col="col_name", text="test")
        api_value = {
            "col_name": {
                "rich_text": [
                    {
                        "text": {
                            "content": "test"
                        }
                    }
                ]
            }
        }
        self.assertEqual(properties_object.result, api_value)

    def test_rich_text_for_empty_string(self):
        properties_object = Properties()
        properties_object.set_rich_text(col="col_name", text="")
        api_value = {
            "col_name": {
                "rich_text": [
                    {
                        "text": {
                            "content": ""
                        }
                    }
                ]
            }
        }
        self.assertEqual(properties_object.result, api_value)

    def test_rich_text_for_setting(self):
        properties_object = Properties()
        properties_object.set_rich_text(col="col_name")
        api_value = {"col_name": {"rich_text": {}}}
        self.assertEqual(properties_object.result, api_value)

    def test_number_0(self):
        properties_object = Properties()
        properties_object.set_number(col="col_name", text=0)
        api_value = {
            "col_name": {
                "number": 0
            }
        }
        self.assertEqual(properties_object.result, api_value)

    def test_number_int(self):
        properties_object = Properties()
        properties_object.set_number(col="col_name", text=1)
        api_value = {
            "col_name": {
                "number": 1
            }
        }
        self.assertEqual(properties_object.result, api_value)

    def test_number_float(self):
        properties_object = Properties()
        properties_object.set_number(col="col_name", text=1.5)
        api_value = {
            "col_name": {
                "number": 1.5
            }
        }
        self.assertEqual(properties_object.result, api_value)

    def test_number_for_setting(self):
        properties_object = Properties()
        properties_object.set_number(col="col_name")
        api_value = {"col_name": {"number": {}}}
        self.assertEqual(properties_object.result, api_value)

    def test_select(self):
        properties_object = Properties()
        properties_object.set_select(col="col_name", text="test")
        api_value = {
            "col_name": {
                "select":
                    {
                        "name": "test"
                    }
            }
        }
        self.assertEqual(properties_object.result, api_value)

    def test_select_for_setting(self):
        properties_object = Properties()
        properties_object.set_select(col="col_name")
        api_value = {"col_name": {"select": {}}}
        self.assertEqual(properties_object.result, api_value)

    def test_multi_select(self):
        properties_object = Properties()
        properties_object.set_multi_select(col="col_name", text_list=["test1", "test2"])
        api_value = {
            "col_name": {
                "multi_select": [
                    {
                        "name": "test1"
                    },
                    {
                        "name": "test2"
                    }
                ]
            }
        }
        self.assertEqual(properties_object.result, api_value)

    def test_multi_select_for_setting(self):
        properties_object = Properties()
        properties_object.set_multi_select(col="col_name")
        api_value = {"col_name": {"multi_select": {}}}
        self.assertEqual(properties_object.result, api_value)

    def test_checkbox_for_true(self):
        properties_object = Properties()
        properties_object.set_checkbox(col="col_name", text=True)
        api_value = {"col_name": {"checkbox": True}}
        self.assertEqual(properties_object.result, api_value)

    def test_checkbox_for_false(self):
        properties_object = Properties()
        properties_object.set_checkbox(col="col_name", text=False)
        api_value = {"col_name": {"checkbox": False}}
        self.assertEqual(properties_object.result, api_value)

    def test_checkbox_for_setting(self):
        properties_object = Properties()
        properties_object.set_checkbox(col="col_name")
        api_value = {"col_name": {"checkbox": {}}}
        self.assertEqual(properties_object.result, api_value)

    def test_url(self):
        properties_object = Properties()
        properties_object.set_url(col="col_name", text="www.google.com")
        api_value = {"col_name": {"url": "www.google.com"}}
        self.assertEqual(properties_object.result, api_value)

    def test_url_for_setting(self):
        properties_object = Properties()
        properties_object.set_url(col="col_name")
        api_value = {"col_name": {"url": {}}}
        self.assertEqual(properties_object.result, api_value)

    def test_email(self):
        properties_object = Properties()
        properties_object.set_email(col="col_name", text="test@test.com")
        api_value = {"col_name": {"email": "test@test.com"}}
        self.assertEqual(properties_object.result, api_value)

    def test_email_for_setting(self):
        properties_object = Properties()
        properties_object.set_email(col="col_name")
        api_value = {"col_name": {"email": {}}}
        self.assertEqual(properties_object.result, api_value)

    def test_phone_number(self):
        properties_object = Properties()
        properties_object.set_phone_number(col="col_name", text="+8210-0000-0000")
        api_value = {"col_name": {"phone_number": "+8210-0000-0000"}}
        self.assertEqual(properties_object.result, api_value)

    def test_phone_number_for_setting(self):
        properties_object = Properties()
        properties_object.set_phone_number(col="col_name")
        api_value = {"col_name": {"phone_number": {}}}
        self.assertEqual(properties_object.result, api_value)

    def test_date(self):
        properties_object = Properties()
        start = "2022-12-31T01:01:01.000+0900"
        end = "2023-01-10T01:01:01.000+0900"
        properties_object.set_date(col="col_name", start=start, end=end)
        api_value = {"col_name": {"date": {"start": start, "end": end}}}
        self.assertEqual(properties_object.result, api_value)

    def test_date_for_setting(self):
        properties_object = Properties()
        properties_object.set_date(col="col_name")
        api_value = {"col_name": {"date": {}}}
        self.assertEqual(properties_object.result, api_value)

    def test_files(self):
        properties_object = Properties()
        properties_object.set_files(col="col_name", files_list=["www.google.com/file.txt"])
        api_value = {'col_name': {'files': [{'external': {'url': 'www.google.com/file.txt'},
                                             'name': 'file.txt',
                                             'type': 'external'}]}}
        self.assertEqual(properties_object.result, api_value)

    def test_files_for_setting(self):
        properties_object = Properties()
        properties_object.set_files(col="col_name")
        api_value = {"col_name": {'files': {}}}
        self.assertEqual(properties_object.result, api_value)


if __name__ == '__main__':
    unittest.main()
