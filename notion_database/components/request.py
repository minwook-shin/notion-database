"""
Requests wrapper
"""
import json
from typing import Dict

import requests

from notion_database import NOTION_VERSION


class Request:
    """
    Requests wrapper class
    """

    def __init__(self, url: str, integrations_token: str):
        """
        init

        :param url: Notion API URL
        :param integrations_token: Notion Internal Integration Token
        """
        self.notion_key: str = integrations_token
        self.notion_version: str = NOTION_VERSION
        self.header: Dict = {"Authorization": f"Bearer {self.notion_key}",
                             "Content-Type": "application/json",
                             "Notion-Version": self.notion_version}
        self.url: str = url

    def call_api_post(self, url: str, body: Dict) -> Dict:
        """
        request post

        :param url:
        :param body:
        :return:
        """
        response = requests.post(url, data=json.dumps(body), headers=self.header, timeout=60)
        response.raise_for_status()
        return response.json()

    def call_api_get(self, url: str) -> Dict:
        """
        request get

        :param url:
        :return:
        """
        response = requests.get(url, headers=self.header, timeout=60)
        response.raise_for_status()
        return response.json()

    def call_api_patch(self, url: str, body: Dict) -> Dict:
        """
        request patch

        :param url:
        :param body:
        :return:
        """
        response = requests.patch(url, data=json.dumps(body), headers=self.header, timeout=60)
        response.raise_for_status()
        return response.json()
