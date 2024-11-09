from typing import Dict

from notion_database.service.search import Search


class NotionDatabase:
    """
    Notion API Database class
    """
    @staticmethod
    def search(integrations_token: str, sort: Dict, query: str = ""):
        search = Search(integrations_token=integrations_token)
        search.search_database(query=query, sort=sort)
        return search.result