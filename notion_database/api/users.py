"""
Notion Users API  –  https://developers.notion.com/reference/user
"""
from typing import Any, Dict, List, Optional

from notion_database.http.client import HttpClient


class UsersAPI:
    """1-to-1 mapping of the Notion Users REST endpoints.

    Reference: https://developers.notion.com/reference/user
    """

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def retrieve(self, user_id: str) -> Dict:
        """Retrieve a user by ID.

        Args:
            user_id: The ID of the user to retrieve.

        Returns:
            Notion user object.

        Reference: https://developers.notion.com/reference/get-user
        """
        return self._http.get(f"/users/{user_id}")

    def list(
        self,
        *,
        start_cursor: Optional[str] = None,
        page_size: int = 100,
    ) -> Dict:
        """List all users in the workspace.

        Args:
            start_cursor: Cursor for pagination.
            page_size: Number of results per page (1-100).

        Returns:
            Notion list object with ``results``, ``has_more``, and
            ``next_cursor`` fields.

        Reference: https://developers.notion.com/reference/get-users
        """
        params: Dict[str, Any] = {"page_size": page_size}
        if start_cursor is not None:
            params["start_cursor"] = start_cursor
        return self._http.get("/users", params=params)

    def list_all(self) -> List[Dict]:
        """List **all** users in the workspace, automatically paginating.

        Returns:
            A flat list of all Notion user objects.
        """
        users: List[Dict] = []
        cursor: Optional[str] = None
        while True:
            response = self.list(start_cursor=cursor)
            users.extend(response.get("results", []))
            if not response.get("has_more"):
                break
            cursor = response.get("next_cursor")
        return users

    def me(self) -> Dict:
        """Retrieve the bot user associated with the current integration token.

        Returns:
            Notion bot user object.

        Reference: https://developers.notion.com/reference/get-self
        """
        return self._http.get("/users/me")
