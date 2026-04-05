"""
Notion Blocks API  –  https://developers.notion.com/reference/block
"""
from typing import Any, Dict, List, Optional

from notion_database.http.client import HttpClient


class BlocksAPI:
    """1-to-1 mapping of the Notion Blocks REST endpoints.

    All methods accept plain Python dicts / lists that match the Notion API
    request body schema, and return the raw Notion API response dict.

    Reference: https://developers.notion.com/reference/block
    """

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    # ------------------------------------------------------------------
    # GET /blocks/{block_id}
    # ------------------------------------------------------------------

    def retrieve(self, block_id: str) -> Dict:
        """Retrieve a block by ID.

        Args:
            block_id: The ID of the block to retrieve.

        Returns:
            Notion block object.

        Reference: https://developers.notion.com/reference/retrieve-a-block
        """
        return self._http.get(f"/blocks/{block_id}")

    # ------------------------------------------------------------------
    # GET /blocks/{block_id}/children
    # ------------------------------------------------------------------

    def retrieve_children(
        self,
        block_id: str,
        *,
        start_cursor: Optional[str] = None,
        page_size: int = 100,
    ) -> Dict:
        """Retrieve the immediate children of a block or page.

        Args:
            block_id: The parent block or page ID.
            start_cursor: Cursor for pagination.
            page_size: Number of results per page (1-100).

        Returns:
            Notion list object with ``results``, ``has_more``, and
            ``next_cursor`` fields.

        Reference: https://developers.notion.com/reference/get-block-children
        """
        params: Dict[str, Any] = {"page_size": page_size}
        if start_cursor is not None:
            params["start_cursor"] = start_cursor
        return self._http.get(f"/blocks/{block_id}/children", params=params)

    def retrieve_all_children(self, block_id: str) -> List[Dict]:
        """Retrieve **all** children of a block, automatically paginating.

        Args:
            block_id: The parent block or page ID.

        Returns:
            A flat list of all child block objects.
        """
        blocks: List[Dict] = []
        cursor: Optional[str] = None
        while True:
            response = self.retrieve_children(block_id, start_cursor=cursor)
            blocks.extend(response.get("results", []))
            if not response.get("has_more"):
                break
            cursor = response.get("next_cursor")
        return blocks

    # ------------------------------------------------------------------
    # PATCH /blocks/{block_id}/children
    # ------------------------------------------------------------------

    def append_children(self, block_id: str, children: List[Dict]) -> Dict:
        """Append new block children to a block or page.

        Args:
            block_id: The parent block or page ID to append to.
            children: List of block objects to append.  Build with
                :class:`~notion_database.models.blocks.BlockContent`.

        Returns:
            Notion list object containing the newly appended block objects.

        Reference: https://developers.notion.com/reference/patch-block-children
        """
        return self._http.patch(f"/blocks/{block_id}/children", {"children": children})

    # ------------------------------------------------------------------
    # PATCH /blocks/{block_id}
    # ------------------------------------------------------------------

    def update(self, block_id: str, block: Dict) -> Dict:
        """Update the content of a block.

        The ``block`` dict should contain only the fields to change.  Refer to
        the Notion API docs for the per-type update schema.

        Args:
            block_id: The block to update.
            block: Partial block object with the fields to change.

        Returns:
            Updated Notion block object.

        Reference: https://developers.notion.com/reference/update-a-block
        """
        return self._http.patch(f"/blocks/{block_id}", block)

    # ------------------------------------------------------------------
    # DELETE /blocks/{block_id}
    # ------------------------------------------------------------------

    def delete(self, block_id: str) -> Dict:
        """Delete (archive) a block.

        Args:
            block_id: The block to delete.

        Returns:
            Deleted Notion block object with ``archived: true``.

        Reference: https://developers.notion.com/reference/delete-a-block
        """
        return self._http.delete(f"/blocks/{block_id}")
