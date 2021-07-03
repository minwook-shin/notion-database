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

    def list_databases(self, page_size=100):
        url = self.url + f"?page_size={str(page_size)}"
        self.result = self.request.call_api_get(url)
