"""
Notion Pages API  –  https://developers.notion.com/reference/page
"""
from typing import Any, Dict, List, Optional

from notion_database.http.client import HttpClient


class PagesAPI:
    """1-to-1 mapping of the Notion Pages REST endpoints.

    All methods accept plain Python dicts / lists that match the Notion API
    request body schema, and return the raw Notion API response dict.

    Reference: https://developers.notion.com/reference/page
    """

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    # ------------------------------------------------------------------
    # GET /pages/{page_id}
    # ------------------------------------------------------------------

    def retrieve(
        self,
        page_id: str,
        *,
        filter_properties: Optional[List[str]] = None,
    ) -> Dict:
        """Retrieve a page by ID.

        Args:
            page_id: The ID of the page to retrieve.
            filter_properties: List of property names/IDs to include.
                Reduces response payload size.

        Returns:
            Notion page object.

        Reference: https://developers.notion.com/reference/retrieve-a-page
        """
        params: Dict[str, Any] = {}
        if filter_properties:
            params["filter_properties"] = filter_properties
        return self._http.get(f"/pages/{page_id}", params=params or None)

    # ------------------------------------------------------------------
    # GET /pages/{page_id}/properties/{property_id}
    # ------------------------------------------------------------------

    def retrieve_property(
        self,
        page_id: str,
        property_id: str,
        *,
        page_size: int = 100,
        start_cursor: Optional[str] = None,
    ) -> Dict:
        """Retrieve a specific property item of a page.

        Useful for properties that contain more values than the inline page
        object can carry (e.g. long relation lists, rollup arrays, rich-text
        properties that exceed the inline limit).

        Args:
            page_id: The page containing the property.
            property_id: The property ID or name.
            page_size: Number of items per page (1-100).
            start_cursor: Cursor for pagination.

        Returns:
            Property item object or a paginated list of property item objects.

        Reference: https://developers.notion.com/reference/retrieve-a-page-property
        """
        params: Dict[str, Any] = {"page_size": page_size}
        if start_cursor is not None:
            params["start_cursor"] = start_cursor
        return self._http.get(f"/pages/{page_id}/properties/{property_id}", params=params)

    # ------------------------------------------------------------------
    # POST /pages
    # ------------------------------------------------------------------

    def create(
        self,
        parent: Dict,
        properties: Dict[str, Dict],
        *,
        children: Optional[List[Dict]] = None,
        icon: Optional[Dict] = None,
        cover: Optional[Dict] = None,
        timezone: Optional[str] = None,
    ) -> Dict:
        """Create a new page.

        Args:
            parent: Parent object.  For database children:
                ``{"type": "database_id", "database_id": "..."}``.
                For page children:
                ``{"type": "page_id", "page_id": "..."}``.
            properties: Page property values dict.  Keys are property names
                matching the parent database schema.  Build values with
                :class:`~notion_database.models.properties.PropertyValue`.
            children: Initial page content as a list of block objects.
                Build with :class:`~notion_database.models.blocks.BlockContent`.
            icon: Icon object.
            cover: Cover object.
            timezone: IANA timezone string used when resolving template
                variables such as ``@now`` and ``@today``
                (e.g. ``"Asia/Seoul"``).  Defaults to the authorizing
                user's timezone for public integrations, or UTC for
                internal integrations.

        Returns:
            Newly created Notion page object.

        Reference: https://developers.notion.com/reference/post-page
        """
        body: Dict[str, Any] = {
            "parent": parent,
            "properties": properties,
        }
        if children is not None:
            body["children"] = children
        if icon is not None:
            body["icon"] = icon
        if cover is not None:
            body["cover"] = cover
        if timezone is not None:
            body["timezone"] = timezone
        return self._http.post("/pages", body)

    # ------------------------------------------------------------------
    # PATCH /pages/{page_id}
    # ------------------------------------------------------------------

    def update(
        self,
        page_id: str,
        *,
        properties: Optional[Dict[str, Any]] = None,
        archived: Optional[bool] = None,
        icon: Optional[Any] = None,
        cover: Optional[Any] = None,
        in_trash: Optional[bool] = None,
    ) -> Dict:
        """Update a page's properties, icon, cover, or archived status.

        Args:
            page_id: The page to update.
            properties: Partial property values dict.  Omitted keys are
                left unchanged.
            archived: Set to ``True`` to archive (soft-delete) the page,
                ``False`` to restore it.
            icon: New icon object, or ``None`` to remove.
            cover: New cover object, or ``None`` to remove.
            in_trash: Set to ``True`` to move to trash.

        Returns:
            Updated Notion page object.

        Reference: https://developers.notion.com/reference/patch-page
        """
        body: Dict[str, Any] = {}
        if properties is not None:
            body["properties"] = properties
        # Notion API 2026-03-11 replaced `archived` with `in_trash`.
        # Fall back to `archived` only when `in_trash` is not set, for
        # compatibility with older API versions.
        if archived is not None and in_trash is None:
            body["in_trash"] = archived
        if icon is not None:
            body["icon"] = icon
        if cover is not None:
            body["cover"] = cover
        if in_trash is not None:
            body["in_trash"] = in_trash
        return self._http.patch(f"/pages/{page_id}", body)

    def archive(self, page_id: str, *, archived: bool = True) -> Dict:
        """Archive (trash) or restore a page.

        Convenience wrapper around :meth:`update`.  In Notion API 2026-03-11
        this maps to ``in_trash``; older versions used ``archived``.

        Args:
            page_id: The page to archive/restore.
            archived: ``True`` to move to trash, ``False`` to restore.

        Returns:
            Updated Notion page object.
        """
        return self.update(page_id, in_trash=archived)

    # ------------------------------------------------------------------
    # GET /pages/{page_id}/markdown  (Notion-Version: 2026-03-11)
    # ------------------------------------------------------------------

    def retrieve_markdown(
        self,
        page_id: str,
        *,
        include_transcript: bool = False,
    ) -> Dict:
        """Retrieve a page's full content rendered as enhanced Markdown.

        Returns a ``page_markdown`` object.  For very large pages
        (20 000+ blocks) the ``truncated`` field will be ``true`` and
        ``unknown_block_ids`` will list block IDs that were omitted.

        Args:
            page_id: The ID of the page to retrieve.
            include_transcript: When ``True``, meeting-note transcript
                content is included in full.  When ``False`` (default) a
                placeholder with the meeting-note URL is used instead.

        Returns:
            ``{"type": "page_markdown", "page_id": "...", "markdown": "...",
            "truncated": bool, "unknown_block_ids": [...]}``

        Reference: https://developers.notion.com/reference/retrieve-page-markdown
        """
        params: Dict[str, Any] = {}
        if include_transcript:
            params["include_transcript"] = "true"
        return self._http.get(f"/pages/{page_id}/markdown", params=params or None)

    # ------------------------------------------------------------------
    # PATCH /pages/{page_id}/markdown  (Notion-Version: 2026-03-11)
    # ------------------------------------------------------------------

    def update_markdown(
        self,
        page_id: str,
        markdown: str,
        *,
        allow_deleting_content: bool = False,
    ) -> Dict:
        """Replace a page's entire content with the provided Markdown.

        Args:
            page_id: The ID of the page whose content to replace.
            markdown: Enhanced Markdown string to write as the page body.
            allow_deleting_content: Set to ``True`` to allow the operation to
                delete child pages or databases that are not referenced in the
                new Markdown content.

        Returns:
            Updated Notion page object.

        Reference: https://developers.notion.com/reference/update-page-markdown
        """
        replace_content: Dict[str, Any] = {"new_str": markdown}
        if allow_deleting_content:
            replace_content["allow_deleting_content"] = True
        return self._http.patch(
            f"/pages/{page_id}/markdown",
            {"type": "replace_content", "replace_content": replace_content},
        )
