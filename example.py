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

database_id = databases[0]["id"]
log.debug("using database: %s", database_id)

# ──────────────────────────────────────────────
# 2. Retrieve and update a database
# ──────────────────────────────────────────────
log.debug("=== 2. Retrieve & update database ===")
db = client.databases.retrieve(database_id)
pprint.pprint(db)

client.databases.update(
    database_id,
    title=[RichText.text("Updated DB")],
    icon=Icon.emoji("📚"),
    cover=Cover.external("https://github.githubassets.com/images/modules/logos_page/Octocat.png"),
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

existing = set(db["properties"].keys())
missing = {k: v for k, v in REQUIRED_PROPERTIES.items() if k not in existing}

if missing:
    log.debug("adding missing columns: %s", list(missing.keys()))
    client.databases.update(database_id, properties=missing)
else:
    log.debug("all required columns already exist")

# ──────────────────────────────────────────────
# 4. Create a page (all PropertyValue types + all BlockContent types)
# ──────────────────────────────────────────────
log.debug("=== 4. Create page ===")
page = client.pages.create(
    parent={"database_id": database_id},
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
# 4. Retrieve the page
# ──────────────────────────────────────────────
log.debug("=== 5. Retrieve page ===")
page = client.pages.retrieve(page_id)
pprint.pprint(page)

# ──────────────────────────────────────────────
# 5. Update the page
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
# 6. Retrieve block children
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

# Append a new block
client.blocks.append_children(page_id, children=[
    BlockContent.paragraph("This block was appended after the page was created."),
])

# ──────────────────────────────────────────────
# 7. Query the database (filters + sorts)
# ──────────────────────────────────────────────
log.debug("=== 8. Query database ===")

# Simple filter
result = client.databases.query(
    database_id,
    filter=Filter.checkbox("checkbox").equals(False),
    sorts=[Sort.by_property("title")],
)
pprint.pprint(result)

# OR compound filter
result = client.databases.query(
    database_id,
    filter=Filter.or_([
        Filter.checkbox("checkbox").equals(False),
        Filter.number("number").greater_than_or_equal_to(2),
    ]),
)
pprint.pprint(result)

# Nested AND + OR filter
result = client.databases.query(
    database_id,
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
all_pages = client.databases.query_all(database_id)
log.debug("total pages: %d", len(all_pages))

# ──────────────────────────────────────────────
# 8. Archive and restore the page
# ──────────────────────────────────────────────
log.debug("=== 9. Archive & restore page ===")
time.sleep(1)
client.pages.archive(page_id)
log.debug("page archived")

time.sleep(1)
client.pages.archive(page_id, archived=False)
log.debug("page restored")

# ──────────────────────────────────────────────
# 9. Create a child database
# ──────────────────────────────────────────────
log.debug("=== 10. Create child database ===")
child_db = client.databases.create(
    parent={"type": "page_id", "page_id": page_id},
    title=[RichText.text("Child Database")],
    properties={
        "Name":        PropertySchema.title(),
        "Description": PropertySchema.rich_text(),
        "Score":       PropertySchema.number(),
        "Category":    PropertySchema.select([
                           {"name": "Option A", "color": "green"},
                           {"name": "Option B", "color": "red"},
                       ]),
        "Tags":        PropertySchema.multi_select(),
        "Active":      PropertySchema.checkbox(),
        "Website":     PropertySchema.url(),
        "Email":       PropertySchema.email(),
        "Phone":       PropertySchema.phone_number(),
        "Due":         PropertySchema.date(),
    },
    icon=Icon.external("https://github.githubassets.com/images/modules/logos_page/Octocat.png"),
    cover=Cover.external("https://github.githubassets.com/images/modules/logos_page/Octocat.png"),
)
log.debug("child database: %s", child_db["id"])

# ──────────────────────────────────────────────
# 10. Users
# ──────────────────────────────────────────────
log.debug("=== 11. Users ===")
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
