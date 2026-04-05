"""
BlockContent builder  –  https://developers.notion.com/reference/block
"""
from typing import List, Optional, Union

from notion_database.models.rich_text import _normalize

_DEFAULT_COLOR = "default"


def _rt(text: Union[str, List[dict]]) -> List[dict]:
    return _normalize(text)


class BlockContent:
    """Static factory methods for Notion block objects.

    Each method returns a single block dict suitable for use in the
    ``children`` parameter of
    :meth:`~notion_database.api.pages.PagesAPI.create` or
    :meth:`~notion_database.api.blocks.BlocksAPI.append_children`.

    All ``text`` parameters accept either a plain string (automatically
    wrapped in a single rich-text element) or a list of
    :class:`~notion_database.models.rich_text.RichText` dicts for annotated
    content.

    Example::

        client.blocks.append_children(page_id, children=[
            BlockContent.heading_1("Introduction"),
            BlockContent.paragraph("Hello, Notion!"),
            BlockContent.bulleted_list_item("First item"),
            BlockContent.bulleted_list_item("Second item"),
            BlockContent.divider(),
        ])
    """

    # ------------------------------------------------------------------
    # Text blocks
    # ------------------------------------------------------------------

    @staticmethod
    def paragraph(
        text: Union[str, List[dict]] = "",
        *,
        color: str = _DEFAULT_COLOR,
        children: Optional[List[dict]] = None,
    ) -> dict:
        """Paragraph block.

        Args:
            text: Block content.
            color: Notion color string.
            children: Nested child blocks.

        Returns:
            Notion paragraph block dict.
        """
        body: dict = {"rich_text": _rt(text), "color": color}
        if children:
            body["children"] = children
        return {"object": "block", "type": "paragraph", "paragraph": body}

    @staticmethod
    def heading_1(
        text: Union[str, List[dict]] = "",
        *,
        color: str = _DEFAULT_COLOR,
        is_toggleable: bool = False,
    ) -> dict:
        """Heading 1 block.

        Args:
            text: Block content.
            color: Notion color string.
            is_toggleable: Whether the heading can be toggled.

        Returns:
            Notion heading_1 block dict.
        """
        return {
            "object": "block",
            "type": "heading_1",
            "heading_1": {
                "rich_text": _rt(text),
                "color": color,
                "is_toggleable": is_toggleable,
            },
        }

    @staticmethod
    def heading_2(
        text: Union[str, List[dict]] = "",
        *,
        color: str = _DEFAULT_COLOR,
        is_toggleable: bool = False,
    ) -> dict:
        """Heading 2 block.

        Args:
            text: Block content.
            color: Notion color string.
            is_toggleable: Whether the heading can be toggled.

        Returns:
            Notion heading_2 block dict.
        """
        return {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": _rt(text),
                "color": color,
                "is_toggleable": is_toggleable,
            },
        }

    @staticmethod
    def heading_3(
        text: Union[str, List[dict]] = "",
        *,
        color: str = _DEFAULT_COLOR,
        is_toggleable: bool = False,
    ) -> dict:
        """Heading 3 block.

        Args:
            text: Block content.
            color: Notion color string.
            is_toggleable: Whether the heading can be toggled.

        Returns:
            Notion heading_3 block dict.
        """
        return {
            "object": "block",
            "type": "heading_3",
            "heading_3": {
                "rich_text": _rt(text),
                "color": color,
                "is_toggleable": is_toggleable,
            },
        }

    @staticmethod
    def callout(
        text: Union[str, List[dict]] = "",
        *,
        icon: Optional[dict] = None,
        color: str = _DEFAULT_COLOR,
        children: Optional[List[dict]] = None,
    ) -> dict:
        """Callout block.

        Args:
            text: Block content.
            icon: Icon object (emoji or external image).
                Use :class:`~notion_database.models.icons.Icon`.
            color: Notion color string.
            children: Nested child blocks.

        Returns:
            Notion callout block dict.
        """
        body: dict = {"rich_text": _rt(text), "color": color}
        if icon:
            body["icon"] = icon
        if children:
            body["children"] = children
        return {"object": "block", "type": "callout", "callout": body}

    @staticmethod
    def quote(
        text: Union[str, List[dict]] = "",
        *,
        color: str = _DEFAULT_COLOR,
        children: Optional[List[dict]] = None,
    ) -> dict:
        """Quote block.

        Args:
            text: Block content.
            color: Notion color string.
            children: Nested child blocks.

        Returns:
            Notion quote block dict.
        """
        body: dict = {"rich_text": _rt(text), "color": color}
        if children:
            body["children"] = children
        return {"object": "block", "type": "quote", "quote": body}

    @staticmethod
    def bulleted_list_item(
        text: Union[str, List[dict]] = "",
        *,
        color: str = _DEFAULT_COLOR,
        children: Optional[List[dict]] = None,
    ) -> dict:
        """Bulleted list item block.

        Args:
            text: Item content.
            color: Notion color string.
            children: Nested child blocks (sub-list items etc.).

        Returns:
            Notion bulleted_list_item block dict.
        """
        body: dict = {"rich_text": _rt(text), "color": color}
        if children:
            body["children"] = children
        return {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": body,
        }

    @staticmethod
    def numbered_list_item(
        text: Union[str, List[dict]] = "",
        *,
        color: str = _DEFAULT_COLOR,
        children: Optional[List[dict]] = None,
    ) -> dict:
        """Numbered list item block.

        Args:
            text: Item content.
            color: Notion color string.
            children: Nested child blocks.

        Returns:
            Notion numbered_list_item block dict.
        """
        body: dict = {"rich_text": _rt(text), "color": color}
        if children:
            body["children"] = children
        return {
            "object": "block",
            "type": "numbered_list_item",
            "numbered_list_item": body,
        }

    @staticmethod
    def to_do(
        text: Union[str, List[dict]] = "",
        *,
        checked: bool = False,
        color: str = _DEFAULT_COLOR,
        children: Optional[List[dict]] = None,
    ) -> dict:
        """To-do (checkbox) block.

        Args:
            text: Item content.
            checked: Whether the checkbox is checked.
            color: Notion color string.
            children: Nested child blocks.

        Returns:
            Notion to_do block dict.
        """
        body: dict = {"rich_text": _rt(text), "checked": checked, "color": color}
        if children:
            body["children"] = children
        return {"object": "block", "type": "to_do", "to_do": body}

    @staticmethod
    def toggle(
        text: Union[str, List[dict]] = "",
        *,
        color: str = _DEFAULT_COLOR,
        children: Optional[List[dict]] = None,
    ) -> dict:
        """Toggle block.

        Args:
            text: Toggle header content.
            color: Notion color string.
            children: Content revealed when toggled.

        Returns:
            Notion toggle block dict.
        """
        body: dict = {"rich_text": _rt(text), "color": color}
        if children:
            body["children"] = children
        return {"object": "block", "type": "toggle", "toggle": body}

    # ------------------------------------------------------------------
    # Code block
    # ------------------------------------------------------------------

    @staticmethod
    def code(
        code: Union[str, List[dict]] = "",
        *,
        language: str = "plain text",
        caption: Optional[Union[str, List[dict]]] = None,
    ) -> dict:
        """Code block.

        Args:
            code: The code content.
            language: Programming language for syntax highlighting.
                Common values: ``"abap"``, ``"arduino"``, ``"bash"``,
                ``"basic"``, ``"c"``, ``"clojure"``, ``"coffeescript"``,
                ``"c++"``, ``"c#"``, ``"css"``, ``"dart"``, ``"diff"``,
                ``"docker"``, ``"elixir"``, ``"elm"``, ``"erlang"``,
                ``"flow"``, ``"fortran"``, ``"f#"``, ``"gherkin"``,
                ``"glsl"``, ``"go"``, ``"graphql"``, ``"groovy"``,
                ``"haskell"``, ``"html"``, ``"java"``, ``"javascript"``,
                ``"json"``, ``"julia"``, ``"kotlin"``, ``"latex"``,
                ``"less"``, ``"lisp"``, ``"livescript"``, ``"lua"``,
                ``"makefile"``, ``"markdown"``, ``"markup"``,
                ``"matlab"``, ``"mermaid"``, ``"nix"``, ``"objective-c"``,
                ``"ocaml"``, ``"pascal"``, ``"perl"``, ``"php"``,
                ``"plain text"``, ``"powershell"``, ``"prolog"``,
                ``"protobuf"``, ``"python"``, ``"r"``, ``"reason"``,
                ``"ruby"``, ``"rust"``, ``"sass"``, ``"scala"``,
                ``"scheme"``, ``"scss"``, ``"shell"``, ``"sql"``,
                ``"swift"``, ``"typescript"``, ``"vb.net"``, ``"verilog"``,
                ``"vhdl"``, ``"visual basic"``, ``"webassembly"``,
                ``"xml"``, ``"yaml"``, or ``"java/c/c++/c#"``.
            caption: Optional caption rich-text.

        Returns:
            Notion code block dict.
        """
        body: dict = {"rich_text": _rt(code), "language": language}
        if caption is not None:
            body["caption"] = _rt(caption)
        return {"object": "block", "type": "code", "code": body}

    # ------------------------------------------------------------------
    # Media / embed blocks
    # ------------------------------------------------------------------

    @staticmethod
    def image(url: str, *, caption: Optional[Union[str, List[dict]]] = None) -> dict:
        """External image block.

        Args:
            url: URL of the image.
            caption: Optional caption rich-text.

        Returns:
            Notion image block dict.
        """
        body: dict = {"type": "external", "external": {"url": url}}
        if caption is not None:
            body["caption"] = _rt(caption)
        return {"object": "block", "type": "image", "image": body}

    @staticmethod
    def video(url: str, *, caption: Optional[Union[str, List[dict]]] = None) -> dict:
        """External video block.

        Args:
            url: URL of the video.
            caption: Optional caption rich-text.

        Returns:
            Notion video block dict.
        """
        body: dict = {"type": "external", "external": {"url": url}}
        if caption is not None:
            body["caption"] = _rt(caption)
        return {"object": "block", "type": "video", "video": body}

    @staticmethod
    def file(url: str, *, caption: Optional[Union[str, List[dict]]] = None) -> dict:
        """External file block.

        Args:
            url: URL of the file.
            caption: Optional caption rich-text.

        Returns:
            Notion file block dict.
        """
        body: dict = {"type": "external", "external": {"url": url}}
        if caption is not None:
            body["caption"] = _rt(caption)
        return {"object": "block", "type": "file", "file": body}

    @staticmethod
    def pdf(url: str, *, caption: Optional[Union[str, List[dict]]] = None) -> dict:
        """External PDF block.

        Args:
            url: URL of the PDF.
            caption: Optional caption rich-text.

        Returns:
            Notion pdf block dict.
        """
        body: dict = {"type": "external", "external": {"url": url}}
        if caption is not None:
            body["caption"] = _rt(caption)
        return {"object": "block", "type": "pdf", "pdf": body}

    @staticmethod
    def embed(url: str) -> dict:
        """Embed block.

        Args:
            url: URL to embed.

        Returns:
            Notion embed block dict.
        """
        return {"object": "block", "type": "embed", "embed": {"url": url}}

    @staticmethod
    def bookmark(
        url: str, *, caption: Optional[Union[str, List[dict]]] = None
    ) -> dict:
        """Bookmark block.

        Args:
            url: URL of the bookmark.
            caption: Optional caption rich-text.

        Returns:
            Notion bookmark block dict.
        """
        body: dict = {"url": url}
        if caption is not None:
            body["caption"] = _rt(caption)
        return {"object": "block", "type": "bookmark", "bookmark": body}

    # ------------------------------------------------------------------
    # Structural blocks
    # ------------------------------------------------------------------

    @staticmethod
    def divider() -> dict:
        """Divider (horizontal rule) block.

        Returns:
            Notion divider block dict.
        """
        return {"object": "block", "type": "divider", "divider": {}}

    @staticmethod
    def table_of_contents(*, color: str = _DEFAULT_COLOR) -> dict:
        """Table of contents block.

        Args:
            color: Notion color string.

        Returns:
            Notion table_of_contents block dict.
        """
        return {
            "object": "block",
            "type": "table_of_contents",
            "table_of_contents": {"color": color},
        }

    @staticmethod
    def breadcrumb() -> dict:
        """Breadcrumb block.

        Returns:
            Notion breadcrumb block dict.
        """
        return {"object": "block", "type": "breadcrumb", "breadcrumb": {}}

    # ------------------------------------------------------------------
    # Math
    # ------------------------------------------------------------------

    @staticmethod
    def equation(expression: str) -> dict:
        """Block-level equation.

        Args:
            expression: The LaTeX expression string.

        Returns:
            Notion equation block dict.
        """
        return {
            "object": "block",
            "type": "equation",
            "equation": {"expression": expression},
        }

    # ------------------------------------------------------------------
    # Tab layout  (Notion-Version: 2026-03-11)
    # ------------------------------------------------------------------

    @staticmethod
    def tab(
        title: Union[str, List[dict]],
        children: Optional[List[dict]] = None,
        *,
        icon: Optional[dict] = None,
    ) -> dict:
        """Tab block item for organizing content into labeled sections.

        Tabs must be placed inside a ``tab_group`` block.  Build a full tab
        group using :meth:`tab_group`.

        Args:
            title: Tab label as a plain string or rich-text list.
            children: Content blocks shown when the tab is active.
            icon: Optional icon object for the tab label.

        Returns:
            Notion tab block dict.
        """
        body: dict = {"title": _rt(title)}
        if children:
            body["children"] = children
        if icon is not None:
            body["icon"] = icon
        return {"object": "block", "type": "tab", "tab": body}

    @staticmethod
    def tab_group(tabs: List[dict]) -> dict:
        """Tab group block containing two or more :meth:`tab` blocks.

        Args:
            tabs: List of tab block dicts built with :meth:`tab`.

        Returns:
            Notion tab_group block dict.

        Example::

            BlockContent.tab_group([
                BlockContent.tab("Overview", [BlockContent.paragraph("Overview content")]),
                BlockContent.tab("Details",  [BlockContent.paragraph("Details content")]),
            ])
        """
        return {
            "object": "block",
            "type": "tab_group",
            "tab_group": {"children": tabs},
        }

    # ------------------------------------------------------------------
    # Column layout
    # ------------------------------------------------------------------

    @staticmethod
    def column_list(columns: List[List[dict]]) -> dict:
        """Column list block containing two or more column blocks.

        Args:
            columns: A list where each element is a list of blocks to place
                in one column.

        Returns:
            Notion column_list block dict with nested column children.

        Example::

            BlockContent.column_list([
                [BlockContent.paragraph("Left column")],
                [BlockContent.paragraph("Right column")],
            ])
        """
        column_blocks = [
            {
                "object": "block",
                "type": "column",
                "column": {"children": col_children},
            }
            for col_children in columns
        ]
        return {
            "object": "block",
            "type": "column_list",
            "column_list": {"children": column_blocks},
        }
