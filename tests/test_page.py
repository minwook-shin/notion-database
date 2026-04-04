import unittest
from unittest.mock import MagicMock, patch

from notion_database.page import Page


class TestPageMethods(unittest.TestCase):
    def setUp(self):
        self.page = Page(integrations_token="test-token")

    @patch("notion_database.components.request.requests.get")
    def test_retrieve_page_property(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "object": "property_item",
            "type": "relation",
            "relation": {"id": "page-id-1"}
        }
        mock_get.return_value = mock_response

        result = self.page.retrieve_page_property(
            page_id="test-page-id",
            property_id="test-property-id"
        )

        mock_get.assert_called_once()
        call_url = mock_get.call_args[0][0]
        self.assertIn("test-page-id", call_url)
        self.assertIn("test-property-id", call_url)
        self.assertEqual(result["type"], "relation")

    @patch("notion_database.components.request.requests.get")
    def test_retrieve_page_property_with_pagination(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "object": "list",
            "results": [
                {"object": "property_item", "type": "relation", "relation": {"id": "page-id-1"}},
                {"object": "property_item", "type": "relation", "relation": {"id": "page-id-2"}}
            ],
            "next_cursor": None,
            "has_more": False,
            "property_item": {"id": "test-property-id", "type": "relation", "relation": {}}
        }
        mock_get.return_value = mock_response

        result = self.page.retrieve_page_property(
            page_id="test-page-id",
            property_id="test-property-id",
            start_cursor="some-cursor"
        )

        call_url = mock_get.call_args[0][0]
        self.assertIn("start_cursor=some-cursor", call_url)
        self.assertEqual(len(result["results"]), 2)

    @patch("notion_database.components.request.requests.get")
    def test_retrieve_page_property_with_page_size(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {"object": "list", "results": []}
        mock_get.return_value = mock_response

        self.page.retrieve_page_property(
            page_id="test-page-id",
            property_id="test-property-id",
            page_size=10
        )

        call_url = mock_get.call_args[0][0]
        self.assertIn("page_size=10", call_url)


if __name__ == '__main__':
    unittest.main()
