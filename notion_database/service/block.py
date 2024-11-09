"""
Notion API Block
"""
from typing import Dict, List

from notion_database.components.request import Request


class Block:  # pylint: disable=too-few-public-methods
    """
    Notion API Block class
    """

    def __init__(self, integrations_token: str):
        """
        init

        :param integrations_token: Notion Internal Integration Token
        """
        self.properties_list: List[Dict] = []
        self.url: str = 'https://api.notion.com/v1/blocks'
        self.result: Dict = {}
        self.request: Request = Request(self.url, integrations_token=integrations_token)

    def retrieve_block(self, block_id: str, is_children: bool = False,
                       page_size: int = 100, start_cursor: str = None):
        """
        Retrieve a block

        :param block_id: Identifier for a Notion blocks
        :param is_children: Trigger's paginated array of child block objects
        :param start_cursor: optional parameter for is_children=True
        :param page_size: optional parameter for is_children=True
        :return:
        """
        if is_children:
            param = f"children?page_size={page_size}&start_cursor={start_cursor}"
            if start_cursor is None:
                param = param.split("&")[0]
            self.result = self.request.call_api_get(self.url + "/" + block_id
                                                    + "/" + param)
        else:
            self.result = self.request.call_api_get(self.url + "/" + block_id)
