Python Notion Database
======================

https://github.com/minwook-shin/notion-database

   Notion API Database Python Implementation

created only by database from the official Notion API.


Installing / Getting started
----------------------------

.. code:: shell

   pip install notion-database

List Database
~~~~~~~~~~~~~

.. code:: python

    S = Search(integrations_token=NOTION_KEY)
    S.search_database(query="",
                      sort={"direction": Direction.ascending,
                            "timestamp": Timestamp.last_edited_time})

Retrieve Database
~~~~~~~~~~~~~~~~~

.. code:: python

   from notion_database.database import Database

   D = Database(integrations_token=NOTION_KEY)
   D.retrieve_database(database_id=database_id)

Properties
~~~~~~~~~~

-  For Database

.. code:: python

   from notion_database.properties import Properties

   PROPERTY = Properties()
   PROPERTY.set_title("title")
   PROPERTY.set_rich_text("description")
   PROPERTY.set_number("number")
   PROPERTY.set_select("select")
   PROPERTY.set_multi_select("multi_select")
   PROPERTY.set_checkbox("checkbox")
   PROPERTY.set_url("url")
   PROPERTY.set_email("email")
   PROPERTY.set_phone_number("phone")
   PROPERTY.set_date("date")
   PROPERTY.set_files("file")

-  For Page

.. code:: python

   from notion_database.properties import Properties

   PROPERTY = Properties()
   PROPERTY.set_title("title", "title")
   PROPERTY.set_rich_text("description", "notion-database")
   PROPERTY.set_number("number", 1)
   PROPERTY.set_select("select", "test1")
   PROPERTY.set_multi_select("multi_select", ["test1", "test2"])
   PROPERTY.set_checkbox("checkbox", True)
   PROPERTY.set_url("url", "www.google.com")
   PROPERTY.set_email("email", "test@test.com")
   PROPERTY.set_phone_number("phone", "010-0000-0000")
   PROPERTY.set_date("date", "2022-12-31T01:01:01.000+0900", "2023-01-10T01:01:01.000+0900")
   PROPERTY.set_files("file", files_list=["https://github.githubassets.com/images/modules/logos_page/Octocat.png"])

Create Page
~~~~~~~~~~~

.. code:: python

   from notion_database.page import Page

   P = Page(integrations_token=NOTION_KEY)
   P.create_page(database_id=database_id, properties=PROPERTY, children=children)
   page_id = P.result["id"]

Retrieve Page
~~~~~~~~~~~~~

.. code:: python

   from notion_database.page import Page

   P = Page(integrations_token=NOTION_KEY)
   P.retrieve_page(page_id=page_id)

Update Page
~~~~~~~~~~~

.. code:: python

   from notion_database.page import Page

   P = Page(integrations_token=NOTION_KEY)
   P.update_page(page_id=page_id, properties=PROPERTY)

Clear Properties
~~~~~~~~~~~~~~~~

.. code:: python

   from notion_database.properties import Properties

   PROPERTY = Properties()
   PROPERTY.clear()

Archive Page
~~~~~~~~~~~~

.. code:: python

   from notion_database.page import Page

   P = Page(integrations_token=NOTION_KEY)
   P.archive_page(page_id=page_id, archived=True)

Create database
~~~~~~~~~~~~~~~

.. code:: python

   from notion_database.database import Database

   D = Database(integrations_token=NOTION_KEY)
   D.create_database(page_id=page_id, title="TEST TITLE", properties=PROPERTY)

Finding all pages in a database
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

   from notion_database.database import Database
   import pprint

   D = Database(integrations_token=NOTION_KEY)
   D.find_all_page(database_id=database_id)
   pprint.pprint(D.result)

   if D.result["has_more"]:
      D.find_all_page(database_id=database_id, start_cursor=D.result["next_cursor"])

Get Properties
~~~~~~~~~~~~~~

.. code:: python

   from notion_database.database import Database

   D = Database(integrations_token=NOTION_KEY)
   D.retrieve_database(database_id, get_properties=True)
   properties_list = D.properties_list

Remove Properties / Update Database
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

   from notion_database.database import Database

   D = Database(integrations_token=NOTION_KEY)
   D.update_database(database_id=database_id, title="DB", add_properties=PROPERTY)

or

.. code:: python

   from notion_database.database import Database

   D = Database(integrations_token=NOTION_KEY)
   D.update_database(database_id=database_id, title="DB", remove_properties=D.properties_list)

or

.. code:: python

   from notion_database.database import Database

   D = Database(integrations_token=NOTION_KEY)
   D.update_database(database_id=database_id, title="DB", remove_properties=D.properties_list, add_properties=PROPERTY)

Children block
~~~~~~~~~~~~~~

.. code:: python

   from notion_database.children import Children
   children = Children()

   children.set_paragraph("set_paragraph")
   children.set_paragraph("set_paragraph", color=clr.BLUE)

   children.set_heading_1("set_heading_1")
   children.set_heading_2("set_heading_2")
   children.set_heading_3("set_heading_3")
   children.set_heading_1("set_heading_1", color=clr.BLUE)
   children.set_heading_2("set_heading_2", color=clr.BLUE_BACKGROUND)
   children.set_heading_3("set_heading_3", color=clr.GREEN)

   children.set_callout("set_callout")
   children.set_callout("set_callout",color=clr.RED_BACKGROUND)

   children.set_quote("set_quote")
   children.set_quote("set_quote",color=clr.RED)

   children.set_bulleted_list_item("set_bulleted_list_item")
   children.set_bulleted_list_item("set_bulleted_list_item", color=clr.BROWN)

   children.set_numbered_list_item("first set_numbered_list_item")
   children.set_numbered_list_item("second set_numbered_list_item", color=clr.BROWN)

   children.set_to_do("set_to_do", checked=True)
   children.set_to_do("set_to_do", checked=False, color=clr.RED)

   children.set_toggle("set_toggle", children_text="WOW!", color=clr.BLUE)

   children.set_code("set_code")
   children.set_code("const a = 1", lang="javascript")
   children.set_code("print(\"hello world!\")", lang='python')

   children.set_embed("https://www.google.com")

   children.set_external_image("https://github.githubassets.com/images/modules/logos_page/Octocat.png")
   children.set_external_video("http://download.blender.org/peach/trailer/trailer_480p.mov")
   children.set_external_file("https://github.com/microsoft/ML-For-Beginners/raw/main/pdf/readme.pdf")
   children.set_external_pdf("https://github.com/microsoft/ML-For-Beginners/blob/main/pdf/readme.pdf")

   children.set_bookmark("https://www.google.com")

   children.set_equation("e=mc^2")

   children.set_divider()
   children.set_table_of_contents()
   children.set_breadcrumb()

   # P.create_page(database_id=database_id, properties=PROPERTY, children=children)

Building / Developing
---------------------

.. code:: shell

   python setup.py install

Contributing
------------

If you’d like to contribute, please fork the repository and use a
feature branch. Pull requests are warmly welcome.

Links
-----

-  Notion API : https://developers.notion.com

Licensing
---------

The code in this project is licensed under GPL license.
