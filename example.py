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
# 1. Find a parent page; fall back to an existing database
# ──────────────────────────────────────────────
log.debug("=== 1. Find parent page ===")

# Strategy 1: search with the "page" filter
parent_page_id = None
page_result = client.search.search_pages(
    sort={"direction": "Ascending", "timestamp": "last_edited_time"},
)
for p in page_result["results"]:
    if not p.get("in_trash") and not p.get("archived"):
        parent_page_id = p["id"]
        log.debug("found page via page filter: %s", parent_page_id)
        break

# Strategy 2: search everything, look for object:"page"
if parent_page_id is None:
    all_result = client.search.search(
        sort={"direction": "descending", "timestamp": "last_edited_time"},
    )
    for obj in all_result["results"]:
        if (obj.get("object") == "page"
                and not obj.get("in_trash")
                and not obj.get("archived")):
            parent_page_id = obj["id"]
            log.debug("found page via unfiltered search: %s", parent_page_id)
            break

# Strategy 3: fall back to any accessible database and work with its schema
database_id = None
data_source_id = None
fallback_db = None
available_properties: set = set()
if parent_page_id is None:
    log.debug("no page found — falling back to existing database")
    db_search = client.search.search_databases(
        sort={"direction": "ascending", "timestamp": "last_edited_time"},
    )
    for candidate in db_search["results"]:
        if candidate.get("in_trash") or candidate.get("archived"):
            continue
        try:
            fallback_db = client.databases.retrieve(candidate["id"])
            database_id = candidate["id"]
            ds_list = fallback_db.get("data_sources") or []
            data_source_id = ds_list[0]["id"] if ds_list else None
            log.debug("using existing database: %s", database_id)
            break
        except Exception as e:
            log.debug("skipping database %s (%s)", candidate["id"], e)

if parent_page_id is None and database_id is None:
    log.warning(
        "No accessible page or database found. "
        "Share at least one page with your integration."
    )
    raise SystemExit(0)

# ──────────────────────────────────────────────
# 2. Create a fresh example database (or reuse existing)
# ──────────────────────────────────────────────
log.debug("=== 2. Create / reuse example database ===")

ALL_PROPERTIES = {
    "title":         PropertySchema.title(),
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

DB_TITLE = "notion-database 2.0 Example DB"

if parent_page_id is not None:
    # Reuse an existing example database with the same title if one exists,
    # so re-running the example doesn't create duplicate databases.
    db_obj = None
    search_result = client.search.search_databases(DB_TITLE)
    for r in search_result["results"]:
        if r.get("in_trash") or r.get("archived"):
            continue
        # Match on plain-text title
        title_parts = r.get("title") or []
        plain = "".join(t.get("plain_text", "") for t in title_parts)
        if plain == DB_TITLE:
            db_obj = r
            log.debug("reusing existing database: %s", r["id"])
            break

    if db_obj is None:
        db_obj = client.databases.create(
            parent={"type": "page_id", "page_id": parent_page_id},
            title=[RichText.text(DB_TITLE)],
            is_inline=False,
            properties=ALL_PROPERTIES,
            icon=Icon.emoji("📚"),
        )
        log.debug("created database: %s", db_obj["id"])

    database_id = db_obj["id"]
    ds_list = db_obj.get("data_sources") or []
    data_source_id = ds_list[0]["id"] if ds_list else None
    log.debug("database_id: %s  data_source_id: %s", database_id, data_source_id)
    pprint.pprint(db_obj)
    # Determine which columns actually exist (2026-03-11 puts schema in data_source)
    if ds_list:
        available_properties = set((ds_list[0].get("properties") or {}).keys())
    else:
        available_properties = set((db_obj.get("properties") or {}).keys())
    available_properties.discard("title")
    available_properties.add("title")
    log.debug("available columns: %s", sorted(available_properties))
else:
    # Fallback: use existing database; only populate columns that exist
    pprint.pprint(fallback_db)
    # Get property names from the data_source (2026-03-11) or database object
    ds_props = {}
    if data_source_id:
        ds_refresh = client.search.search_databases()
        for r in ds_refresh["results"]:
            if r["id"] == database_id:
                ds_props = r.get("properties") or {}
                break
    available_properties = set(ds_props.keys()) | set(
        (fallback_db.get("properties") or {}).keys()
    )
    log.debug("existing columns: %s", sorted(available_properties))
    missing = set(ALL_PROPERTIES) - available_properties
    if missing:
        log.warning(
            "Using existing database — missing columns %s. "
            "Share a PAGE with the integration to let the example create its own database.",
            sorted(missing),
        )

# ──────────────────────────────────────────────
# 3. Retrieve and update the database metadata
# ──────────────────────────────────────────────
log.debug("=== 3. Retrieve & update database ===")
db = client.databases.retrieve(database_id)
pprint.pprint(db)

client.databases.update(
    database_id,
    title=[RichText.text("Updated Example DB")],
    icon=Icon.emoji("📚"),
    cover=Cover.external("https://github.githubassets.com/images/modules/logos_page/Octocat.png"),
    is_inline=False,
    is_locked=False,
)

# ──────────────────────────────────────────────
# 4. Create a page (all PropertyValue types + all BlockContent types)
# ──────────────────────────────────────────────
log.debug("=== 4. Create page ===")

# Build property values — only include columns that exist in this database
_ap = available_properties
page_properties: dict = {
    "title": PropertyValue.title([
        RichText.text("Hello, "),
        RichText.text("Notion 2.0!", bold=True),
    ]),
}
if "description"   in _ap: page_properties["description"]   = PropertyValue.rich_text("Example page created by notion-database 2.0")
if "number"        in _ap: page_properties["number"]        = PropertyValue.number(1)
if "number-float"  in _ap: page_properties["number-float"]  = PropertyValue.number(1.5)
if "select"        in _ap: page_properties["select"]        = PropertyValue.select("test1")
if "multi_select"  in _ap: page_properties["multi_select"]  = PropertyValue.multi_select(["test1", "test2"])
if "multi_select2" in _ap: page_properties["multi_select2"] = PropertyValue.multi_select(["test1", "test2", "test3"])
if "checkbox"      in _ap: page_properties["checkbox"]      = PropertyValue.checkbox(True)
if "url"           in _ap: page_properties["url"]           = PropertyValue.url("https://www.google.com")
if "email"         in _ap: page_properties["email"]         = PropertyValue.email("test@test.com")
if "phone"         in _ap: page_properties["phone"]         = PropertyValue.phone_number("+1-555-0100")
if "date"          in _ap: page_properties["date"]          = PropertyValue.date("2024-01-01T00:00:00.000+09:00")
if "file"          in _ap: page_properties["file"]          = PropertyValue.files([
    "https://github.githubassets.com/images/modules/logos_page/Octocat.png"
])

page = client.pages.create(
    parent={"database_id": database_id},
    properties=page_properties,
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
update_properties: dict = {"title": PropertyValue.title("Updated Title")}
if "description" in _ap: update_properties["description"] = PropertyValue.rich_text("Updated description")
if "number"      in _ap: update_properties["number"]      = PropertyValue.number(2)
if "checkbox"    in _ap: update_properties["checkbox"]    = PropertyValue.checkbox(False)
if "date"        in _ap: update_properties["date"]        = PropertyValue.date(
    "2024-01-01T00:00:00.000+09:00",
    end="2024-01-31T00:00:00.000+09:00",
)
if "file"        in _ap: update_properties["file"]        = PropertyValue.files([
    "https://github.githubassets.com/images/modules/logos_page/Octocat.png",
    "https://download.blender.org/peach/trailer/trailer_480p.mov",
])
client.pages.update(
    page_id,
    properties=update_properties,
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
# data_source_id is the queryable object in 2026-03-11; fall back to
# database_id for legacy databases that don't have a data_source.
query_id = data_source_id or database_id

# Simple filter — only non-trashed pages (skip if checkbox column not present)
if "checkbox" in _ap:
    result = client.databases.query(
        query_id,
        filter=Filter.checkbox("checkbox").equals(False),
        sorts=[Sort.by_property("title")],
    )
    pprint.pprint(result)

# OR compound filter
if "checkbox" in _ap and "number" in _ap:
    result = client.databases.query(
        query_id,
        filter=Filter.or_([
            Filter.checkbox("checkbox").equals(False),
            Filter.number("number").greater_than_or_equal_to(2),
        ]),
    )
    pprint.pprint(result)

# Nested AND + OR filter
if "select" in _ap and "number" in _ap:
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

# Fetch all results with automatic pagination
all_pages = client.databases.query_all(query_id)
log.debug("total pages: %d", len(all_pages))

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

# Append Markdown content to the bottom of the page
client.pages.append_markdown(
    page_id,
    markdown="## Appended via Markdown API\n\nThis section was added using the Markdown API.",
)
log.debug("markdown appended to page")

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
