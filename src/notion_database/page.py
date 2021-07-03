from notion_database.request import Request


class Page:
    def __init__(self, integrations_token, database_id):
        self.url = 'https://api.notion.com/v1/pages'
        self.result = {}
        self.database_id = database_id
        self.request = Request(self.url, integrations_token=integrations_token)

    def retrieve_page(self, page_id):
        self.result = self.request.call_api_get(self.url + "/" + page_id)

    def create_page(self, properties=None, children=None):
        if children is None:
            children = {}
        if properties is None:
            properties = {}
        properties = properties
        children = children
        body = {
            "parent": {
                "database_id": self.database_id
            },
            "properties": properties,
            "children": children
        }
        self.result = self.request.call_api_post(self.url, body)

    def update_page(self, page_id, properties):
        body = {
            "properties": properties,
        }
        self.result = self.request.call_api_patch(self.url + "/" + page_id, body)
