"""
Notion Search API  –  https://developers.notion.com/reference/post-search
"""
from typing import Any, Dict, List, Optional

from notion_database.http.client import HttpClient


class SearchAPI:
    """1-to-1 mapping of the Notion Search endpoint.

    Reference: https://developers.notion.com/reference/post-search
    """

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def search(
        self,
        query: str = "",
        *,
        filter: Optional[Dict] = None,
        sort: Optional[Dict] = None,
        start_cursor: Optional[str] = None,
        page_size: int = 100,
    ) -> Dict:
        """Search all pages and databases that the integration has access to.

        Args:
            query: Text to search for.  Pass an empty string to list all
                accessible objects.
            filter: Object type filter.  ``{"value": "page", "property": "object"}``
                or ``{"value": "data_source", "property": "object"}``.
            sort: Sort criteria dict, e.g.
                ``{"direction": "ascending", "timestamp": "last_edited_time"}``.
            start_cursor: Cursor for pagination.
            page_size: Number of results per page (1-100).

        Returns:
            Notion list object with ``results``, ``has_more``, and
            ``next_cursor`` fields.

        Reference: https://developers.notion.com/reference/post-search
        """
        body: Dict[str, Any] = {
            "query": query,
            "page_size": page_size,
        }
        if filter is not None:
            body["filter"] = filter
        if sort is not None:
            body["sort"] = sort
        if start_cursor is not None:
            body["start_cursor"] = start_cursor
        return self._http.post("/search", body)

    def search_databases(
        self,
        query: str = "",
        *,
        sort: Optional[Dict] = None,
        start_cursor: Optional[str] = None,
        page_size: int = 100,
        include_archived: bool = False,
    ) -> Dict:
        """Search only databases.

        Uses the ``"data_source"`` filter value required by
        Notion-Version 2026-03-11 (the old ``"database"`` value is no longer
        accepted).  Trashed and archived results are excluded by default.

        Args:
            query: Text to search for.
            sort: Sort criteria dict.
            start_cursor: Cursor for pagination.
            page_size: Number of results per page.
            include_archived: When ``True``, include archived/trashed results.
                Defaults to ``False``.

        Returns:
            Notion list object whose ``results`` contain database objects.
        """
        response = self.search(
            query,
            filter={"value": "data_source", "property": "object"},
            sort=sort,
            start_cursor=start_cursor,
            page_size=page_size,
        )
        results = response.get("results", [])
        if not include_archived:
            results = [r for r in results if not r.get("in_trash") and not r.get("archived")]
        # In Notion-Version 2026-03-11 the search endpoint returns
        # object:"data_source" wrappers whose own `id` is NOT the database ID.
        # The real database ID lives in parent.database_id.  Normalise so that
        # callers can always use result["id"] with GET /databases/{id}.
        normalised = []
        for r in results:
            if r.get("object") == "data_source":
                parent = r.get("parent", {})
                if parent.get("type") == "database_id" and parent.get("database_id"):
                    r = dict(r)
                    r["id"] = parent["database_id"]
            normalised.append(r)
        response["results"] = normalised
        return response

    def search_pages(
        self,
        query: str = "",
        *,
        sort: Optional[Dict] = None,
        start_cursor: Optional[str] = None,
        page_size: int = 100,
    ) -> Dict:
        """Search only pages.

        Convenience wrapper around :meth:`search` with the page filter
        pre-applied.

        Args:
            query: Text to search for.
            sort: Sort criteria dict.
            start_cursor: Cursor for pagination.
            page_size: Number of results per page.

        Returns:
            Notion list object containing only page objects.
        """
        return self.search(
            query,
            filter={"value": "page", "property": "object"},
            sort=sort,
            start_cursor=start_cursor,
            page_size=page_size,
        )

    def search_all(
        self,
        query: str = "",
        *,
        filter: Optional[Dict] = None,
        sort: Optional[Dict] = None,
    ) -> List[Dict]:
        """Search and automatically paginate to return **all** matching results.

        Args:
            query: Text to search for.
            filter: Object type filter.
            sort: Sort criteria dict.

        Returns:
            A flat list of all matching Notion objects.
        """
        results: List[Dict] = []
        cursor: Optional[str] = None
        while True:
            response = self.search(query, filter=filter, sort=sort, start_cursor=cursor)
            results.extend(response.get("results", []))
            if not response.get("has_more"):
                break
            cursor = response.get("next_cursor")
        return results
