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
        in_trash: Optional[bool] = None,
        result_type: Optional[str] = None,
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
            in_trash: When ``True``, only return trashed pages.  When ``False``,
                only return non-trashed pages.  Omit to return all.
            result_type: Filter results by type.  One of ``"page"`` or
                ``"data_source"`` (for databases embedded as data sources).

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
        if in_trash is not None:
            body["in_trash"] = in_trash
        if result_type is not None:
            body["result_type"] = result_type
        return self._http.post(f"/databases/{database_id}/query", body)

    def query_all(
        self,
        database_id: str,
        *,
        filter: Optional[Dict] = None,
        sorts: Optional[List[Dict]] = None,
        filter_properties: Optional[List[str]] = None,
        in_trash: Optional[bool] = None,
        result_type: Optional[str] = None,
    ) -> List[Dict]:
        """Query a database and automatically paginate to return **all** pages.

        Args:
            database_id: The database to query.
            filter: A filter object.
            sorts: A list of sort objects.
            filter_properties: Property names/IDs to include in page objects.
            in_trash: When ``True``, only return trashed pages.
            result_type: Filter results by type (``"page"`` or ``"data_source"``).

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
                in_trash=in_trash,
                result_type=result_type,
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
        initial_data_source: Optional[Dict] = None,
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
            initial_data_source: Optional data source configuration for
                pre-populating the database with data on creation
                (Notion-Version: 2026-03-11).

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
        if initial_data_source is not None:
            body["initial_data_source"] = initial_data_source
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
        is_inline: Optional[bool] = None,
        in_trash: Optional[bool] = None,
        is_locked: Optional[bool] = None,
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
            is_inline: Whether the database should appear inline on its parent
                page.
            in_trash: Set to ``True`` to move the database to trash.
            is_locked: Set to ``True`` to lock the database (prevents edits
                without unlocking).

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
        if is_inline is not None:
            body["is_inline"] = is_inline
        if in_trash is not None:
            body["in_trash"] = in_trash
        if is_locked is not None:
            body["is_locked"] = is_locked
        return self._http.patch(f"/databases/{database_id}", body)
