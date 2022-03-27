from utils import deprecate

from notion_database.properties import Properties
from notion_database.request import Request


class Database:
    def __init__(self, integrations_token):
        """
        init

        :param integrations_token: Notion Internal Integration Token
        """
        self.properties_list = []
        self.url = 'https://api.notion.com/v1/databases'
        self.result = {}
        self.request = Request(self.url, integrations_token=integrations_token)

    def retrieve_database(self, database_id, get_properties=False):
        """
        Retrieve a database

        :param database_id: Identifier for a Notion database
        :param get_properties: Get properties_list trigger
        :return:
        """
        self.result = self.request.call_api_get(self.url + "/" + database_id)
        if get_properties:
            self.properties_list.clear()
            for property_value in self.result["properties"].values():
                if property_value["id"] == "title":
                    # property type of the title cannot be changed.
                    continue
                self.properties_list.append(property_value)

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

    @deprecate.deprecated_warn
    def list_databases(self, page_size=100):
        """
        List databases ('This API is deprecated.')

        :param page_size: The number of items from the full list desired in the response.
        :return:
        """
        url = self.url + f"?page_size={str(page_size)}"
        self.result = self.request.call_api_get(url)

    def create_database(self, page_id, title, properties=None):
        """
        Create a database

        :param page_id: Notion Page ID
        :param title: Title of database as it appears in Notion
        :param properties: Property schema of database
        :return:
        """
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

    def update_database(self, database_id, title=None, remove_properties=None, add_properties=None):
        """
        Update database

        :param database_id: Identifier for a Notion database
        :param title: Title of database as it appears in Notion
        :param remove_properties: Removal Property schema of database
        :param add_properties: Property schema of database
        :return:
        """
        if add_properties is None:
            add_properties = Properties()
        body = {
            "properties": {}
        }
        if title:
            body["title"] = [
                {
                    "type": "text",
                    "text": {
                        "content": title,
                        "link": None
                    }
                }
            ]
        if remove_properties:
            body["properties"].update({i["id"]: None for i in remove_properties})
            self.result = self.request.call_api_patch(self.url + "/" + database_id, body)
            body["properties"] = {}
        if add_properties:
            body["properties"].update(add_properties.result)
            self.result = self.request.call_api_patch(self.url + "/" + database_id, body)
            body["properties"] = {}
