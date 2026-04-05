"""
RichText builder  –  https://developers.notion.com/reference/rich-text
"""
from typing import List, Optional, Union


def _normalize(text: Union[str, List[dict]]) -> List[dict]:
    """Convert a plain string to a single-element rich-text array.

    If ``text`` is already a list, return it unchanged.
    """
    if isinstance(text, str):
        return [RichText.text(text)]
    return text


class RichText:
    """Static factory methods for Notion rich-text objects.

    Each method returns a single rich-text element (a dict).  To build a
    rich-text *array* (as required by most API fields), wrap the results in a
    list::

        [RichText.text("Hello, "), RichText.text("world!", bold=True)]

    For convenience, string arguments accepted by other builders (e.g.
    :class:`~notion_database.models.properties.PropertyValue`,
    :class:`~notion_database.models.blocks.BlockContent`) are automatically
    normalised to a ``[RichText.text(s)]`` array via the module-level
    :func:`_normalize` helper.
    """

    @staticmethod
    def text(
        content: str,
        *,
        bold: bool = False,
        italic: bool = False,
        underline: bool = False,
        strikethrough: bool = False,
        code: bool = False,
        color: str = "default",
        link: Optional[str] = None,
    ) -> dict:
        """Create a plain-text rich-text element with optional annotations.

        Args:
            content: The text content.
            bold: Whether the text is bold.
            italic: Whether the text is italic.
            underline: Whether the text is underlined.
            strikethrough: Whether the text has strikethrough.
            code: Whether the text is inline code.
            color: Notion color string (e.g. ``"red"``, ``"blue_background"``).
            link: Optional URL to make the text a hyperlink.

        Returns:
            A Notion rich-text element dict.
        """
        element: dict = {
            "type": "text",
            "text": {"content": content},
        }
        if link:
            element["text"]["link"] = {"url": link}
        annotations: dict = {}
        if bold:
            annotations["bold"] = True
        if italic:
            annotations["italic"] = True
        if underline:
            annotations["underline"] = True
        if strikethrough:
            annotations["strikethrough"] = True
        if code:
            annotations["code"] = True
        if color != "default":
            annotations["color"] = color
        if annotations:
            element["annotations"] = annotations
        return element

    @staticmethod
    def mention_page(page_id: str) -> dict:
        """Create a page-mention rich-text element.

        Args:
            page_id: The ID of the page to mention.

        Returns:
            A Notion rich-text mention element dict.
        """
        return {
            "type": "mention",
            "mention": {"type": "page", "page": {"id": page_id}},
        }

    @staticmethod
    def mention_database(database_id: str) -> dict:
        """Create a database-mention rich-text element.

        Args:
            database_id: The ID of the database to mention.

        Returns:
            A Notion rich-text mention element dict.
        """
        return {
            "type": "mention",
            "mention": {"type": "database", "database": {"id": database_id}},
        }

    @staticmethod
    def mention_user(user_id: str) -> dict:
        """Create a user-mention rich-text element.

        Args:
            user_id: The ID of the user to mention.

        Returns:
            A Notion rich-text mention element dict.
        """
        return {
            "type": "mention",
            "mention": {"type": "user", "user": {"id": user_id}},
        }

    @staticmethod
    def mention_date(start: str, end: Optional[str] = None) -> dict:
        """Create a date-mention rich-text element.

        Args:
            start: ISO 8601 date or datetime string (e.g. ``"2024-01-15"``).
            end: Optional end date for a date range.

        Returns:
            A Notion rich-text mention element dict.
        """
        date_obj: dict = {"start": start}
        if end is not None:
            date_obj["end"] = end
        return {
            "type": "mention",
            "mention": {"type": "date", "date": date_obj},
        }

    @staticmethod
    def equation(expression: str) -> dict:
        """Create an inline equation rich-text element.

        Args:
            expression: The LaTeX expression string.

        Returns:
            A Notion rich-text equation element dict.
        """
        return {
            "type": "equation",
            "equation": {"expression": expression},
        }
