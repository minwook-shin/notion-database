"""
notion-database 2.0 — end-to-end example

Set the NOTION_KEY environment variable to your Notion Internal Integration
token before running:

    export NOTION_KEY=secret_xxx
    python example.py

Alternatively, create a .env file in the project root and python-dotenv will
load it automatically.
"""
import logging
import os
import pprint
import time

try:
    from dotenv import load_dotenv
    load_dotenv()
except ModuleNotFoundError:
    pass

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
from notion_database.const import (
    BLUE, BLUE_BACKGROUND, BROWN, GREEN, RED, RED_BACKGROUND,
)

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s %(message)s")
log = logging.getLogger(__name__)

NOTION_KEY = os.environ["NOTION_KEY"]
client = NotionClient(NOTION_KEY)

# ──────────────────────────────────────────────
# 1. Search databases
# ──────────────────────────────────────────────
log.debug("=== 1. Search databases ===")
search_result = client.search.search_databases(
    sort={"direction": "ascending", "timestamp": "last_edited_time"},
)
databases = search_result["results"]
log.debug("found %d database(s)", len(databases))

if not databases:
    log.warning("No accessible databases found. Make sure the integration is shared with a page.")
    raise SystemExit(0)

# Search may return trashed / archived databases, or databases the integration
# can discover but cannot access directly. Skip those and use the first live,
# retrievable one.
#
# NOTE (Notion-Version 2026-03-11): search returns object:"data_source"
# wrappers; search_databases() normalises result["id"] to the real database ID
# but the wrapper still carries the property schema in result["properties"].
# databases.retrieve() returns the database container which no longer contains
# a "properties" key — properties now live on the data_source object.
database_id = None
db = None
datasource = None  # data_source object from search (carries "properties")
data_source_id = None  # original data_source ID (for schema/page/query ops)
for candidate in databases:
    if candidate.get("in_trash") or candidate.get("archived"):
        log.debug("skipping trashed/archived database %s", candidate["id"])
        continue
    cid = candidate["id"]
    try:
        db = client.databases.retrieve(cid)
        database_id = cid
        datasource = candidate  # keep for property schema access
        # In 2026-03-11 the database container lists its data_sources.
        # Schema updates, page creation, and queries must target the
        # data_source ID, not the parent database container ID.
        ds_list = db.get("data_sources") or []
        if ds_list:
            data_source_id = ds_list[0]["id"]
        log.debug("using database: %s  data_source: %s", database_id, data_source_id)
        break
    except Exception as e:
        log.debug("skipping database %s (%s)", cid, e)

if database_id is None:
    log.warning(
        "No accessible database found among %d result(s). "
        "Share at least one database directly with your integration.",
        len(databases),
    )
    raise SystemExit(0)

# ──────────────────────────────────────────────
# 2. Retrieve and update a database
# ──────────────────────────────────────────────
log.debug("=== 2. Retrieve & update database ===")
pprint.pprint(db)

# Update title, icon, cover, and layout options
client.databases.update(
    database_id,
    title=[RichText.text("Updated DB")],
    icon=Icon.emoji("📚"),
    cover=Cover.external("https://github.githubassets.com/images/modules/logos_page/Octocat.png"),
    is_inline=False,   # show as full-page (not inline on parent page)
    is_locked=False,   # ensure the database is editable
)

# ──────────────────────────────────────────────
# 3. Ensure required columns exist in the database
# ──────────────────────────────────────────────
log.debug("=== 3. Ensure required columns ===")

REQUIRED_PROPERTIES = {
    "description":   PropertySchema.rich_text(),
    "number":        PropertySchema.number(),
    "number-float":  PropertySchema.number(),
    "select":        PropertySchema.select(),
    "multi_select":  PropertySchema.multi_select(),
    "multi_select2": PropertySchema.multi_select(),
    "checkbox":      PropertySchema.checkbox(),
    "url":           PropertySchema.url(),
    "email":         PropertySchema.email(),
    "phone":         PropertySchema.phone_number(),
    "date":          PropertySchema.date(),
    "file":          PropertySchema.files(),
}

# In 2026-03-11 the database container has no "properties"; use the
# data_source object (from search) which still carries the schema.
ds_properties = (datasource or {}).get("properties") or db.get("properties") or {}
existing = set(ds_properties.keys())
missing = {k: v for k, v in REQUIRED_PROPERTIES.items() if k not in existing}

if missing:
    log.debug("adding missing columns: %s", list(missing.keys()))
    # In 2026-03-11 only PATCH /databases/{database_id} (container) returns
    # 200; PATCH on the data_source_id returns 404.  Use the container ID for
    # schema updates and verify what the response contains.
    updated = client.databases.update(database_id, properties=missing)
    log.debug("update response object=%r id=%r has_props=%r",
              updated.get("object"), updated.get("id"),
              list((updated.get("properties") or {}).keys()) or "none")
else:
    log.debug("all required columns already exist")

# ──────────────────────────────────────────────
# 4. Create a page (all PropertyValue types + all BlockContent types)
# ──────────────────────────────────────────────
log.debug("=== 4. Create page ===")
# In 2026-03-11 pages (rows) are created inside the data_source, not the
# database container.  Fall back to database_id for older API versions.
page = client.pages.create(
    parent={"database_id": data_source_id or database_id},
    properties={
        "title":         PropertyValue.title([
                             RichText.text("Hello, "),
                             RichText.text("Notion 2.0!", bold=True),
                         ]),
        "description":   PropertyValue.rich_text("Example page created by notion-database 2.0"),
        "number":        PropertyValue.number(1),
        "number-float":  PropertyValue.number(1.5),
        "select":        PropertyValue.select("test1"),
        "multi_select":  PropertyValue.multi_select(["test1", "test2"]),
        "multi_select2": PropertyValue.multi_select(["test1", "test2", "test3"]),
        "checkbox":      PropertyValue.checkbox(True),
        "url":           PropertyValue.url("https://www.google.com"),
        "email":         PropertyValue.email("test@test.com"),
        "phone":         PropertyValue.phone_number("+1-555-0100"),
        "date":          PropertyValue.date("2024-01-01T00:00:00.000+09:00"),
        "file":          PropertyValue.files([
                             "https://github.githubassets.com/images/modules/logos_page/Octocat.png"
                         ]),
    },
    icon=Icon.emoji("📚"),
    cover=Cover.external("https://github.githubassets.com/images/modules/logos_page/Octocat.png"),
    children=[
        # Title and intro
        BlockContent.heading_1("notion-database 2.0 Example"),
        BlockContent.paragraph([
            RichText.text("This page was created with "),
            RichText.text("notion-database 2.0", bold=True),
            RichText.text("."),
        ]),

        # Structural
        BlockContent.divider(),
        BlockContent.table_of_contents(),
        BlockContent.breadcrumb(),

        # Text blocks
        BlockContent.heading_2("Text Blocks"),
        BlockContent.paragraph("Plain paragraph", color=BLUE),
        BlockContent.heading_1("Heading 1"),
        BlockContent.heading_2("Heading 2", color=BLUE_BACKGROUND),
        BlockContent.heading_3("Heading 3", color=GREEN),
        BlockContent.callout("This is a callout.", color=RED_BACKGROUND),
        BlockContent.quote("This is a quote.", color=RED),

        # Lists
        BlockContent.heading_2("List Blocks"),
        BlockContent.bulleted_list_item("Bullet item 1"),
        BlockContent.bulleted_list_item("Bullet item 2", color=BROWN),
        BlockContent.bulleted_list_item("Nested bullet", children=[
            BlockContent.bulleted_list_item("Child item"),
        ]),
        BlockContent.numbered_list_item("Numbered item 1"),
        BlockContent.numbered_list_item("Numbered item 2", color=BROWN),
        BlockContent.to_do("Completed task", checked=True),
        BlockContent.to_do("Pending task", checked=False, color=RED),

        # Toggle
        BlockContent.toggle("Toggle header", color=BLUE, children=[
            BlockContent.paragraph("Hidden content inside the toggle."),
        ]),

        # Code
        BlockContent.heading_2("Code Blocks"),
        BlockContent.code('print("Hello, Notion!")', language="python"),
        BlockContent.code("const a = 1;", language="javascript"),
        BlockContent.code("SELECT * FROM pages;", language="sql"),

        # Math
        BlockContent.equation("E = mc^2"),

        # Media
        BlockContent.heading_2("Media Blocks"),
        BlockContent.image(
            "https://github.githubassets.com/images/modules/logos_page/Octocat.png",
            caption="GitHub Octocat",
        ),
        BlockContent.video("https://download.blender.org/peach/trailer/trailer_480p.mov"),
        BlockContent.file("https://github.com/microsoft/ML-For-Beginners/raw/main/pdf/readme.pdf"),
        BlockContent.pdf("https://github.com/microsoft/ML-For-Beginners/blob/main/pdf/readme.pdf"),
        BlockContent.embed("https://www.google.com"),
        BlockContent.bookmark("https://www.google.com"),

        # Column layout
        BlockContent.heading_2("Column Layout"),
        BlockContent.column_list([
            [BlockContent.paragraph("Left column")],
            [BlockContent.paragraph("Right column")],
        ]),
    ],
)

page_id = page["id"]
log.debug("created page: %s", page_id)

# ──────────────────────────────────────────────
# 5. Retrieve the page
# ──────────────────────────────────────────────
log.debug("=== 5. Retrieve page ===")
page = client.pages.retrieve(page_id)
pprint.pprint(page)

# ──────────────────────────────────────────────
# 6. Update the page
# ──────────────────────────────────────────────
log.debug("=== 6. Update page ===")
client.pages.update(
    page_id,
    properties={
        "title":       PropertyValue.title("Updated Title"),
        "description": PropertyValue.rich_text("Updated description"),
        "number":      PropertyValue.number(2),
        "checkbox":    PropertyValue.checkbox(False),
        "date":        PropertyValue.date(
                           "2024-01-01T00:00:00.000+09:00",
                           end="2024-01-31T00:00:00.000+09:00",
                       ),
        "file":        PropertyValue.files([
                           "https://github.githubassets.com/images/modules/logos_page/Octocat.png",
                           "https://download.blender.org/peach/trailer/trailer_480p.mov",
                       ]),
    },
    icon=Icon.external("https://github.githubassets.com/images/modules/logos_page/Octocat.png"),
    cover=Cover.external("https://github.githubassets.com/images/modules/logos_page/Octocat.png"),
)

# ──────────────────────────────────────────────
# 7. Retrieve block children
# ──────────────────────────────────────────────
log.debug("=== 7. Retrieve block children ===")
blocks_response = client.blocks.retrieve_children(page_id, page_size=5)
pprint.pprint(blocks_response)

first_block_id = blocks_response["results"][0]["id"]
block = client.blocks.retrieve(first_block_id)
pprint.pprint(block)

# Fetch all children with automatic pagination
all_blocks = client.blocks.retrieve_all_children(page_id)
log.debug("total blocks: %d", len(all_blocks))

# Append blocks at end (default) and at start using position param (2026-03-11)
client.blocks.append_children(page_id, children=[
    BlockContent.paragraph("This block was appended after page creation."),
])
client.blocks.append_children(page_id, children=[
    BlockContent.paragraph("This block was prepended to the top."),
], position={"type": "start"})

# Tab layout (Notion-Version: 2026-03-11) — append_children only,
# not supported in pages.create children
try:
    client.blocks.append_children(page_id, children=[
        BlockContent.tab_group([
            BlockContent.tab("Overview", [BlockContent.paragraph("Overview content")]),
            BlockContent.tab("Details",  [BlockContent.paragraph("Details content")]),
        ]),
    ])
    log.debug("tab_group appended successfully")
except Exception as e:
    log.warning("tab_group not supported via append_children: %s", e)

# ──────────────────────────────────────────────
# 8. Query the database (filters + sorts)
# ──────────────────────────────────────────────
log.debug("=== 8. Query database ===")
# In 2026-03-11 queries target the data_source, not the database container.
query_id = data_source_id or database_id

# Simple filter — only non-trashed pages
result = client.databases.query(
    query_id,
    filter=Filter.checkbox("checkbox").equals(False),
    sorts=[Sort.by_property("title")],
    in_trash=False,
)
pprint.pprint(result)

# OR compound filter
result = client.databases.query(
    query_id,
    filter=Filter.or_([
        Filter.checkbox("checkbox").equals(False),
        Filter.number("number").greater_than_or_equal_to(2),
    ]),
)
pprint.pprint(result)

# Nested AND + OR filter
result = client.databases.query(
    query_id,
    filter=Filter.and_([
        Filter.text("title").is_not_empty(),
        Filter.or_([
            Filter.select("select").equals("test1"),
            Filter.number("number").less_than(10),
        ]),
    ]),
    sorts=[
        Sort.descending("number"),
        Sort.by_timestamp("last_edited_time", "descending"),
    ],
)
pprint.pprint(result)

# Filter by result_type: only pages (excludes embedded data sources)
result = client.databases.query(
    query_id,
    result_type="page",
)
log.debug("page-type results: %d", len(result.get("results", [])))

# Filters for people-type properties (created_by / last_edited_by)
# Replace "user-id" with a real Notion user ID
# result = client.databases.query(
#     database_id,
#     filter=Filter.created_by("Created By").contains("user-id"),
# )

# Formula, rollup, and verification filters (escape-hatch via Filter.raw
# or the dedicated helpers below)
# Filter.formula("Computed", "string").equals("ok")
# Filter.formula("Score",    "number").greater_than(50)
# Filter.rollup("Tasks",     "any",    "number").greater_than(0)
# Filter.rollup("Tags",      "every",  "rich_text").contains("urgent")
# Filter.verification("Verified").equals("verified")

# Fetch all results with automatic pagination
all_pages = client.databases.query_all(query_id, in_trash=False)
log.debug("total pages: %d", len(all_pages))

# ──────────────────────────────────────────────
# 9. Archive and restore the page
# ──────────────────────────────────────────────
log.debug("=== 9. Archive & restore page ===")
time.sleep(1)
client.pages.archive(page_id)
log.debug("page archived")

time.sleep(1)
client.pages.archive(page_id, archived=False)
log.debug("page restored")

# ──────────────────────────────────────────────
# 10. Create a child database (all PropertySchema types)
# ──────────────────────────────────────────────
log.debug("=== 10. Create child database ===")
child_db = client.databases.create(
    parent={"type": "page_id", "page_id": page_id},
    title=[RichText.text("Child Database")],
    is_inline=False,
    properties={
        # Core text
        "Name":          PropertySchema.title(),
        "Description":   PropertySchema.rich_text(),
        "Website":       PropertySchema.url(),
        "Email":         PropertySchema.email(),
        "Phone":         PropertySchema.phone_number(),

        # Numeric
        "Score":         PropertySchema.number(),
        "Price":         PropertySchema.number("dollar"),

        # Selection
        "Category":      PropertySchema.select([
                             {"name": "Option A", "color": "green"},
                             {"name": "Option B", "color": "red"},
                         ]),
        "Tags":          PropertySchema.multi_select(),
        "Status":        PropertySchema.status(),

        # Date / time (read-only columns included for reference)
        "Due":           PropertySchema.date(),
        "Created":       PropertySchema.created_time(),
        "CreatedBy":     PropertySchema.created_by(),
        "LastEdited":    PropertySchema.last_edited_time(),
        "LastEditedBy":  PropertySchema.last_edited_by(),

        # Other
        "Active":        PropertySchema.checkbox(),
        "Attachment":    PropertySchema.files(),
        "People":        PropertySchema.people(),

        # Special (2026-03-11 and newer)
        "Action":        PropertySchema.button(),        # automation trigger
        "Location":      PropertySchema.location(),      # geographic location
        # "LastVisited": PropertySchema.last_visited_time(),  # read-only; add if supported

        # Computed
        "Formula":       PropertySchema.formula("prop('Score') * 2"),
        "UniqueID":      PropertySchema.unique_id(prefix="ITEM"),
    },
    icon=Icon.external("https://github.githubassets.com/images/modules/logos_page/Octocat.png"),
    cover=Cover.external("https://github.githubassets.com/images/modules/logos_page/Octocat.png"),
)
child_db_id = child_db["id"]
log.debug("child database: %s", child_db_id)

# Lock the child database to prevent accidental edits
client.databases.update(child_db_id, is_locked=True)
log.debug("child database locked")

# ──────────────────────────────────────────────
# 11. Markdown API (Notion-Version: 2026-03-11)
# ──────────────────────────────────────────────
log.debug("=== 11. Markdown API ===")
md_response = client.pages.retrieve_markdown(page_id)
log.debug("markdown length: %d chars", len(md_response.get("markdown", "")))
log.debug("truncated: %s", md_response.get("truncated"))

# Replace page content with Markdown
client.pages.update_markdown(
    page_id,
    markdown="# Updated via Markdown\n\nThis content was written using the Markdown API.",
)
log.debug("page content replaced via Markdown API")

# ──────────────────────────────────────────────
# 12. Users
# ──────────────────────────────────────────────
log.debug("=== 12. Users ===")
me = client.users.me()
log.debug("bot user: %s", me.get("name"))

# Listing all users requires the integration to have user-reading capability
# enabled in the Notion workspace settings. Skip gracefully if not permitted.
try:
    all_users = client.users.list_all()
    log.debug("workspace users: %d", len(all_users))
except Exception as e:
    log.warning("could not list users (insufficient permissions): %s", e)

log.debug("=== Done ===")
