"""
Notion Databases API  –  https://developers.notion.com/reference/database
"""
from typing import Any, Dict, List, Optional

from notion_database.http.client import HttpClient


class DatabasesAPI:
    """1-to-1 mapping of the Notion Databases REST endpoints.

    All methods accept plain Python dicts / lists that match the Notion API
    request body schema, and return the raw Notion API response dict.

    Reference: https://developers.notion.com/reference/database
    """

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    # ------------------------------------------------------------------
    # GET /databases/{database_id}
    # ------------------------------------------------------------------

    def retrieve(self, database_id: str) -> Dict:
        """Retrieve a database by ID.

        Args:
            database_id: The ID of the database to retrieve.

        Returns:
            Notion database object.

        Reference: https://developers.notion.com/reference/retrieve-a-database
        """
        return self._http.get(f"/databases/{database_id}")

    # ------------------------------------------------------------------
    # POST /databases/{database_id}/query
    # ------------------------------------------------------------------

    def query(
        self,
        database_id: str,
        *,
        filter: Optional[Dict] = None,
        sorts: Optional[List[Dict]] = None,
        start_cursor: Optional[str] = None,
        page_size: int = 100,
        filter_properties: Optional[List[str]] = None,
    ) -> Dict:
        """Query a database and return a page of results.

        Args:
            database_id: The database to query.
            filter: A filter object.  Use :class:`~notion_database.models.filters.Filter`
                to build one, or pass a raw dict matching the Notion API schema.
            sorts: A list of sort objects.  Use :class:`~notion_database.models.sorts.Sort`
                to build them.
            start_cursor: Cursor returned by a previous query for pagination.
            page_size: Number of results per page (1-100).  Defaults to 100.
            filter_properties: List of property names/IDs to include in the
                response page objects.  Reduces response payload size.

        Returns:
            Notion list object with ``results``, ``has_more``, and
            ``next_cursor`` fields.

        Reference: https://developers.notion.com/reference/post-database-query
        """
        body: Dict[str, Any] = {"page_size": page_size}
        if filter is not None:
            body["filter"] = filter
        if sorts is not None:
            body["sorts"] = sorts
        if start_cursor is not None:
            body["start_cursor"] = start_cursor
        if filter_properties is not None:
            body["filter_properties"] = filter_properties
        return self._http.post(f"/databases/{database_id}/query", body)

    def query_all(
        self,
        database_id: str,
        *,
        filter: Optional[Dict] = None,
        sorts: Optional[List[Dict]] = None,
        filter_properties: Optional[List[str]] = None,
    ) -> List[Dict]:
        """Query a database and automatically paginate to return **all** pages.

        Args:
            database_id: The database to query.
            filter: A filter object.
            sorts: A list of sort objects.
            filter_properties: Property names/IDs to include in page objects.

        Returns:
            A flat list of all matching Notion page objects.
        """
        pages: List[Dict] = []
        cursor: Optional[str] = None
        while True:
            response = self.query(
                database_id,
                filter=filter,
                sorts=sorts,
                start_cursor=cursor,
                filter_properties=filter_properties,
            )
            pages.extend(response.get("results", []))
            if not response.get("has_more"):
                break
            cursor = response.get("next_cursor")
        return pages

    # ------------------------------------------------------------------
    # POST /databases
    # ------------------------------------------------------------------

    def create(
        self,
        parent: Dict,
        title: List[Dict],
        properties: Dict[str, Dict],
        *,
        icon: Optional[Dict] = None,
        cover: Optional[Dict] = None,
        is_inline: bool = False,
        description: Optional[List[Dict]] = None,
    ) -> Dict:
        """Create a new database as a child of a page.

        Args:
            parent: Parent object, e.g. ``{"type": "page_id", "page_id": "..."}``.
            title: Rich-text array for the database title.
                Use :class:`~notion_database.models.rich_text.RichText` to build.
            properties: Database property schema dict where keys are column
                names and values are property schema objects.
                Use :class:`~notion_database.models.properties.PropertySchema`
                to build individual schemas.
            icon: Icon object.  Use :class:`~notion_database.models.icons.Icon`.
            cover: Cover object.  Use :class:`~notion_database.models.icons.Cover`.
            is_inline: Whether the database appears inline on its parent page.
            description: Rich-text array for the database description.

        Returns:
            Newly created Notion database object.

        Reference: https://developers.notion.com/reference/create-a-database
        """
        body: Dict[str, Any] = {
            "parent": parent,
            "title": title,
            "properties": properties,
            "is_inline": is_inline,
        }
        if icon is not None:
            body["icon"] = icon
        if cover is not None:
            body["cover"] = cover
        if description is not None:
            body["description"] = description
        return self._http.post("/databases", body)

    # ------------------------------------------------------------------
    # PATCH /databases/{database_id}
    # ------------------------------------------------------------------

    def update(
        self,
        database_id: str,
        *,
        title: Optional[List[Dict]] = None,
        description: Optional[List[Dict]] = None,
        properties: Optional[Dict[str, Any]] = None,
        icon: Optional[Any] = None,
        cover: Optional[Any] = None,
    ) -> Dict:
        """Update an existing database.

        Pass ``None`` as a property value to remove it from the schema.

        Args:
            database_id: The database to update.
            title: New rich-text title array.
            description: New rich-text description array.
            properties: Partial property schema dict.  Set a key to ``None``
                to remove that property from the schema.
            icon: New icon object, or ``None`` to remove.
            cover: New cover object, or ``None`` to remove.

        Returns:
            Updated Notion database object.

        Reference: https://developers.notion.com/reference/update-a-database
        """
        body: Dict[str, Any] = {}
        if title is not None:
            body["title"] = title
        if description is not None:
            body["description"] = description
        if properties is not None:
            body["properties"] = properties
        if icon is not None:
            body["icon"] = icon
        if cover is not None:
            body["cover"] = cover
        return self._http.patch(f"/databases/{database_id}", body)
