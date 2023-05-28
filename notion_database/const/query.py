"""
query setting
"""
from enum import Enum


class Direction(Enum):
    """
    query direction enum
    """
    ascending = "ascending"  # pylint: disable=invalid-name
    descending = "descending"  # pylint: disable=invalid-name


class Timestamp(Enum):
    """
    query timestamp enum

    Limitation: only a single sort is allowed and is limited to last_edited_time.
    """
    # created_time = "created_time"
    last_edited_time = "last_edited_time"  # pylint: disable=invalid-name


class Filter:  # pylint: disable=too-few-public-methods
    """
    Not Implemented
    """
    def __init__(self):
        pass


class Sort:  # pylint: disable=too-few-public-methods
    """
    Not Implemented
    """
    def __init__(self):
        pass
