# support : "title", "rich_text", "number", "select", "multi_select", "checkbox", "url", "email", "phone_number"

class Properties:
    def __init__(self):
        self.title = {"title": [{"text": {"content": ""}}]}
        self.rich_text = {"rich_text": [{"text": {"content": ""}}]}
        self.number = {"number": 0}
        self.select = {"select": {"name": ""}}
        self.multi_select = {"multi_select": [{"name": ""}]}
        self.checkbox = {"checkbox": False}
        self.url = {"url": ""}
        self.email = {"email": ""}
        self.phone_number = {"phone_number": ""}

    def set_title(self, text):
        self.title["title"][0]["text"]["content"] = text
        return self.title

    def set_rich_text(self, text):
        self.rich_text["rich_text"][0]["text"]["content"] = text
        return self.rich_text

    def set_number(self, text):
        self.number["number"] = text
        return self.number

    def set_select(self, text):
        self.select["select"]["name"] = text
        return self.select

    def set_multi_select(self, text_list):
        data = [{"name": i} for i in text_list]
        self.multi_select["multi_select"] = data
        return self.multi_select

    def set_checkbox(self, text=False):
        self.checkbox["checkbox"] = text
        return self.checkbox

    def set_url(self, text):
        self.url["url"] = text
        return self.url

    def set_email(self, text):
        self.email["email"] = text
        return self.email

    def set_phone_number(self, text):
        self.phone_number["phone_number"] = text
        return self.phone_number


class Children:
    def __init__(self):
        self.text = ""
        self.body = {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "text": [
                    {
                        "type": "text",
                        "text": {
                            "content": self.text,
                        }
                    }
                ]
            }
        }

    def set_body(self, text):
        self.body["paragraph"]["text"][0]["text"]["content"] = text
        return self.body
