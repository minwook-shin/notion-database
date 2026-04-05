"""
HTTP client for the Notion API.
"""
import json
from typing import Any, Dict, Optional

import requests

from notion_database.exceptions import (
    NotionAPIError,
    NotionConflictError,
    NotionForbiddenError,
    NotionInternalError,
    NotionNotFoundError,
    NotionRateLimitError,
    NotionUnauthorizedError,
    NotionValidationError,
)

_NOTION_VERSION = "2022-06-28"
_BASE_URL = "https://api.notion.com/v1"

_STATUS_TO_EXCEPTION = {
    400: NotionValidationError,
    401: NotionUnauthorizedError,
    403: NotionForbiddenError,
    404: NotionNotFoundError,
    409: NotionConflictError,
    429: NotionRateLimitError,
}


class HttpClient:
    """Thin HTTP wrapper around the Notion REST API.

    All methods return the parsed JSON response as a plain ``dict``.  On
    non-2xx responses a :class:`~notion_database.exceptions.NotionAPIError`
    subclass is raised with the Notion ``code`` and ``message`` fields
    populated from the response body.
    """

    def __init__(self, token: str) -> None:
        self._headers: Dict[str, str] = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Notion-Version": _NOTION_VERSION,
        }

    # ------------------------------------------------------------------
    # Public HTTP verbs
    # ------------------------------------------------------------------

    def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Dict:
        response = requests.get(
            f"{_BASE_URL}{path}",
            headers=self._headers,
            params=params,
            timeout=60,
        )
        return self._parse(response)

    def post(self, path: str, body: Optional[Dict] = None) -> Dict:
        response = requests.post(
            f"{_BASE_URL}{path}",
            headers=self._headers,
            data=json.dumps(body or {}),
            timeout=60,
        )
        return self._parse(response)

    def patch(self, path: str, body: Optional[Dict] = None) -> Dict:
        response = requests.patch(
            f"{_BASE_URL}{path}",
            headers=self._headers,
            data=json.dumps(body or {}),
            timeout=60,
        )
        return self._parse(response)

    def delete(self, path: str) -> Dict:
        response = requests.delete(
            f"{_BASE_URL}{path}",
            headers=self._headers,
            timeout=60,
        )
        return self._parse(response)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _parse(response: requests.Response) -> Dict:
        if response.ok:
            return response.json()

        exc_class = _STATUS_TO_EXCEPTION.get(response.status_code, NotionAPIError)
        if response.status_code >= 500:
            exc_class = NotionInternalError

        try:
            body = response.json()
            code = body.get("code", "unknown_error")
            message = body.get("message", response.text)
        except Exception:
            code = "unknown_error"
            message = response.text

        raise exc_class(response.status_code, code, message)
