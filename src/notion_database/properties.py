# support : "title", "rich_text", "number", "select", "multi_select", "checkbox", "url", "email", "phone_number"
from utils import deprecate


class Properties:
    def __init__(self):
        """
        init
        """
        self.result = {}

    def set_title(self, col, text=None):
        """
        title configuration

        :param col: column name
        :param text: page text. If no text is given, for database only.
        :return:
        """
        if text:
            text = [{"text": {"content": text}}]
        else:
            text = {}
        self.result.update({col: {"title": text}})

    def set_rich_text(self, col, text=None):
        """
        rich_text configuration

        :param col: column name
        :param text: page text. If no text is given, for database only.
        :return:
        """
        if text:
            text = [{"text": {"content": text}}]
        else:
            text = {}
        self.result.update({col: {"rich_text": text}})

    def set_number(self, col, text=None):
        """
        number configuration

        :param col: column name
        :param text: page text. If no text is given, for database only.
        :return:
        """
        if text:
            text = int(text)
        else:
            text = {}
        self.result.update({col: {"number": text}})

    def set_select(self, col, text=None):
        """
        select configuration

        :param col: column name
        :param text: page text. If no text is given, for database only.
        :return:
        """
        if text:
            text = {"name": text}
        else:
            text = {}
        self.result.update({col: {"select": text}})

    def set_multi_select(self, col, text_list=None):
        """
        multi select configuration

        :param col: column name
        :param text_list: page text list. If no text is given, for database only.
        :return:
        """
        if text_list:
            data = []
            for i in text_list:
                data.append({"name": i})
        else:
            data = {}

        self.result.update({col: {"multi_select": data}})

    def set_checkbox(self, col, text=None):
        """
        checkbox configuration

        :param col: column name
        :param text: page text. If no text is given, for database only.
        :return:
        """
        if not text:
            text = {}
        self.result.update({col: {"checkbox": text}})

    def set_url(self, col, text=None):
        """
        url configuration

        :param col: column name
        :param text: page text. If no text is given, for database only.
        :return:
        """
        if not text:
            text = {}
        self.result.update({col: {"url": text}})

    def set_email(self, col, text=None):
        """
        email configuration

        :param col: column name
        :param text: page text. If no text is given, for database only.
        :return:
        """
        if not text:
            text = {}
        self.result.update({col: {"email": text}})

    def set_phone_number(self, col, text=None):
        """
        phone_number configuration

        :param col: column name
        :param text: page text. If no text is given, for database only.
        :return:
        """
        if not text:
            text = {}
        self.result.update({col: {"phone_number": text}})

    def clear(self):
        """
        Clear result

        :return:
        """
        self.result.clear()


class Children:
    """
    deprecated class
    """

    def __init__(self):
        """
        init
        """
        self.result = []

    @deprecate.deprecated_warn
    def set_body(self, text):
        """
        (deprecated) Children configuration

        move to set_paragraph function
        """
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
