import json
import os

import requests

from src.notion_database import NOTION_VERSION


class Request:
    def __init__(self, url, integrations_token, database_id):
        self.NOTION_DATABASE_ID = database_id
        self.NOTION_KEY = integrations_token
        self.NOTION_VERSION = NOTION_VERSION
        self.HEADER = {"Authorization": f"Bearer {self.NOTION_KEY}",
                       "Content-Type": "application/json",
                       "Notion-Version": self.NOTION_VERSION}
        self.url = url

    def call_api_post(self, body):
        r = requests.post(self.url, data=json.dumps(body), headers=self.HEADER).json()
        return r

    def call_api_get(self, url):
        r = requests.get(url, headers=self.HEADER).json()
        return r

    def call_api_patch(self, body):
        r = requests.patch(self.url, data=json.dumps(body), headers=self.HEADER).json()
        return r
