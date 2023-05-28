"""
Notion API Search
"""
from typing import TypedDict, List, Dict

from notion_database.const.query import Direction, Timestamp
from notion_database.components.request import Request


class SortType(TypedDict):
    """
    Notion API Sort class
    """
    direction: Direction
    timestamp: Timestamp


class Search:
    """
    Notion API Search class
    """
    def __init__(self, integrations_token: str):
        """
        init

        :param integrations_token: Notion Internal Integration Token
        """
        self.properties_list: List = []
        self.url: str = 'https://api.notion.com/v1/search'
        self.result: Dict = {}
        self.request: Request = Request(self.url, integrations_token=integrations_token)

    def search_database(self, query: str, sort: SortType, root_only: bool = True):
        """
        Searches all original databases and child databases that are shared with the integration

        :param query: matches against the database titles.
        :param sort: sort query specifically for only databases.
        :param root_only: get only the root databases.
        :return:
        """
        self.result = self.request.call_api_post(self.url + "/", {
            "query": query, "sort": {"direction": sort["direction"].value,
                                     "timestamp": sort["timestamp"].value},
            "filter": {"value": "database", "property": "object"}
        })["results"]
        root_list = []
        if root_only:
            result = self.result
            for db_index, _ in enumerate(result):
                db_data = result[db_index]
                if db_data["parent"].get("workspace", None):
                    root_list.append(db_data)
            self.result = root_list

    def search_pages(self, query: str, sort: SortType,
                     page_size: int = 100, start_cursor: str = None):
        """
        Searches all original pages and child pages that are shared with the integration

        :param query: matches against the pages titles.
        :param sort: sort query specifically for only pages.
        :param page_size: The number of items from the full list desired in the response.
        :param start_cursor: returns a page of results starting after the cursor provided.
        :return:
        """
        if start_cursor:
            self.result = self.request.call_api_post(self.url + "/", {
                "query": query, "sort": {"direction": sort["direction"].value,
                                         "timestamp": sort["timestamp"].value},
                "filter": {"value": "page", "property": "object"},
                "page_size": page_size, "start_cursor": start_cursor
            })
        self.result = self.request.call_api_post(self.url + "/", {
            "query": query, "sort": {"direction": sort["direction"].value,
                                     "timestamp": sort["timestamp"].value},
            "filter": {"value": "page", "property": "object"}, "page_size": page_size
        })
