import json

import requests

from notion_database import NOTION_VERSION


class Request:
    def __init__(self, url, integrations_token):
        self.NOTION_KEY = integrations_token
        self.NOTION_VERSION = NOTION_VERSION
        self.HEADER = {"Authorization": f"Bearer {self.NOTION_KEY}",
                       "Content-Type": "application/json",
                       "Notion-Version": self.NOTION_VERSION}
        self.url = url

    def call_api_post(self, url, body):
        r = requests.post(url, data=json.dumps(body), headers=self.HEADER).json()
        return r

    def call_api_get(self, url):
        r = requests.get(url, headers=self.HEADER).json()
        return r

    def call_api_patch(self, url, body):
        r = requests.patch(url, data=json.dumps(body), headers=self.HEADER).json()
        return r
