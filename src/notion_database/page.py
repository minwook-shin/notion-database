import logging

from notion_database.children import Children
from notion_database.properties import Properties
from notion_database.request import Request

LOGGER = logging.getLogger("Notion-Database")


class Page:
    def __init__(self, integrations_token):
        """
        init

        :param integrations_token: Notion Internal Integration Token
        """
        self.url = 'https://api.notion.com/v1/pages'
        self.result = {}
        self.request = Request(self.url, integrations_token=integrations_token)

    def retrieve_page(self, page_id):
        """
        Retrieve a page

        :param page_id: Identifier for a Notion page
        :return:
        """
        self.result = self.request.call_api_get(self.url + "/" + page_id)

    def create_page(self, database_id, properties=None, children=None):
        """
        Create a page

        :param database_id: Identifier for a Notion database
        :param properties: Property values of this page
        :param children: Page content for the new page
        :return:
        """
        if children is None:
            children = Children()
        if properties is None:
            properties = Properties()
        properties = properties
        children = children
        body = {
            "parent": {
                "database_id": database_id
            },
            "properties": properties.result,
            "children": children.result
        }
        self.result = self.request.call_api_post(self.url, body)

        self.check_field()

    def update_page(self, page_id, properties=None):
        """
        Update page

        :param page_id: Identifier for a Notion page
        :param properties: Property values to update for this page
        :return:
        """
        if properties is None:
            properties = Properties()
        body = {
            "properties": properties.result,
        }
        self.result = self.request.call_api_patch(self.url + "/" + page_id, body)

        self.check_field()

    def archive_page(self, page_id, archived):
        """
        Archive page

        :param page_id: Identifier for a Notion page
        :param archived: Set to archive a page.
        :return:
        """
        body = {
            "archived": archived,
        }
        self.result = self.request.call_api_patch(self.url + "/" + page_id, body)

        self.check_field()

    def check_field(self):
        """
        Check the Object Error

        :return:
        """
        if self.result["object"] == "error":
            LOGGER.error(self.result["message"])
            raise ValueError(self.result["code"])
