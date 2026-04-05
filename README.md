[![Test Python Package](https://github.com/minwook-shin/notion-database/actions/workflows/python-publish.yml/badge.svg)](https://github.com/minwook-shin/notion-database/actions/workflows/python-publish.yml)

> [!IMPORTANT]
> **Upgrading from v1.4?**
> Version 2.0 is a full redesign with a new API — `NotionClient` replaces the old `Page`, `Database`, and `Search` classes.
> v1.4.x will continue to receive security fixes only. See the [migration table](#install) and [CHANGELOG](CHANGELOG.md) for details.

# notion-database

> Python client for the Notion API — easy to use, 1-to-1 API mapping, AI/MCP friendly

**Notion API version supported: `2026-03-11`**

## What's new in 2.0

| Feature | Description |
|---|---|
| `client.pages.retrieve_markdown()` | Retrieve a page as enhanced Markdown (`GET /pages/{id}/markdown`) |
| `client.pages.update_markdown()` | Replace page content with Markdown (`POST /pages/{id}/markdown`) |
| `client.pages.create(timezone=...)` | IANA timezone for template variables (`@now`, `@today`) |
| `client.blocks.append_children(position=...)` | Insert blocks at `start`, `end`, or `after_block` |
| `client.databases.query(in_trash=...)` | Filter trashed / non-trashed rows |
| `client.databases.update(is_inline=..., in_trash=..., is_locked=...)` | Toggle inline layout, trash, and lock state |
| `client.databases.create(initial_data_source=...)` | Pre-populate a database from a data source on creation |
| `PropertySchema.button()` | Automation button column |
| `PropertySchema.location()` | Geographic location column |
| `PropertySchema.last_visited_time()` | Last visited time column (read-only) |
| `PropertySchema.rollup(relation_property_id=..., rollup_property_id=...)` | ID-based rollup lookup params |
| `PropertySchema.verification()` | Wiki page verification column |
| `PropertyValue.verification()` | Set wiki page verification state |
| `BlockContent.tab()` / `tab_group()` | Tab layout blocks |
| `Filter.created_by()` / `last_edited_by()` | Filter by creator or last editor |
| `Filter.formula(name, value_type)` | Filter on formula property results |
| `Filter.rollup(name, aggregate, value_type)` | Filter on rollup aggregates |
| `Filter.verification()` | Filter on wiki verification state |

## Install

```bash
pip install notion-database==2.0.0rc1
```

## Quick start

```python
from notion_database import (
    NotionClient,
    PropertyValue,
    PropertySchema,
    BlockContent,
    RichText,
    Filter,
    Sort,
    Icon,
    Cover,
)

client = NotionClient("secret_xxx")
```

## Databases

```python
# Retrieve
db = client.databases.retrieve("database-id")

# Create
db = client.databases.create(
    parent={"type": "page_id", "page_id": "page-id"},
    title=[RichText.text("My Database")],
    properties={
        "Name":   PropertySchema.title(),
        "Status": PropertySchema.select([
            {"name": "Active", "color": "green"},
            {"name": "Done",   "color": "gray"},
        ]),
        "Score":  PropertySchema.number("number"),
        "Due":    PropertySchema.date(),
    },
)

# Query with filter and sort
results = client.databases.query(
    "database-id",
    filter=Filter.select("Status").equals("Active"),
    sorts=[Sort.descending("Score")],
    in_trash=False,        # exclude trashed rows
)
pages = results["results"]

# Compound filter
results = client.databases.query(
    "database-id",
    filter=Filter.and_([
        Filter.select("Status").equals("Active"),
        Filter.number("Score").greater_than(80),
    ]),
)

# Auto-paginate (returns all pages at once)
all_pages = client.databases.query_all("database-id", in_trash=False)

# Update schema — rename, lock, and set inline layout
client.databases.update(
    "database-id",
    title=[RichText.text("Renamed DB")],
    is_inline=False,  # full-page, not inline
    is_locked=True,   # prevent edits without unlocking
)
```

## Pages

```python
# Create
page = client.pages.create(
    parent={"database_id": "database-id"},
    properties={
        "Name":   PropertyValue.title("Hello, Notion 2.0!"),
        "Status": PropertyValue.select("Active"),
        "Score":  PropertyValue.number(95),
        "Due":    PropertyValue.date("2024-12-31"),
        "Done":   PropertyValue.checkbox(False),
    },
    icon=Icon.emoji("🚀"),
    cover=Cover.external("https://example.com/cover.jpg"),
    children=[
        BlockContent.heading_1("Introduction"),
        BlockContent.paragraph("This page was created via notion-database 2.0."),
    ],
)

# Retrieve
page = client.pages.retrieve("page-id")

# Update properties
client.pages.update(
    "page-id",
    properties={
        "Status": PropertyValue.select("Done"),
        "Done":   PropertyValue.checkbox(True),
    },
)

# Archive / restore
client.pages.archive("page-id")
client.pages.archive("page-id", archived=False)
```

## Blocks

```python
# Append content to a page (inserted at end by default)
client.blocks.append_children(
    "page-id",
    children=[
        BlockContent.heading_2("Section"),
        BlockContent.paragraph([
            RichText.text("Normal text, "),
            RichText.text("bold", bold=True),
            RichText.text(", and "),
            RichText.text("italic", italic=True),
        ]),
        BlockContent.bulleted_list_item("First item"),
        BlockContent.bulleted_list_item("Second item"),
        BlockContent.to_do("Finish docs", checked=False),
        BlockContent.code("print('hello')", language="python"),
        BlockContent.divider(),
        BlockContent.image("https://example.com/image.png", caption="Fig 1"),
        BlockContent.column_list([
            [BlockContent.paragraph("Left column")],
            [BlockContent.paragraph("Right column")],
        ]),
        # Tab layout (Notion-Version: 2026-03-11)
        BlockContent.tab_group([
            BlockContent.tab("Overview", [BlockContent.paragraph("Overview content")]),
            BlockContent.tab("Details",  [BlockContent.paragraph("Details content")]),
        ]),
    ],
)

# Insert at a specific position (Notion-Version: 2026-03-11)
client.blocks.append_children("page-id", children=[
    BlockContent.paragraph("Prepended to top"),
], position={"type": "start"})

client.blocks.append_children("page-id", children=[
    BlockContent.paragraph("After a specific block"),
], position={"type": "after_block", "after_block": {"id": "block-id"}})

# Retrieve children (single page)
response = client.blocks.retrieve_children("page-id")
blocks = response["results"]

# Auto-paginate all children
all_blocks = client.blocks.retrieve_all_children("page-id")

# Delete a block
client.blocks.delete("block-id")
```

## Search

```python
# Search all
results = client.search.search("Project")

# Filter by type
db_results = client.search.search_databases("Project")
page_results = client.search.search_pages("Meeting notes")

# Auto-paginate all results
all_results = client.search.search_all("Q1")
```

## Users

```python
# Current bot
me = client.users.me()

# List all workspace users
all_users = client.users.list_all()

# Retrieve by ID
user = client.users.retrieve("user-id")
```

## Comments

```python
# Retrieve comments on a page
comments = client.comments.retrieve("page-id")

# Post a comment
client.comments.create(
    parent={"page_id": "page-id"},
    rich_text=[RichText.text("Great work!")],
)
```

## Filters reference

```python
# Text / title
Filter.text("Name").equals("Alice")
Filter.text("Name").contains("Al")
Filter.text("Name").starts_with("A")
Filter.text("Name").is_empty()

# Number
Filter.number("Score").greater_than(80)
Filter.number("Score").less_than_or_equal_to(100)

# Checkbox
Filter.checkbox("Done").equals(True)

# Select / status
Filter.select("Status").equals("Active")
Filter.status("Status").does_not_equal("Archived")

# Multi-select
Filter.multi_select("Tags").contains("python")

# Date
Filter.date("Due").before("2025-01-01")
Filter.date("Due").past_week()
Filter.date("Due").next_month()

# People-type columns
Filter.people("Assignee").contains("user-id")
Filter.created_by("Created By").contains("user-id")
Filter.last_edited_by("Last Edited By").does_not_contain("user-id")

# Timestamp columns
Filter.created_time().after("2024-01-01")
Filter.last_edited_time().past_week()

# Formula (value_type: "string" | "number" | "checkbox" | "date")
Filter.formula("Computed", "string").equals("ok")
Filter.formula("Score",    "number").greater_than(50)

# Rollup (aggregate: "any" | "every" | "none" | "number"; value_type: property type)
Filter.rollup("Tasks", "any",   "number").greater_than(0)
Filter.rollup("Tags",  "every", "rich_text").contains("urgent")

# Verification (wiki pages)
Filter.verification("Verified").equals("verified")

# Compound
Filter.and_([
    Filter.select("Status").equals("Active"),
    Filter.number("Score").greater_than(80),
])
Filter.or_([
    Filter.text("Name").contains("Alice"),
    Filter.text("Name").contains("Bob"),
])

# Nested compound
Filter.and_([
    Filter.checkbox("Done").equals(False),
    Filter.or_([
        Filter.select("Priority").equals("High"),
        Filter.date("Due").before("2025-01-01"),
    ]),
])

# Raw (escape hatch)
Filter.raw({"property": "Formula", "formula": {"string": {"equals": "ok"}}})
```

## Sorts reference

```python
Sort.by_property("Name")                      # ascending by default
Sort.by_property("Score", "descending")
Sort.ascending("Name")                        # alias
Sort.descending("CreatedAt")                  # alias
Sort.by_timestamp("created_time", "descending")
Sort.by_timestamp("last_edited_time")
```

## RichText reference

```python
RichText.text("plain")
RichText.text("bold", bold=True)
RichText.text("italic", italic=True)
RichText.text("underline", underline=True)
RichText.text("strike", strikethrough=True)
RichText.text("code", code=True)
RichText.text("colored", color="red")
RichText.text("link", link="https://example.com")

RichText.mention_page("page-id")
RichText.mention_database("db-id")
RichText.mention_user("user-id")
RichText.mention_date("2024-01-01", end="2024-01-31")
RichText.equation("E=mc^2")
```

## PropertySchema reference

```python
from notion_database import PropertySchema

{
    # Text
    "Name":         PropertySchema.title(),
    "Notes":        PropertySchema.rich_text(),
    "Website":      PropertySchema.url(),
    "Email":        PropertySchema.email(),
    "Phone":        PropertySchema.phone_number(),

    # Numeric
    "Score":        PropertySchema.number("number"),
    "Price":        PropertySchema.number("dollar"),

    # Selection
    "Category":     PropertySchema.select([{"name": "A", "color": "green"}]),
    "Tags":         PropertySchema.multi_select(),
    "Status":       PropertySchema.status(),

    # Date / time (read-only system columns)
    "Due":          PropertySchema.date(),
    "Created":      PropertySchema.created_time(),
    "CreatedBy":    PropertySchema.created_by(),
    "LastEdited":   PropertySchema.last_edited_time(),
    "LastEditedBy": PropertySchema.last_edited_by(),

    # Other
    "Done":         PropertySchema.checkbox(),
    "Files":        PropertySchema.files(),
    "People":       PropertySchema.people(),

    # Special (2026-03-11)
    "Action":       PropertySchema.button(),           # automation trigger
    "Location":     PropertySchema.location(),         # geographic location
    "LastVisited":  PropertySchema.last_visited_time(), # read-only

    # Computed
    "Formula":      PropertySchema.formula("prop('Score') * 2"),
    "UniqueID":     PropertySchema.unique_id(prefix="ITEM"),
    "Related":      PropertySchema.relation("other-database-id"),
    "Rollup":       PropertySchema.rollup("Related", "Count", "count"),
    # ID-based rollup (stable against column renames)
    "RollupByID":   PropertySchema.rollup(
                        "Related", "Count", "sum",
                        relation_property_id="rel-id",
                        rollup_property_id="prop-id",
                    ),
    # Verification (wiki databases only)
    "Verified":     PropertySchema.verification(),
}
```

## Error handling

```python
from notion_database import (
    NotionAPIError,
    NotionNotFoundError,
    NotionRateLimitError,
    NotionUnauthorizedError,
)
import time

try:
    page = client.pages.retrieve("invalid-id")
except NotionNotFoundError:
    print("Page not found")
except NotionRateLimitError:
    time.sleep(1)
    page = client.pages.retrieve("invalid-id")
except NotionUnauthorizedError:
    print("Check your integration token")
except NotionAPIError as e:
    print(f"[{e.status_code}] {e.code}: {e.message}")
```

## Color constants

```python
from notion_database.const import (
    DEFAULT, GRAY, BROWN, ORANGE, YELLOW, GREEN, BLUE, PURPLE, PINK, RED,
    GRAY_BACKGROUND, BROWN_BACKGROUND, ORANGE_BACKGROUND, YELLOW_BACKGROUND,
    GREEN_BACKGROUND, BLUE_BACKGROUND, PURPLE_BACKGROUND, PINK_BACKGROUND,
    RED_BACKGROUND,
)

BlockContent.paragraph("Highlighted", color=RED_BACKGROUND)
```

## MCP integration

`NotionClient` is designed to map directly to Notion API endpoints, making it
straightforward to expose as MCP tools.  Each sub-client (`databases`,
`pages`, `blocks`, `search`, `users`, `comments`) corresponds to one section
of the Notion API docs.  All parameters are typed and documented, so an AI can
introspect the signatures without additional context.

## License

LGPLv3
