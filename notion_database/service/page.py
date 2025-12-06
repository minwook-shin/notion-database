"""
Notion API Page
"""
import logging
from typing import Dict

from notion_database.service.children import Children
from notion_database.service.properties import Properties
from notion_database.components.request import Request

from notion_database.service.cover import Cover
from notion_database.service.icon import Icon

LOGGER = logging.getLogger("Notion-Database")


class Page:
    """
    Notion API Page class
    """
    def __init__(self, integrations_token):
        """
        init

        :param integrations_token: Notion Internal Integration Token
        """
        self.url: str = 'https://api.notion.com/v1/pages'
        self.result: Dict = {}
        self.request: Request = Request(self.url, integrations_token=integrations_token)

    def retrieve_page(self, page_id: str):
        """
        Retrieve a page

        :param page_id: Identifier for a Notion page
        :return:
        """
        self.result = self.request.call_api_get(self.url + "/" + page_id)

    def create_page(self, database_id: str, properties: Properties = None,
                    children: Children = None, cover: Cover = None, icon: Icon = None):
        """
        Create a page

        :param database_id: Identifier for a Notion database
        :param properties: Property values of this page
        :param children: Page content for the new page
        :param cover:
        :param icon:
        :return:
        """
        if children is None:
            children = Children()
        if properties is None:
            properties = Properties()
        body = {
            "parent": {
                "database_id": database_id
            },
            "properties": properties.result,
            "children": children.result
        }
        if cover:
            body.update(cover.result)
        if icon:
            body.update(icon.result)
        self.result = self.request.call_api_post(self.url, body)

        self.check_field()

    def update_page(self, page_id: str, properties: Properties = None,
                    cover: Cover = None, icon: Icon = None):
        """
        Update page

        :param page_id: Identifier for a Notion page
        :param properties: Property values to update for this page
        :param cover:
        :param icon:
        :return:
        """
        if properties is None:
            properties = Properties()
        body = {
            "properties": properties.result,
        }
        if cover:
            body.update(cover.result)
        if icon:
            body.update(icon.result)
        self.result = self.request.call_api_patch(self.url + "/" + page_id, body)

        self.check_field()

    def archive_page(self, page_id: str, archived: bool):
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
