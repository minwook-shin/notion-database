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

    @staticmethod
    def search_pages(integrations_token: str,
                     sort: Dict, query: str = "", page_size: int = 100, start_cursor: str = None):
        search = Search(integrations_token=integrations_token)
        search.search_pages(query=query, sort=sort, page_size=page_size, start_cursor=start_cursor)
        return search.result
