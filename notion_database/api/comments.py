"""
Notion Comments API  –  https://developers.notion.com/reference/comment-object
"""
from typing import Any, Dict, List, Optional

from notion_database.http.client import HttpClient


class CommentsAPI:
    """1-to-1 mapping of the Notion Comments REST endpoints.

    Reference: https://developers.notion.com/reference/comment-object
    """

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def retrieve(
        self,
        block_id: str,
        *,
        start_cursor: Optional[str] = None,
        page_size: int = 100,
    ) -> Dict:
        """Retrieve comments associated with a page or block.

        Args:
            block_id: The page or block ID to retrieve comments for.
            start_cursor: Cursor for pagination.
            page_size: Number of results per page (1-100).

        Returns:
            Notion list object with comment objects.

        Reference: https://developers.notion.com/reference/retrieve-a-comment
        """
        params: Dict[str, Any] = {
            "block_id": block_id,
            "page_size": page_size,
        }
        if start_cursor is not None:
            params["start_cursor"] = start_cursor
        return self._http.get("/comments", params=params)

    def create(
        self,
        parent: Dict,
        rich_text: List[Dict],
        *,
        discussion_id: Optional[str] = None,
    ) -> Dict:
        """Create a new comment on a page or existing discussion thread.

        Args:
            parent: Parent object.  For page-level comments:
                ``{"page_id": "..."}``.
            rich_text: The comment body as a rich-text array.  Build with
                :class:`~notion_database.models.rich_text.RichText`.
            discussion_id: If set, adds the comment to an existing discussion
                thread instead of creating a new one.

        Returns:
            Newly created Notion comment object.

        Reference: https://developers.notion.com/reference/create-a-comment
        """
        body: Dict[str, Any] = {
            "parent": parent,
            "rich_text": rich_text,
        }
        if discussion_id is not None:
            body["discussion_id"] = discussion_id
        return self._http.post("/comments", body)
