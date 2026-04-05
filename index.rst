notion-database
===============

`GitHub <https://github.com/minwook-shin/notion-database>`_ |
`PyPI <https://pypi.org/project/notion-database/>`_ |
`Issue Tracker <https://github.com/minwook-shin/notion-database/issues>`_

A Python client for the Notion API.
Start with a single ``NotionClient`` and use the builder classes to compose requests.

Installation
------------

.. code:: shell

   pip install notion-database

Getting Started
---------------

Create a Notion Internal Integration and copy the token.

.. code:: shell

   export NOTION_KEY=secret_xxx

.. code:: python

   from notion_database import NotionClient

   client = NotionClient("secret_xxx")

All resources are accessed through ``client.databases``, ``client.pages``,
``client.blocks``, ``client.search``, ``client.users``, and ``client.comments``.

----

Databases
---------

Search Databases
~~~~~~~~~~~~~~~~

.. code:: python

   result = client.search.search_databases(
       sort={"direction": "ascending", "timestamp": "last_edited_time"},
   )
   for db in result["results"]:
       print(db["id"])

Retrieve a Database
~~~~~~~~~~~~~~~~~~~

.. code:: python

   db = client.databases.retrieve("database-id")

Create a Database
~~~~~~~~~~~~~~~~~

.. code:: python

   from notion_database import NotionClient, PropertySchema, RichText, Icon

   client = NotionClient("secret_xxx")

   db = client.databases.create(
       parent={"type": "page_id", "page_id": "page-id"},
       title=[RichText.text("My Database")],
       properties={
           "Name":   PropertySchema.title(),
           "Status": PropertySchema.select([
                         {"name": "In Progress", "color": "blue"},
                         {"name": "Done",        "color": "green"},
                     ]),
           "Score":  PropertySchema.number("number"),
           "Due":    PropertySchema.date(),
           "Done":   PropertySchema.checkbox(),
       },
       icon=Icon.emoji("📋"),
   )

Update a Database
~~~~~~~~~~~~~~~~~

.. code:: python

   from notion_database import RichText, Icon

   client.databases.update(
       "database-id",
       title=[RichText.text("Renamed Database")],
       icon=Icon.emoji("🗂️"),
   )

----

Pages
-----

Create a Page
~~~~~~~~~~~~~

The keys in ``properties`` must match the column names in the parent database.

.. code:: python

   from notion_database import NotionClient, PropertyValue, BlockContent, Icon, Cover

   client = NotionClient("secret_xxx")

   page = client.pages.create(
       parent={"database_id": "database-id"},
       properties={
           "Name":   PropertyValue.title("New Page"),
           "Status": PropertyValue.select("In Progress"),
           "Score":  PropertyValue.number(100),
           "Due":    PropertyValue.date("2024-12-31"),
           "Done":   PropertyValue.checkbox(False),
       },
       icon=Icon.emoji("🚀"),
       cover=Cover.external("https://example.com/cover.jpg"),
       children=[
           BlockContent.heading_1("Introduction"),
           BlockContent.paragraph("This page was created with notion-database 2.0."),
       ],
   )
   page_id = page["id"]

Retrieve a Page
~~~~~~~~~~~~~~~

.. code:: python

   page = client.pages.retrieve("page-id")

Update a Page
~~~~~~~~~~~~~

.. code:: python

   from notion_database import PropertyValue

   client.pages.update(
       "page-id",
       properties={
           "Status": PropertyValue.select("Done"),
           "Done":   PropertyValue.checkbox(True),
       },
   )

Archive / Restore a Page
~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

   client.pages.archive("page-id")                     # archive
   client.pages.archive("page-id", archived=False)     # restore

----

Property Values
---------------

Use ``PropertyValue`` to build property values when creating or updating pages.

.. code:: python

   from notion_database import PropertyValue

   {
       "Name":        PropertyValue.title("Page title"),
       "Description": PropertyValue.rich_text("Some text"),
       "Count":       PropertyValue.number(42),
       "Category":    PropertyValue.select("Option A"),
       "Tags":        PropertyValue.multi_select(["tag1", "tag2"]),
       "Status":      PropertyValue.status("In Progress"),
       "Date":        PropertyValue.date("2024-01-01"),
       "DateRange":   PropertyValue.date("2024-01-01", end="2024-01-31"),
       "Active":      PropertyValue.checkbox(True),
       "Website":     PropertyValue.url("https://example.com"),
       "Email":       PropertyValue.email("hello@example.com"),
       "Phone":       PropertyValue.phone_number("+1-555-0100"),
       "Attachment":  PropertyValue.files(["https://example.com/file.pdf"]),
       "Related":     PropertyValue.relation(["other-page-id"]),
       "Owner":       PropertyValue.people(["user-id"]),
   }

Use ``PropertySchema`` to define database column schemas when creating or updating databases.

.. code:: python

   from notion_database import PropertySchema

   {
       "Name":     PropertySchema.title(),
       "Notes":    PropertySchema.rich_text(),
       "Score":    PropertySchema.number("number"),
       "Category": PropertySchema.select([{"name": "A"}, {"name": "B"}]),
       "Tags":     PropertySchema.multi_select(),
       "Due":      PropertySchema.date(),
       "Done":     PropertySchema.checkbox(),
       "Website":  PropertySchema.url(),
       "Formula":  PropertySchema.formula("prop('Score') * 2"),
       "Related":  PropertySchema.relation("other-database-id"),
   }

----

Block Content
-------------

Use ``BlockContent`` to build page content blocks.

.. code:: python

   from notion_database import NotionClient, BlockContent, RichText
   from notion_database.const import BLUE, RED_BACKGROUND

   client = NotionClient("secret_xxx")

   client.blocks.append_children("page-id", children=[
       BlockContent.heading_1("Heading 1"),
       BlockContent.heading_2("Heading 2"),
       BlockContent.heading_3("Heading 3"),

       BlockContent.paragraph("Plain paragraph"),
       BlockContent.paragraph("Colored paragraph", color=BLUE),
       BlockContent.paragraph([
           RichText.text("Bold", bold=True),
           RichText.text(", "),
           RichText.text("italic", italic=True),
           RichText.text(", "),
           RichText.text("link", link="https://example.com"),
       ]),

       BlockContent.callout("Note", color=RED_BACKGROUND),
       BlockContent.quote("A famous quote."),

       BlockContent.bulleted_list_item("Bullet item"),
       BlockContent.numbered_list_item("Numbered item"),
       BlockContent.to_do("Task", checked=False),
       BlockContent.toggle("Toggle header", children=[
           BlockContent.paragraph("Hidden content"),
       ]),

       BlockContent.code('print("hello")', language="python"),
       BlockContent.equation("E = mc^2"),

       BlockContent.image("https://example.com/image.png", caption="Figure 1"),
       BlockContent.video("https://example.com/video.mp4"),
       BlockContent.embed("https://www.youtube.com/watch?v=xxx"),
       BlockContent.bookmark("https://example.com"),

       BlockContent.divider(),
       BlockContent.table_of_contents(),

       BlockContent.column_list([
           [BlockContent.paragraph("Left column")],
           [BlockContent.paragraph("Right column")],
       ]),
   ])

Retrieve Block Children
~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

   # Single page of results
   response = client.blocks.retrieve_children("page-id")
   blocks = response["results"]

   # Fetch all children automatically (auto-pagination)
   all_blocks = client.blocks.retrieve_all_children("page-id")

----

Querying (Filters & Sorts)
--------------------------

Use ``Filter`` and ``Sort`` to query a database.

.. code:: python

   from notion_database import NotionClient, Filter, Sort

   client = NotionClient("secret_xxx")

   # Simple filter
   result = client.databases.query(
       "database-id",
       filter=Filter.select("Status").equals("In Progress"),
       sorts=[Sort.descending("Due")],
   )

   # OR compound filter
   result = client.databases.query(
       "database-id",
       filter=Filter.or_([
           Filter.checkbox("Done").equals(False),
           Filter.number("Score").greater_than(90),
       ]),
   )

   # Nested AND + OR filter
   result = client.databases.query(
       "database-id",
       filter=Filter.and_([
           Filter.text("Name").is_not_empty(),
           Filter.or_([
               Filter.select("Status").equals("In Progress"),
               Filter.date("Due").next_week(),
           ]),
       ]),
   )

   # Fetch all results with automatic pagination
   all_pages = client.databases.query_all("database-id")

Filter Conditions Reference
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

   Filter.text("col").equals("value")
   Filter.text("col").contains("value")
   Filter.text("col").starts_with("value")
   Filter.text("col").is_empty()
   Filter.text("col").is_not_empty()

   Filter.number("col").greater_than(0)
   Filter.number("col").less_than_or_equal_to(100)

   Filter.checkbox("col").equals(True)

   Filter.select("col").equals("Option")
   Filter.multi_select("col").contains("tag")

   Filter.date("col").before("2025-01-01")
   Filter.date("col").past_week()
   Filter.date("col").next_month()
   Filter.date("col").this_week()

   Filter.created_time().after("2024-01-01")
   Filter.last_edited_time().past_week()

   # Compound
   Filter.and_([...])
   Filter.or_([...])

----

Error Handling
--------------

.. code:: python

   from notion_database import (
       NotionClient,
       NotionNotFoundError,
       NotionRateLimitError,
       NotionAPIError,
   )
   import time

   client = NotionClient("secret_xxx")

   try:
       page = client.pages.retrieve("page-id")
   except NotionNotFoundError:
       print("Page not found.")
   except NotionRateLimitError:
       time.sleep(1)
       page = client.pages.retrieve("page-id")
   except NotionAPIError as e:
       print(f"[{e.status_code}] {e.code}: {e.message}")

----

Contributing
------------

Bug reports and feature requests are welcome via
`GitHub Issues <https://github.com/minwook-shin/notion-database/issues>`_.
To contribute code, fork the repository and open a Pull Request.

Links
-----

- Notion API: https://developers.notion.com
- GitHub: https://github.com/minwook-shin/notion-database
- PyPI: https://pypi.org/project/notion-database/

License
-------

LGPLv3
