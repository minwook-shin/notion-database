import logging
import os
import pprint

from notion_database import NotionDatabase
from notion_database.const.query import Direction, Timestamp

try:
    from dotenv import load_dotenv

    load_dotenv()
except ModuleNotFoundError:
    pass

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

NOTION_KEY = os.getenv('NOTION_KEY')

logger.debug("List Database")
result = NotionDatabase.search(integrations_token=NOTION_KEY,
                               sort={"direction": Direction.ascending, "timestamp": Timestamp.last_edited_time})

for i in result:
    database_id = i["id"]
    logger.debug(database_id)
    database = NotionDatabase.run_query_database(
        database_id=database_id,
        integrations_token=NOTION_KEY,
        db_filter={
            "or": [
                {
                    "property": "checkbox",
                    "checkbox": {
                        "equals": False
                    }
                },
                {
                    "property": "number",
                    "number": {
                        "greater_than_or_equal_to": 2
                    }
                }
            ]
        })
    pprint.pprint(database)

    search_pages = NotionDatabase.search_pages(integrations_token=NOTION_KEY,
                                               sort={"direction": Direction.ascending,
                                                     "timestamp": Timestamp.last_edited_time},
                                               query="Custom_description")
    pprint.pprint(search_pages)
