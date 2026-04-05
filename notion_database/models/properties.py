"""
Property builders for Notion pages and databases.

Two classes are provided:

* :class:`PropertyValue` – builds property *values* when creating or updating
  **pages** (the ``properties`` field in POST /pages and PATCH /pages/{id}).
* :class:`PropertySchema` – builds property *schemas* when creating or updating
  **database columns** (the ``properties`` field in POST /databases and
  PATCH /databases/{id}).

Reference (values):  https://developers.notion.com/reference/property-value-object
Reference (schema):  https://developers.notion.com/reference/property-object
"""
from typing import List, Optional, Union

from notion_database.models.rich_text import RichText, _normalize


class PropertyValue:
    """Static factory methods for Notion page property *values*.

    Each method returns a dict ready to be used as the value for a key in the
    ``properties`` dict passed to :meth:`~notion_database.api.pages.PagesAPI.create`
    or :meth:`~notion_database.api.pages.PagesAPI.update`.

    Example::

        client.pages.create(
            parent={"database_id": db_id},
            properties={
                "Name":    PropertyValue.title("My page"),
                "Status":  PropertyValue.select("Active"),
                "Count":   PropertyValue.number(42),
                "Done":    PropertyValue.checkbox(True),
            },
        )
    """

    @staticmethod
    def title(text: Union[str, List[dict]]) -> dict:
        """Title property value.

        Args:
            text: Plain string or list of
                :class:`~notion_database.models.rich_text.RichText` elements.

        Returns:
            ``{"title": [...]}``
        """
        return {"title": _normalize(text)}

    @staticmethod
    def rich_text(text: Union[str, List[dict]]) -> dict:
        """Rich-text property value.

        Args:
            text: Plain string or list of
                :class:`~notion_database.models.rich_text.RichText` elements.

        Returns:
            ``{"rich_text": [...]}``
        """
        return {"rich_text": _normalize(text)}

    @staticmethod
    def number(value: Union[int, float]) -> dict:
        """Number property value.

        Args:
            value: Numeric value.

        Returns:
            ``{"number": value}``
        """
        return {"number": value}

    @staticmethod
    def select(name: str) -> dict:
        """Select (single) property value.

        Args:
            name: The name of the option to select.

        Returns:
            ``{"select": {"name": name}}``
        """
        return {"select": {"name": name}}

    @staticmethod
    def multi_select(names: List[str]) -> dict:
        """Multi-select property value.

        Args:
            names: List of option names to select.

        Returns:
            ``{"multi_select": [{"name": ...}, ...]}``
        """
        return {"multi_select": [{"name": n} for n in names]}

    @staticmethod
    def status(name: str) -> dict:
        """Status property value.

        Args:
            name: The name of the status option (e.g. ``"In progress"``).

        Returns:
            ``{"status": {"name": name}}``
        """
        return {"status": {"name": name}}

    @staticmethod
    def date(
        start: str,
        *,
        end: Optional[str] = None,
        time_zone: Optional[str] = None,
    ) -> dict:
        """Date property value.

        Args:
            start: ISO 8601 date or datetime string (e.g. ``"2024-01-15"``
                or ``"2024-01-15T09:00:00+09:00"``).
            end: Optional end date for a date range.
            time_zone: Optional IANA time-zone string.

        Returns:
            ``{"date": {"start": ..., "end": ..., "time_zone": ...}}``
        """
        date_obj: dict = {"start": start}
        if end is not None:
            date_obj["end"] = end
        if time_zone is not None:
            date_obj["time_zone"] = time_zone
        return {"date": date_obj}

    @staticmethod
    def checkbox(checked: bool) -> dict:
        """Checkbox property value.

        Args:
            checked: ``True`` to check, ``False`` to uncheck.

        Returns:
            ``{"checkbox": checked}``
        """
        return {"checkbox": checked}

    @staticmethod
    def url(url: str) -> dict:
        """URL property value.

        Args:
            url: The URL string.

        Returns:
            ``{"url": url}``
        """
        return {"url": url}

    @staticmethod
    def email(email: str) -> dict:
        """Email property value.

        Args:
            email: The email address.

        Returns:
            ``{"email": email}``
        """
        return {"email": email}

    @staticmethod
    def phone_number(phone: str) -> dict:
        """Phone number property value.

        Args:
            phone: The phone number string.

        Returns:
            ``{"phone_number": phone}``
        """
        return {"phone_number": phone}

    @staticmethod
    def people(user_ids: List[str]) -> dict:
        """People property value.

        Args:
            user_ids: List of Notion user IDs.

        Returns:
            ``{"people": [{"id": ...}, ...]}``
        """
        return {"people": [{"id": uid} for uid in user_ids]}

    @staticmethod
    def files(
        files: List[Union[str, dict]],
    ) -> dict:
        """Files property value (external files only).

        Args:
            files: Either a list of URL strings, or a list of dicts with
                ``name`` and ``url`` keys, e.g.
                ``[{"name": "report.pdf", "url": "https://..."}]``.

        Returns:
            ``{"files": [...]}``
        """
        result = []
        for f in files:
            if isinstance(f, str):
                result.append({"type": "external", "name": f, "external": {"url": f}})
            else:
                result.append(
                    {
                        "type": "external",
                        "name": f.get("name", f.get("url", "")),
                        "external": {"url": f["url"]},
                    }
                )
        return {"files": result}

    @staticmethod
    def relation(page_ids: List[str]) -> dict:
        """Relation property value.

        Args:
            page_ids: List of page IDs to relate to.

        Returns:
            ``{"relation": [{"id": ...}, ...]}``
        """
        return {"relation": [{"id": pid} for pid in page_ids]}

    @staticmethod
    def unique_id(number: int, *, prefix: Optional[str] = None) -> dict:
        """Unique ID property value (read-only in practice; for completeness).

        Args:
            number: The numeric part of the unique ID.
            prefix: Optional prefix string.

        Returns:
            ``{"unique_id": {"number": ..., "prefix": ...}}``
        """
        obj: dict = {"number": number}
        if prefix is not None:
            obj["prefix"] = prefix
        return {"unique_id": obj}

    @staticmethod
    def verification(
        state: str = "unverified",
        *,
        verified_by: Optional[str] = None,
        date: Optional[str] = None,
    ) -> dict:
        """Verification property value for wiki pages
        (Notion-Version: 2026-03-11).

        Args:
            state: ``"verified"`` or ``"unverified"``.
            verified_by: Optional user ID of the verifier.
            date: Optional ISO 8601 expiration date string.

        Returns:
            ``{"verification": {"state": ..., ...}}``
        """
        obj: dict = {"state": state}
        if verified_by is not None:
            obj["verified_by"] = {"id": verified_by}
        if date is not None:
            obj["date"] = {"start": date}
        return {"verification": obj}


class PropertySchema:
    """Static factory methods for Notion database property *schemas*.

    Each method returns a dict ready to be used as the value for a key in the
    ``properties`` dict passed to
    :meth:`~notion_database.api.databases.DatabasesAPI.create` or
    :meth:`~notion_database.api.databases.DatabasesAPI.update`.

    Example::

        client.databases.create(
            parent={"type": "page_id", "page_id": page_id},
            title=[RichText.text("My Database")],
            properties={
                "Name":    PropertySchema.title(),
                "Status":  PropertySchema.select([
                               {"name": "Active", "color": "green"},
                               {"name": "Done",   "color": "gray"},
                           ]),
                "Score":   PropertySchema.number("number"),
            },
        )
    """

    @staticmethod
    def title() -> dict:
        """Title (primary key) column.  Every database must have exactly one.

        Returns:
            ``{"title": {}}``
        """
        return {"title": {}}

    @staticmethod
    def rich_text() -> dict:
        """Rich-text column.

        Returns:
            ``{"rich_text": {}}``
        """
        return {"rich_text": {}}

    @staticmethod
    def number(format: str = "number") -> dict:
        """Number column.

        Args:
            format: Number format string.  One of ``"number"``,
                ``"number_with_commas"``, ``"percent"``, ``"dollar"``,
                ``"canadian_dollar"``, ``"euro"``, ``"pound"``, ``"yen"``,
                ``"ruble"``, ``"rupee"``, ``"won"``, ``"yuan"``,
                ``"real"``, ``"lira"``, ``"rupiah"``, ``"franc"``,
                ``"hong_kong_dollar"``, ``"new_zealand_dollar"``,
                ``"krona"``, ``"norwegian_krone"``, ``"mexican_peso"``,
                ``"rand"``, ``"new_taiwan_dollar"``, ``"danish_krone"``,
                ``"zloty"``, ``"baht"``, ``"forint"``, ``"koruna"``,
                ``"shekel"``, ``"chilean_peso"``, ``"philippine_peso"``,
                ``"dirham"``, ``"colombian_peso"``, ``"riyal"``,
                ``"ringgit"``, ``"leu"``, ``"argentine_peso"``,
                ``"uruguayan_peso"``, or ``"singapore_dollar"``.

        Returns:
            ``{"number": {"format": format}}``
        """
        return {"number": {"format": format}}

    @staticmethod
    def select(options: Optional[List[dict]] = None) -> dict:
        """Select (single-choice) column.

        Args:
            options: List of option dicts, each with ``name`` and optional
                ``color`` keys, e.g.
                ``[{"name": "Active", "color": "green"}]``.

        Returns:
            ``{"select": {"options": [...]}}``
        """
        return {"select": {"options": options or []}}

    @staticmethod
    def multi_select(options: Optional[List[dict]] = None) -> dict:
        """Multi-select column.

        Args:
            options: List of option dicts (same format as :meth:`select`).

        Returns:
            ``{"multi_select": {"options": [...]}}``
        """
        return {"multi_select": {"options": options or []}}

    @staticmethod
    def status() -> dict:
        """Status column (managed by Notion, options cannot be set via API).

        Returns:
            ``{"status": {}}``
        """
        return {"status": {}}

    @staticmethod
    def date() -> dict:
        """Date column.

        Returns:
            ``{"date": {}}``
        """
        return {"date": {}}

    @staticmethod
    def checkbox() -> dict:
        """Checkbox column.

        Returns:
            ``{"checkbox": {}}``
        """
        return {"checkbox": {}}

    @staticmethod
    def url() -> dict:
        """URL column.

        Returns:
            ``{"url": {}}``
        """
        return {"url": {}}

    @staticmethod
    def email() -> dict:
        """Email column.

        Returns:
            ``{"email": {}}``
        """
        return {"email": {}}

    @staticmethod
    def phone_number() -> dict:
        """Phone number column.

        Returns:
            ``{"phone_number": {}}``
        """
        return {"phone_number": {}}

    @staticmethod
    def people() -> dict:
        """People column.

        Returns:
            ``{"people": {}}``
        """
        return {"people": {}}

    @staticmethod
    def files() -> dict:
        """Files column.

        Returns:
            ``{"files": {}}``
        """
        return {"files": {}}

    @staticmethod
    def relation(
        database_id: str,
        *,
        type: str = "single_property",
        synced_property_name: Optional[str] = None,
        synced_property_id: Optional[str] = None,
    ) -> dict:
        """Relation column.

        Args:
            database_id: The ID of the related database.
            type: Either ``"single_property"`` (one-way) or
                ``"dual_property"`` (two-way synced).
            synced_property_name: For ``dual_property`` only – the name of
                the mirrored property in the related database.
            synced_property_id: For ``dual_property`` only – the ID of the
                mirrored property.

        Returns:
            Notion relation property schema dict.
        """
        config: dict = {"database_id": database_id, "type": type}
        if type == "dual_property":
            synced: dict = {}
            if synced_property_name is not None:
                synced["synced_property_name"] = synced_property_name
            if synced_property_id is not None:
                synced["synced_property_id"] = synced_property_id
            config["dual_property"] = synced
        else:
            config["single_property"] = {}
        return {"relation": config}

    @staticmethod
    def rollup(
        relation_property_name: str,
        rollup_property_name: str,
        function: str,
        *,
        relation_property_id: Optional[str] = None,
        rollup_property_id: Optional[str] = None,
    ) -> dict:
        """Rollup column.

        Args:
            relation_property_name: The name of the relation column to roll up.
            rollup_property_name: The name of the property in the related
                database to aggregate.
            function: Aggregation function.  One of ``"average"``, ``"checked"``,
                ``"count_per_group"``, ``"count"``, ``"count_values"``,
                ``"date_range"``, ``"earliest_date"``, ``"empty"``,
                ``"latest_date"``, ``"max"``, ``"median"``, ``"min"``,
                ``"not_empty"``, ``"percent_checked"``,
                ``"percent_empty"``, ``"percent_not_empty"``,
                ``"percent_per_group"``, ``"percent_unchecked"``, ``"range"``,
                ``"unchecked"``, ``"unique"``, ``"show_original"``,
                ``"show_unique"``, or ``"sum"``.
            relation_property_id: Optional ID of the relation column (alternative
                to ``relation_property_name`` for ID-based lookup).
            rollup_property_id: Optional ID of the property in the related
                database (alternative to ``rollup_property_name``).

        Returns:
            Notion rollup property schema dict.
        """
        config: dict = {
            "relation_property_name": relation_property_name,
            "rollup_property_name": rollup_property_name,
            "function": function,
        }
        if relation_property_id is not None:
            config["relation_property_id"] = relation_property_id
        if rollup_property_id is not None:
            config["rollup_property_id"] = rollup_property_id
        return {"rollup": config}

    @staticmethod
    def formula(expression: str) -> dict:
        """Formula column.

        Args:
            expression: The Notion formula expression string.

        Returns:
            ``{"formula": {"expression": expression}}``
        """
        return {"formula": {"expression": expression}}

    @staticmethod
    def created_time() -> dict:
        """Created time column (read-only).

        Returns:
            ``{"created_time": {}}``
        """
        return {"created_time": {}}

    @staticmethod
    def created_by() -> dict:
        """Created by column (read-only).

        Returns:
            ``{"created_by": {}}``
        """
        return {"created_by": {}}

    @staticmethod
    def last_edited_time() -> dict:
        """Last edited time column (read-only).

        Returns:
            ``{"last_edited_time": {}}``
        """
        return {"last_edited_time": {}}

    @staticmethod
    def last_edited_by() -> dict:
        """Last edited by column (read-only).

        Returns:
            ``{"last_edited_by": {}}``
        """
        return {"last_edited_by": {}}

    @staticmethod
    def unique_id(*, prefix: Optional[str] = None) -> dict:
        """Unique ID column (auto-incremented, read-only).

        Args:
            prefix: Optional prefix string for the ID.

        Returns:
            Notion unique_id property schema dict.
        """
        config: dict = {}
        if prefix is not None:
            config["prefix"] = prefix
        return {"unique_id": config}

    @staticmethod
    def button() -> dict:
        """Button column (triggers a configured automation when clicked).

        Returns:
            ``{"button": {}}``
        """
        return {"button": {}}

    @staticmethod
    def location() -> dict:
        """Location column (stores a geographic location / address).

        Returns:
            ``{"location": {}}``
        """
        return {"location": {}}

    @staticmethod
    def last_visited_time() -> dict:
        """Last visited time column (read-only; tracks when a page was last
        opened by a user).

        Returns:
            ``{"last_visited_time": {}}``
        """
        return {"last_visited_time": {}}

    @staticmethod
    def verification() -> dict:
        """Verification column for wiki pages (Notion-Version: 2026-03-11).

        Stores a verification state (``"verified"`` or ``"unverified"``) and
        an optional expiration date.  Only available on wiki databases.

        Returns:
            ``{"verification": {}}``
        """
        return {"verification": {}}
