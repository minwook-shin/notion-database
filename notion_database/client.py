"""
NotionClient  –  single entry point for the notion-database package.
"""
from notion_database.api.blocks import BlocksAPI
from notion_database.api.comments import CommentsAPI
from notion_database.api.databases import DatabasesAPI
from notion_database.api.pages import PagesAPI
from notion_database.api.search import SearchAPI
from notion_database.api.users import UsersAPI
from notion_database.http.client import HttpClient


class NotionClient:
    """Notion API client.

    Provides access to all Notion REST API resources through namespaced
    sub-clients.  Each sub-client exposes methods that map 1-to-1 to the
    corresponding Notion API endpoints.

    Args:
        token: Notion Internal Integration token (``secret_...``).

    Example::

        from notion_database import NotionClient, PropertyValue, BlockContent

        client = NotionClient("secret_xxx")

        # Retrieve a database
        db = client.databases.retrieve("database-id")

        # Query with filter and sort
        from notion_database import Filter, Sort
        results = client.databases.query(
            "database-id",
            filter=Filter.select("Status").equals("Active"),
            sorts=[Sort.by_property("Name")],
        )

        # Create a page
        page = client.pages.create(
            parent={"database_id": "database-id"},
            properties={
                "Name":   PropertyValue.title("Hello, Notion 2.0!"),
                "Status": PropertyValue.select("Active"),
            },
            children=[
                BlockContent.heading_1("Introduction"),
                BlockContent.paragraph("This page was created via notion-database 2.0."),
            ],
        )

        # Append blocks to a page
        client.blocks.append_children(
            page["id"],
            children=[BlockContent.divider(), BlockContent.paragraph("The end.")],
        )

    Attributes:
        databases: :class:`~notion_database.api.databases.DatabasesAPI` –
            retrieve, query, create, update databases.
        pages: :class:`~notion_database.api.pages.PagesAPI` –
            retrieve, create, update, archive pages.
        blocks: :class:`~notion_database.api.blocks.BlocksAPI` –
            retrieve, append, update, delete blocks.
        search: :class:`~notion_database.api.search.SearchAPI` –
            search pages and databases.
        users: :class:`~notion_database.api.users.UsersAPI` –
            retrieve and list workspace users.
        comments: :class:`~notion_database.api.comments.CommentsAPI` –
            retrieve and create comments.
    """

    def __init__(self, token: str) -> None:
        http = HttpClient(token)
        self.databases: DatabasesAPI = DatabasesAPI(http)
        self.pages: PagesAPI = PagesAPI(http)
        self.blocks: BlocksAPI = BlocksAPI(http)
        self.search: SearchAPI = SearchAPI(http)
        self.users: UsersAPI = UsersAPI(http)
        self.comments: CommentsAPI = CommentsAPI(http)

    def __repr__(self) -> str:
        return "NotionClient()"
