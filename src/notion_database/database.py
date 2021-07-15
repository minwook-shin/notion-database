from notion_database.properties import Properties
from notion_database.request import Request


class Database:
    def __init__(self, integrations_token):
        self.url = 'https://api.notion.com/v1/databases'
        self.result = {}
        self.request = Request(self.url, integrations_token=integrations_token)

    def retrieve_database(self, database_id):
        self.result = self.request.call_api_get(self.url + "/" + database_id)

    def query_database(self):
        # Not Implemented
        pass

    def run_query_database(self, database_id, body=None):
        """
        for developer
        :param database_id:
        :param body:
        :return:
        """
        if body is None:
            body = {}
        self.result = self.request.call_api_post(self.url + "/" + database_id + "/query", body)

    def find_all_page(self, database_id):
        body = {
            "sorts": []
        }
        self.result = self.request.call_api_post(self.url + "/" + database_id + "/query", body)

    def list_databases(self, page_size=100):
        url = self.url + f"?page_size={str(page_size)}"
        self.result = self.request.call_api_get(url)

    def create_database(self, page_id, title, properties=None):
        if properties is None:
            properties = Properties()
        properties = properties
        body = {
            "parent": {
                "type": "page_id",
                "page_id": page_id
            },
            "title": [
                {
                    "type": "text",
                    "text": {
                        "content": title,
                        "link": None
                    }
                }
            ],
            "properties": properties.result
        }
        self.result = self.request.call_api_post(self.url, body)
