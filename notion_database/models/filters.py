"""
Filter builder for Notion database queries.

Reference: https://developers.notion.com/reference/post-database-query-filter
"""
from typing import List, Optional


class _PropertyFilter:
    """Internal fluent builder for a single property filter."""

    def __init__(self, property_name: str, filter_type: str) -> None:
        self._property = property_name
        self._type = filter_type

    def _build(self, condition: dict) -> dict:
        return {"property": self._property, self._type: condition}

    # Generic conditions (available on most types)
    def equals(self, value) -> dict:
        return self._build({"equals": value})

    def does_not_equal(self, value) -> dict:
        return self._build({"does_not_equal": value})

    def is_empty(self) -> dict:
        return self._build({"is_empty": True})

    def is_not_empty(self) -> dict:
        return self._build({"is_not_empty": True})

    # String-like conditions
    def contains(self, value: str) -> dict:
        return self._build({"contains": value})

    def does_not_contain(self, value: str) -> dict:
        return self._build({"does_not_contain": value})

    def starts_with(self, value: str) -> dict:
        return self._build({"starts_with": value})

    def ends_with(self, value: str) -> dict:
        return self._build({"ends_with": value})

    # Numeric conditions
    def greater_than(self, value) -> dict:
        return self._build({"greater_than": value})

    def less_than(self, value) -> dict:
        return self._build({"less_than": value})

    def greater_than_or_equal_to(self, value) -> dict:
        return self._build({"greater_than_or_equal_to": value})

    def less_than_or_equal_to(self, value) -> dict:
        return self._build({"less_than_or_equal_to": value})

    # Date relative conditions
    def before(self, value: str) -> dict:
        return self._build({"before": value})

    def after(self, value: str) -> dict:
        return self._build({"after": value})

    def on_or_before(self, value: str) -> dict:
        return self._build({"on_or_before": value})

    def on_or_after(self, value: str) -> dict:
        return self._build({"on_or_after": value})

    def past_week(self) -> dict:
        return self._build({"past_week": {}})

    def past_month(self) -> dict:
        return self._build({"past_month": {}})

    def past_year(self) -> dict:
        return self._build({"past_year": {}})

    def next_week(self) -> dict:
        return self._build({"next_week": {}})

    def next_month(self) -> dict:
        return self._build({"next_month": {}})

    def next_year(self) -> dict:
        return self._build({"next_year": {}})

    def this_week(self) -> dict:
        return self._build({"this_week": {}})


class _TimestampFilter:
    """Internal fluent builder for a timestamp filter."""

    def __init__(self, timestamp: str) -> None:
        self._timestamp = timestamp

    def _build(self, condition: dict) -> dict:
        return {"timestamp": self._timestamp, self._timestamp: condition}

    def equals(self, value: str) -> dict:
        return self._build({"equals": value})

    def before(self, value: str) -> dict:
        return self._build({"before": value})

    def after(self, value: str) -> dict:
        return self._build({"after": value})

    def on_or_before(self, value: str) -> dict:
        return self._build({"on_or_before": value})

    def on_or_after(self, value: str) -> dict:
        return self._build({"on_or_after": value})

    def is_empty(self) -> dict:
        return self._build({"is_empty": True})

    def is_not_empty(self) -> dict:
        return self._build({"is_not_empty": True})

    def past_week(self) -> dict:
        return self._build({"past_week": {}})

    def past_month(self) -> dict:
        return self._build({"past_month": {}})

    def past_year(self) -> dict:
        return self._build({"past_year": {}})

    def next_week(self) -> dict:
        return self._build({"next_week": {}})

    def next_month(self) -> dict:
        return self._build({"next_month": {}})

    def next_year(self) -> dict:
        return self._build({"next_year": {}})

    def this_week(self) -> dict:
        return self._build({"this_week": {}})


class Filter:
    """Fluent builder for Notion database query filters.

    Use class methods to target a property by its Notion type, then chain a
    condition method to produce a filter dict::

        # Simple filters
        f1 = Filter.text("Name").contains("Alice")
        f2 = Filter.number("Score").greater_than(80)
        f3 = Filter.checkbox("Active").equals(True)
        f4 = Filter.select("Status").equals("Done")
        f5 = Filter.date("Due").before("2025-01-01")

        # Compound filters
        f6 = Filter.and_([f1, f2])
        f7 = Filter.or_([f3, f4])

        # Nested compound
        f8 = Filter.and_([Filter.text("Name").starts_with("A"), f7])

    Reference: https://developers.notion.com/reference/post-database-query-filter
    """

    # ------------------------------------------------------------------
    # Compound filters
    # ------------------------------------------------------------------

    @staticmethod
    def and_(filters: List[dict]) -> dict:
        """Combine filters with AND logic.

        Args:
            filters: List of filter dicts to combine.

        Returns:
            ``{"and": [...]}``
        """
        return {"and": filters}

    @staticmethod
    def or_(filters: List[dict]) -> dict:
        """Combine filters with OR logic.

        Args:
            filters: List of filter dicts to combine.

        Returns:
            ``{"or": [...]}``
        """
        return {"or": filters}

    # ------------------------------------------------------------------
    # Property type shortcuts
    # ------------------------------------------------------------------

    @staticmethod
    def text(property_name: str) -> _PropertyFilter:
        """Filter on a rich_text or title property.

        Supported conditions: ``equals``, ``does_not_equal``, ``contains``,
        ``does_not_contain``, ``starts_with``, ``ends_with``, ``is_empty``,
        ``is_not_empty``.

        Args:
            property_name: The name of the property column.
        """
        return _PropertyFilter(property_name, "rich_text")

    @staticmethod
    def title(property_name: str) -> _PropertyFilter:
        """Filter on a title property (alias for :meth:`text` with ``title`` type).

        Args:
            property_name: The name of the title column (usually ``"Name"``).
        """
        return _PropertyFilter(property_name, "title")

    @staticmethod
    def number(property_name: str) -> _PropertyFilter:
        """Filter on a number property.

        Supported conditions: ``equals``, ``does_not_equal``,
        ``greater_than``, ``less_than``, ``greater_than_or_equal_to``,
        ``less_than_or_equal_to``, ``is_empty``, ``is_not_empty``.

        Args:
            property_name: The name of the property column.
        """
        return _PropertyFilter(property_name, "number")

    @staticmethod
    def checkbox(property_name: str) -> _PropertyFilter:
        """Filter on a checkbox property.

        Supported conditions: ``equals`` (pass ``True``/``False``),
        ``does_not_equal``.

        Args:
            property_name: The name of the property column.
        """
        return _PropertyFilter(property_name, "checkbox")

    @staticmethod
    def select(property_name: str) -> _PropertyFilter:
        """Filter on a select property.

        Supported conditions: ``equals``, ``does_not_equal``,
        ``is_empty``, ``is_not_empty``.

        Args:
            property_name: The name of the property column.
        """
        return _PropertyFilter(property_name, "select")

    @staticmethod
    def multi_select(property_name: str) -> _PropertyFilter:
        """Filter on a multi_select property.

        Supported conditions: ``contains``, ``does_not_contain``,
        ``is_empty``, ``is_not_empty``.

        Args:
            property_name: The name of the property column.
        """
        return _PropertyFilter(property_name, "multi_select")

    @staticmethod
    def status(property_name: str) -> _PropertyFilter:
        """Filter on a status property.

        Supported conditions: ``equals``, ``does_not_equal``,
        ``is_empty``, ``is_not_empty``.

        Args:
            property_name: The name of the property column.
        """
        return _PropertyFilter(property_name, "status")

    @staticmethod
    def date(property_name: str) -> _PropertyFilter:
        """Filter on a date property.

        Supported conditions: ``equals``, ``before``, ``after``,
        ``on_or_before``, ``on_or_after``, ``is_empty``, ``is_not_empty``,
        ``past_week``, ``past_month``, ``past_year``, ``next_week``,
        ``next_month``, ``next_year``, ``this_week``.

        Args:
            property_name: The name of the property column.
        """
        return _PropertyFilter(property_name, "date")

    @staticmethod
    def people(property_name: str) -> _PropertyFilter:
        """Filter on a people property.

        Supported conditions: ``contains``, ``does_not_contain``,
        ``is_empty``, ``is_not_empty``.

        Args:
            property_name: The name of the property column.
        """
        return _PropertyFilter(property_name, "people")

    @staticmethod
    def files(property_name: str) -> _PropertyFilter:
        """Filter on a files property.

        Supported conditions: ``is_empty``, ``is_not_empty``.

        Args:
            property_name: The name of the property column.
        """
        return _PropertyFilter(property_name, "files")

    @staticmethod
    def relation(property_name: str) -> _PropertyFilter:
        """Filter on a relation property.

        Supported conditions: ``contains``, ``does_not_contain``,
        ``is_empty``, ``is_not_empty``.

        Args:
            property_name: The name of the property column.
        """
        return _PropertyFilter(property_name, "relation")

    @staticmethod
    def url(property_name: str) -> _PropertyFilter:
        """Filter on a URL property.

        Supported conditions: ``equals``, ``does_not_equal``, ``contains``,
        ``does_not_contain``, ``starts_with``, ``ends_with``,
        ``is_empty``, ``is_not_empty``.

        Args:
            property_name: The name of the property column.
        """
        return _PropertyFilter(property_name, "url")

    @staticmethod
    def email(property_name: str) -> _PropertyFilter:
        """Filter on an email property.

        Supported conditions: same as :meth:`url`.

        Args:
            property_name: The name of the property column.
        """
        return _PropertyFilter(property_name, "email")

    @staticmethod
    def phone_number(property_name: str) -> _PropertyFilter:
        """Filter on a phone_number property.

        Supported conditions: same as :meth:`url`.

        Args:
            property_name: The name of the property column.
        """
        return _PropertyFilter(property_name, "phone_number")

    @staticmethod
    def unique_id(property_name: str) -> _PropertyFilter:
        """Filter on a unique_id property.

        Supported conditions: ``equals``, ``does_not_equal``,
        ``greater_than``, ``less_than``, ``greater_than_or_equal_to``,
        ``less_than_or_equal_to``.

        Args:
            property_name: The name of the property column.
        """
        return _PropertyFilter(property_name, "unique_id")

    # ------------------------------------------------------------------
    # Timestamp filters (created_time / last_edited_time)
    # ------------------------------------------------------------------

    @staticmethod
    def created_time() -> _TimestampFilter:
        """Filter on the ``created_time`` system timestamp.

        Supported conditions: ``equals``, ``before``, ``after``,
        ``on_or_before``, ``on_or_after``, ``is_empty``, ``is_not_empty``,
        ``past_week``, ``past_month``, ``past_year``, ``next_week``,
        ``next_month``, ``next_year``, ``this_week``.
        """
        return _TimestampFilter("created_time")

    @staticmethod
    def last_edited_time() -> _TimestampFilter:
        """Filter on the ``last_edited_time`` system timestamp.

        Supported conditions: same as :meth:`created_time`.
        """
        return _TimestampFilter("last_edited_time")

    # ------------------------------------------------------------------
    # Raw / custom filter
    # ------------------------------------------------------------------

    @staticmethod
    def raw(filter_dict: dict) -> dict:
        """Pass a raw filter dict directly.

        Use this escape hatch when the built-in helpers don't cover your
        filter type (e.g. formula, rollup).

        Args:
            filter_dict: A dict conforming to the Notion filter schema.

        Returns:
            The dict unchanged.
        """
        return filter_dict
