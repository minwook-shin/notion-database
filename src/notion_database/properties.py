# support : "title", "rich_text", "number", "select", "multi_select", "checkbox", "url", "email", "phone_number"

class Properties:
    def __init__(self):
        self.result = {}

    def set_title(self, col, text=None):
        if text:
            text = [{"text": {"content": text}}]
        else:
            text = {}
        self.result.update({col: {"title": text}})

    def set_rich_text(self, col, text=None):
        if text:
            text = [{"text": {"content": text}}]
        else:
            text = {}
        self.result.update({col: {"rich_text": text}})

    def set_number(self, col, text=None):
        if text:
            text = int(text)
        else:
            text = {}
        self.result.update({col: {"number": text}})

    def set_select(self, col, text=None):
        if text:
            text = {"name": text}
        else:
            text = {}
        self.result.update({col: {"select": text}})

    def set_multi_select(self, col, text_list=None):
        if text_list:
            data = []
            for i in text_list:
                data.append({"name": i})
        else:
            data = {}

        self.result.update({col: {"multi_select": data}})

    def set_checkbox(self, col, text=None):
        if not text:
            text = {}
        self.result.update({col: {"checkbox": text}})

    def set_url(self, col, text=None):
        if not text:
            text = {}
        self.result.update({col: {"url": text}})

    def set_email(self, col, text=None):
        if not text:
            text = {}
        self.result.update({col: {"email": text}})

    def set_phone_number(self, col, text=None):
        if not text:
            text = {}
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
