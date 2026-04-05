"""
Sort builder for Notion database queries.

Reference: https://developers.notion.com/reference/post-database-query-sort
"""


class Sort:
    """Static factory methods for Notion database query sort objects.

    Pass a list of the returned dicts to the ``sorts`` parameter of
    :meth:`~notion_database.api.databases.DatabasesAPI.query`::

        results = client.databases.query(
            db_id,
            sorts=[
                Sort.by_property("Name", "ascending"),
                Sort.by_timestamp("created_time", "descending"),
            ],
        )

    Reference: https://developers.notion.com/reference/post-database-query-sort
    """

    @staticmethod
    def by_property(property_name: str, direction: str = "ascending") -> dict:
        """Sort by a property column.

        Args:
            property_name: The name of the property column to sort by.
            direction: ``"ascending"`` or ``"descending"``.

        Returns:
            ``{"property": property_name, "direction": direction}``
        """
        return {"property": property_name, "direction": direction}

    @staticmethod
    def by_timestamp(timestamp: str, direction: str = "ascending") -> dict:
        """Sort by a system timestamp.

        Args:
            timestamp: ``"created_time"`` or ``"last_edited_time"``.
            direction: ``"ascending"`` or ``"descending"``.

        Returns:
            ``{"timestamp": timestamp, "direction": direction}``
        """
        return {"timestamp": timestamp, "direction": direction}

    # Convenience aliases

    @staticmethod
    def ascending(property_name: str) -> dict:
        """Sort by a property column in ascending order.

        Args:
            property_name: The name of the property column to sort by.

        Returns:
            ``{"property": property_name, "direction": "ascending"}``
        """
        return Sort.by_property(property_name, "ascending")

    @staticmethod
    def descending(property_name: str) -> dict:
        """Sort by a property column in descending order.

        Args:
            property_name: The name of the property column to sort by.

        Returns:
            ``{"property": property_name, "direction": "descending"}``
        """
        return Sort.by_property(property_name, "descending")
