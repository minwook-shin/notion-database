from typing import Dict

from notion_database.service.children import Children
from notion_database.service.cover import Cover
from notion_database.service.database import Database
from notion_database.service.icon import Icon
from notion_database.service.properties import Properties
from notion_database.service.search import Search
from notion_database.service.block import Block
from notion_database.service.page import Page


class NotionDatabase:
    """
    Notion API Search, Database class
    """

    # Search
    @staticmethod
    def search_database(integrations_token: str, sort: Dict, query: str = ""):
        search = Search(integrations_token=integrations_token)
        search.search_database(query=query, sort=sort)
        return search.result

    @staticmethod
    def search_pages(integrations_token: str,
                     sort: Dict, query: str = "", page_size: int = 100, start_cursor: str = None):
        search = Search(integrations_token=integrations_token)
        search.search_pages(query=query, sort=sort, page_size=page_size, start_cursor=start_cursor)
        return search.result

    # Database
    @staticmethod
    def retrieve_database(integrations_token: str, database_id: str, get_properties: bool = False):
        db = Database(integrations_token=integrations_token)
        db.retrieve_database(database_id=database_id, get_properties=get_properties)
        return db.result

    @staticmethod
    def run_query_database(integrations_token: str, database_id: str, db_filter: Dict = None, db_sort: Dict = None):
        db = Database(integrations_token=integrations_token)
        db.run_query_database(database_id=database_id, db_filter=db_filter, db_sort=db_sort)
        return db.result

    @staticmethod
    def find_all_page(integrations_token: str, database_id: str, page_size: int = 100, start_cursor: str = None):
        db = Database(integrations_token=integrations_token)
        db.find_all_page(database_id=database_id, page_size=page_size, start_cursor=start_cursor)
        return db.result

    @staticmethod
    def list_databases(integrations_token: str):
        db = Database(integrations_token=integrations_token)
        db.list_databases()
        return db.result

    @staticmethod
    def create_database(integrations_token: str, page_id: str,
                        title: str, properties: Properties,
                        cover: Cover = None, icon: Icon = None, is_inline: bool = False):
        db = Database(integrations_token=integrations_token)
        db.create_database(page_id=page_id, title=title, properties=properties, cover=cover, icon=icon,
                           is_inline=is_inline)
        return db.result

    @staticmethod
    def update_database(integrations_token: str, database_id: str, title: str,
                        remove_properties=None, add_properties=None, cover: Cover = None, icon: Icon = None):
        db = Database(integrations_token=integrations_token)
        db.update_database(database_id=database_id, title=title,
                           remove_properties=remove_properties, add_properties=add_properties, cover=cover, icon=icon)
        return db.result

    # Block
    @staticmethod
    def retrieve_block(integrations_token: str, block_id: str, is_children: bool = False,
                       page_size: int = 100, start_cursor: str = None):
        block = Block(integrations_token=integrations_token)
        block.retrieve_block(block_id=block_id, is_children=is_children, page_size=page_size, start_cursor=start_cursor)
        return block.result

    # Page
    @staticmethod
    def retrieve_page(integrations_token: str, page_id: str):
        page = Page(integrations_token=integrations_token)
        page.retrieve_page(page_id=page_id)
        return page.result

    @staticmethod
    def create_page(integrations_token: str, database_id: str, properties: Properties = None,
                    children: Children = None, cover: Cover = None, icon: Icon = None):
        page = Page(integrations_token=integrations_token)
        page.create_page(database_id=database_id, properties=properties, children=children, cover=cover, icon=icon)
        return page.result

    @staticmethod
    def update_page(integrations_token: str, page_id: str, properties: Properties = None,
                    cover: Cover = None, icon: Icon = None):
        page = Page(integrations_token=integrations_token)
        page.update_page(page_id=page_id, properties=properties, cover=cover, icon=icon)
        return page.result

    @staticmethod
    def archive_page(integrations_token: str, page_id: str, archived: bool):
        page = Page(integrations_token=integrations_token)
        page.archive_page(page_id=page_id, archived=archived)
        return page.result
