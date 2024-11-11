import os
import pprint

from notion_database import NotionDatabase
from notion_database.service.block import Block
from notion_database.const.query import Direction, Timestamp

try:
    from dotenv import load_dotenv

    load_dotenv()
except ModuleNotFoundError:
    pass

NOTION_KEY = os.getenv('NOTION_KEY')
result = NotionDatabase.search(integrations_token=NOTION_KEY,
                               sort={"direction": Direction.ascending, "timestamp": Timestamp.last_edited_time})


for i in result:
    database_id = i["id"]
    db = NotionDatabase.retrieve_database(integrations_token=NOTION_KEY, database_id=database_id, get_properties=True)
    pprint.pprint(db)
    db = NotionDatabase.find_all_page(integrations_token=NOTION_KEY, database_id=database_id, page_size=1)
    pprint.pprint(db)

    B = Block(integrations_token=NOTION_KEY)
    for j in db["results"]:
        B.retrieve_block(block_id=j["id"])
        pprint.pprint(B.result)
        # B.retrieve_block(block_id=j["id"], is_children=True)
        # pprint.pprint(B.result)
        B.retrieve_block(block_id=j["id"], is_children=True, page_size=1)
        pprint.pprint(B.result)
        # B.retrieve_block(block_id=j["id"],is_children=True, page_size=1, start_cursor=B.result["next_cursor"])
        # pprint.pprint(B.result)
