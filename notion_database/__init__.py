"""
notion-database  –  Python client for the Notion API

Quick start::

    from notion_database import NotionClient, PropertyValue, BlockContent, Filter, Sort

    client = NotionClient("secret_xxx")

    # Query a database
    results = client.databases.query(
        "database-id",
        filter=Filter.select("Status").equals("Active"),
        sorts=[Sort.descending("CreatedAt")],
    )

    # Create a page
    page = client.pages.create(
        parent={"database_id": "database-id"},
        properties={
            "Name": PropertyValue.title("Hello, Notion!"),
        },
        children=[BlockContent.paragraph("Page created with notion-database 2.0")],
    )
"""
from notion_database.client import NotionClient
from notion_database.exceptions import (
    NotionAPIError,
    NotionConflictError,
    NotionError,
    NotionForbiddenError,
    NotionInternalError,
    NotionNotFoundError,
    NotionRateLimitError,
    NotionUnauthorizedError,
    NotionValidationError,
)
from notion_database.models.blocks import BlockContent
from notion_database.models.filters import Filter
from notion_database.models.icons import Cover, Icon
from notion_database.models.properties import PropertySchema, PropertyValue
from notion_database.models.rich_text import RichText
from notion_database.models.sorts import Sort

NOTION_VERSION = "2026-03-11"
__version__ = "2.0.0rc1"

__all__ = [
    # Client
    "NotionClient",
    # Builders
    "PropertyValue",
    "PropertySchema",
    "BlockContent",
    "RichText",
    "Filter",
    "Sort",
    "Icon",
    "Cover",
    # Exceptions
    "NotionError",
    "NotionAPIError",
    "NotionValidationError",
    "NotionUnauthorizedError",
    "NotionForbiddenError",
    "NotionNotFoundError",
    "NotionConflictError",
    "NotionRateLimitError",
    "NotionInternalError",
    # Constants
    "NOTION_VERSION",
    "__version__",
]
