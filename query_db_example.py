import logging
import os
import pprint

from notion_database.const.query import Direction, Timestamp
from notion_database.database import Database
from notion_database.search import Search

try:
    from dotenv import load_dotenv

    load_dotenv()
except ModuleNotFoundError:
    pass

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

NOTION_KEY = os.getenv('NOTION_KEY')

logger.debug("List Database")
S = Search(integrations_token=NOTION_KEY)
S.search_database(query="", sort={"direction": Direction.ascending, "timestamp": Timestamp.last_edited_time})

for i in S.result:
    database_id = i["id"]
    logger.debug(database_id)
    database = Database(integrations_token=NOTION_KEY)
    database.run_query_database(database_id=database_id,
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
    pprint.pprint(database.result)