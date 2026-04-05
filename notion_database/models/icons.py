"""
Icon and Cover builders for Notion pages and databases.

Reference: https://developers.notion.com/reference/page#page-property-value-object
"""
from typing import Optional


class Icon:
    """Static factory methods for Notion icon objects.

    Use the returned dict as the ``icon`` argument when creating or updating
    pages and databases::

        client.pages.create(
            parent={"database_id": db_id},
            properties={"Name": PropertyValue.title("My page")},
            icon=Icon.emoji("🚀"),
        )
    """

    @staticmethod
    def emoji(emoji: str) -> dict:
        """Emoji icon.

        Args:
            emoji: A single emoji character, e.g. ``"🚀"``.

        Returns:
            ``{"type": "emoji", "emoji": emoji}``
        """
        return {"type": "emoji", "emoji": emoji}

    @staticmethod
    def external(url: str) -> dict:
        """External image icon.

        Args:
            url: URL of the icon image.

        Returns:
            ``{"type": "external", "external": {"url": url}}``
        """
        return {"type": "external", "external": {"url": url}}


class Cover:
    """Static factory methods for Notion cover objects.

    Use the returned dict as the ``cover`` argument when creating or updating
    pages and databases::

        client.pages.create(
            parent={"database_id": db_id},
            properties={"Name": PropertyValue.title("My page")},
            cover=Cover.external("https://example.com/cover.jpg"),
        )
    """

    @staticmethod
    def external(url: str) -> dict:
        """External image cover.

        Args:
            url: URL of the cover image.

        Returns:
            ``{"type": "external", "external": {"url": url}}``
        """
        return {"type": "external", "external": {"url": url}}
