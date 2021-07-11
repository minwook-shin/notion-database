# support : "title", "rich_text", "number", "select", "multi_select", "checkbox", "url", "email", "phone_number"

class Properties:
    def __init__(self):
        self.result = {}

    def set_title(self, col, text):
        self.result.update({col: {"title": [{"text": {"content": text}}]}})

    def set_rich_text(self, col, text):
        self.result.update({col: {"rich_text": [{"text": {"content": text}}]}})

    def set_number(self, col, text):
        self.result.update({col: {"number": text}})

    def set_select(self, col, text):
        self.result.update({col: {"select": {"name": text}}})

    def set_multi_select(self, col, text_list):
        data = [{"name": i} for i in text_list]
        self.result.update({col: {"multi_select": data}})

    def set_checkbox(self, col, text=False):
        self.result.update({col: {"checkbox": text}})

    def set_url(self, col, text):
        self.result.update({col: {"url": text}})

    def set_email(self, col, text):
        self.result.update({col: {"email": text}})

    def set_phone_number(self, col, text):
        self.result.update({col: {"phone_number": text}})

    def clear(self):
        self.result.clear()


class Children:
    def __init__(self):
        self.result = []

    def set_body(self, text):
        self.result = [{
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "text": [
                    {
                        "type": "text",
                        "text": {
                            "content": text,
                        }
                    }
                ]
            }
        }]
