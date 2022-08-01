import logging
import os
import pprint
import time

from notion_database.children import Children
from notion_database.database import Database
from notion_database.page import Page
from notion_database.properties import Properties
from notion_database.query import Direction, Timestamp
from notion_database.search import Search

try:
    from dotenv import load_dotenv

    load_dotenv()
except ModuleNotFoundError:
    pass

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

NOTION_KEY = os.getenv('NOTION_KEY')

# List Database
logger.debug("List Database")
S = Search(integrations_token=NOTION_KEY)
S.search_database(query="", sort={"direction": Direction.ascending, "timestamp": Timestamp.last_edited_time})

# List Database API is deprecated.
# D = Database(integrations_token=NOTION_KEY)
# D.list_databases(page_size=100)

for i in S.result:
    database_id = i["id"]
    logger.debug(database_id)

    PROPERTY = Properties()
    PROPERTY.set_title("name")
    PROPERTY.set_rich_text("description")
    PROPERTY.set_number("number")
    PROPERTY.set_select("select")
    PROPERTY.set_multi_select("multi_select")
    PROPERTY.set_multi_select("multi_select2")
    PROPERTY.set_checkbox("checkbox")
    PROPERTY.set_url("url")
    PROPERTY.set_email("email")
    PROPERTY.set_phone_number("phone")

    # Get Properties and Remove/Update Database
    logger.debug("Get properties")
    D = Database(integrations_token=NOTION_KEY)
    D.retrieve_database(database_id, get_properties=True)
    logger.debug("Remove/Update Database")
    D.update_database(database_id=database_id, title="DB", add_properties=PROPERTY)

    # Retrieve Database
    logger.debug("Retrieve Database")
    D = Database(integrations_token=NOTION_KEY)
    D.retrieve_database(database_id=database_id)

    PROPERTY = Properties()
    PROPERTY.set_title("title", "title")
    PROPERTY.set_title("name", "notion-api")
    PROPERTY.set_rich_text("description", "notion-database")
    PROPERTY.set_number("number", 1)
    PROPERTY.set_select("select", "test1")
    PROPERTY.set_multi_select("multi_select", ["test1", "test2"])
    PROPERTY.set_multi_select("multi_select2", ["test1", "test2", "test3"])
    PROPERTY.set_checkbox("checkbox", True)
    PROPERTY.set_url("url", "www.google.com")
    PROPERTY.set_email("email", "test@test.com")
    PROPERTY.set_phone_number("phone", "010-0000-0000")

    # Children block
    logger.debug("Set Children block")
    children = Children()
    # children.set_body("hello world!")  # deprecated. set_body -> set_paragraph
    children.set_paragraph("set_paragraph")

    children.set_heading_1("set_heading_1")
    children.set_heading_2("set_heading_2")
    children.set_heading_3("set_heading_3")

    children.set_callout("set_callout")

    children.set_quote("set_quote")

    children.set_bulleted_list_item("set_bulleted_list_item")

    children.set_numbered_list_item("first set_numbered_list_item")
    children.set_numbered_list_item("second set_numbered_list_item")

    children.set_to_do("set_to_do", checked=True)
    children.set_to_do("set_to_do", checked=False)

    children.set_toggle("set_toggle", children_text="WOW!")

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

    # Create Page
    logger.debug("Create Page")
    P = Page(integrations_token=NOTION_KEY)
    P.create_page(database_id=database_id, properties=PROPERTY, children=children)

    # Retrieve Page
    logger.debug("Retrieve Page")
    page_id = P.result["id"]
    logger.debug(page_id)
    P.retrieve_page(page_id=page_id)

    PROPERTY.clear()
    PROPERTY.set_title("name", "Custom_name")
    PROPERTY.set_rich_text("description", "Custom_description")
    PROPERTY.set_number("number", 2)

    # Update Page
    logger.debug("Update Page")
    P.update_page(page_id=page_id, properties=PROPERTY)

    time.sleep(1)
    # Archive Page
    logger.debug("Archive Database")
    P.archive_page(page_id=page_id, archived=True)

    time.sleep(1)
    # Un-Archive Page
    logger.debug("Un-Archive Database")
    P.archive_page(page_id=page_id, archived=False)

    # Create Database
    logger.debug("Create Database")

    PROPERTY = Properties()
    PROPERTY.set_title("child_name")
    PROPERTY.set_rich_text("child_description")
    PROPERTY.set_number("child_number")
    PROPERTY.set_select("child_select")
    PROPERTY.set_multi_select("child_multi_select")
    PROPERTY.set_multi_select("child_multi_select2")
    PROPERTY.set_checkbox("child_checkbox")
    PROPERTY.set_url("child_url")
    PROPERTY.set_email("child_email")
    PROPERTY.set_phone_number("child_phone")
    D.create_database(page_id=page_id, title="TEST TITLE", properties=PROPERTY)

    # Finding all pages in a database
    D.find_all_page(database_id=database_id, page_size=1)
    pprint.pprint(D.result)
    # Pagination test
    logger.debug("Pagination test")
    if D.result["has_more"]:
        D.find_all_page(database_id=database_id, start_cursor=D.result["next_cursor"])
        pprint.pprint(D.result)
    # D.run_query_database(database_id=database_id, body={})
