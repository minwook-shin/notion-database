from enum import Enum


class Direction(Enum):
    ascending = "ascending"
    descending = "descending"


class Timestamp(Enum):
    # Limitation: Search - Currently only a single sort is allowed and is limited to last_edited_time.
    # created_time = "created_time"
    last_edited_time = "last_edited_time"


class Filter:
    # Not Implemented
    def __init__(self):
        pass


class Sort:
    # Not Implemented
    def __init__(self):
        pass
