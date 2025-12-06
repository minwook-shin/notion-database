"""
Notion API Database
"""
from typing import Dict, List

from notion_database.utils import deprecate

from notion_database.service.properties import Properties
from notion_database.components.request import Request

from notion_database.service.cover import Cover
from notion_database.service.icon import Icon


class Database:
    """
    Notion API Database class
    """
    def __init__(self, integrations_token: str):
        """
        init

        :param integrations_token: Notion Internal Integration Token
        """
        self.properties_list: List[Dict] = []
        self.url: str = 'https://api.notion.com/v1/databases'
        self.result: Dict = {}
        self.request: Request = Request(self.url, integrations_token=integrations_token)

    def retrieve_database(self, database_id: str, get_properties: bool = False):
        """
        Retrieve a database

        :param database_id: Identifier for a Notion database
        :param get_properties: Get properties_list trigger
        :return:
        """
        self.result = self.request.call_api_get(self.url + "/" + database_id)
        if get_properties:
            self.properties_list.clear()
            for property_value in self.result["properties"].values():
                if property_value["id"] == "title":
                    # property type of the title cannot be changed.
                    continue
                self.properties_list.append(property_value)

    @deprecate.deprecated_warn
    def query_database(self):
        """
        (deprecated) query database

        move to run_query_database function
        """

    def run_query_database(self, database_id: str, db_filter: Dict = None, db_sort: Dict = None):
        """
        Gets a list of Pages contained in the database
        :param database_id: Identifier for a Notion database
        :param db_sort: Sorts are similar to the sorts provided in the Notion UI
        :param db_filter: Filters are similar to the filters provided in the Notion UI
        :return:
        """
        body = {}
        if db_filter:
            body["filter"] = db_filter
        if db_sort:
            body["sorts"] = [db_sort]
        self.result = self.request.call_api_post(self.url + "/" + database_id + "/query", body)

    def find_all_page(self, database_id: str, page_size: int = 100, start_cursor: str = None):
        """
        find all database page
        :param database_id: Identifier for a Notion database
        :param page_size: The number of items from the full list desired in the response.
        :param start_cursor: returns a page of results starting after the cursor provided.
        """
        if start_cursor:
            body = {
                "sorts": [],
                "start_cursor": start_cursor,
                "page_size": page_size
            }
        else:
            body = {
                "sorts": [],
                "page_size": page_size
            }
        self.result = self.request.call_api_post(self.url + "/" + database_id + "/query", body)

    @deprecate.deprecated_warn
    def list_databases(self, page_size:int =100):
        """
        List databases ('This API is deprecated.')

        :param page_size: The number of items from the full list desired in the response.
        :return:
        """
        url = self.url + f"?page_size={str(page_size)}"
        self.result = self.request.call_api_get(url)

    def create_database(self, page_id: str, title:str,
                        properties: Properties = None, cover: Cover = None, icon: Icon = None, is_inline: bool = False):
        """
        Create a database

        :param page_id: Notion Page ID
        :param title: Title of database as it appears in Notion
        :param properties: Property schema of database
        :param cover:
        :param icon:
        :param is_inline: Shows the database inline of the parent page
        :return:
        """
        if properties is None:
            properties = Properties()
        body = {
            "parent": {
                "type": "page_id",
                "page_id": page_id
            },
            "is_inline": is_inline,
            "title": [
                {
                    "type": "text",
                    "text": {
                        "content": title,
                        "link": None
                    }
                }
            ],
            "properties": properties.result
        }
        if cover:
            body.update(cover.result)
        if icon:
            body.update(icon.result)
        self.result = self.request.call_api_post(self.url, body)

    def update_database(self, database_id: str, title: str = None,
                        remove_properties=None, add_properties=None,
                        cover: Cover = None, icon: Icon = None):
        """
        Update database

        :param database_id: Identifier for a Notion database
        :param title: Title of database as it appears in Notion
        :param remove_properties: Removal Property schema of database
        :param add_properties: Property schema of database
        :param cover:
        :param icon:
        :return:
        """
        if add_properties is None:
            add_properties = Properties()
        body = {
            "properties": {}
        }
        if title:
            body["title"] = [
                {
                    "type": "text",
                    "text": {
                        "content": title,
                        "link": None
                    }
                }
            ]
        if cover:
            body.update(cover.result)
        if icon:
            body.update(icon.result)
        if remove_properties:
            body["properties"].update({i["id"]: None for i in remove_properties})
            self.result = self.request.call_api_patch(self.url + "/" + database_id, body)
            body["properties"] = {}
        if add_properties:
            body["properties"].update(add_properties.result)
            self.result = self.request.call_api_patch(self.url + "/" + database_id, body)
            body["properties"] = {}
