"""
Notion API Page
"""
import logging
from typing import Dict, Optional

from notion_database.children import Children
from notion_database.properties import Properties
from notion_database.components.request import Request

from notion_database.cover import Cover
from notion_database.icon import Icon

LOGGER = logging.getLogger("Notion-Database")


class Page:
    """
    Notion API Page class
    """
    def __init__(self, integrations_token: str):
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

    def retrieve_page_property(self, page_id: str, property_id: str,
                               page_size: int = 100, start_cursor: Optional[str] = None) -> dict:
        """
        Retrieve a page property item.

        For paginated properties such as relation, rich_text, title, and people,
        the Notion API returns truncated results in database queries.
        Use this method to retrieve the full property value.

        :param page_id: Identifier for a Notion page
        :param property_id: Identifier for a Notion property (ID or name)
        :param page_size: The number of items from the full list desired in the response.
        :param start_cursor: Returns a page of results starting after the cursor provided.
        :return: Property item or property item list dict
        """
        url = self.url + "/" + page_id + "/properties/" + property_id
        params = []
        if start_cursor:
            params.append(f"start_cursor={start_cursor}")
        if page_size != 100:
            params.append(f"page_size={page_size}")
        if params:
            url = url + "?" + "&".join(params)
        return self.request.call_api_get(url)

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
