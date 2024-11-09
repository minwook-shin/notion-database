"""
Notion API Properties
"""
import numbers
from datetime import datetime
from typing import Dict, List

from notion_database.utils import deprecate


class Properties:  # pylint: disable=too-many-public-methods
    """
    Notion API Properties class
    """

    def __init__(self):
        """
        init
        """
        self.result: Dict = {}

    def set_title(self, col: str, text=None):
        """
        title configuration

        :param col: column name
        :param text: page text. If no text is given, for database only.
        :return:
        """
        if (text is not None) and isinstance(text, str):
            text = [{"text": {"content": text}}]
        else:
            text = {}
        self.result.update({col: {"title": text}})

    def set_rich_text(self, col: str, text=None):
        """
        rich_text configuration

        :param col: column name
        :param text: page text. If no text is given, for database only.
        :return:
        """
        if (text is not None) and isinstance(text, str):
            text = [{"text": {"content": text}}]
        else:
            text = {}
        self.result.update({col: {"rich_text": text}})

    def set_number(self, col: str, text=None):
        """
        number configuration

        :param col: column name
        :param text: page text. If no text is given, for database only.
        :return:
        """
        if (text is not None) and isinstance(text, numbers.Number):
            number = text
        else:
            number = {}
        self.result.update({col: {"number": number}})

    def set_select(self, col: str, text=None):
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

    def set_multi_select(self, col: str, text_list: List[str] = None):
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

    def set_checkbox(self, col: str, text: bool = None):
        """
        checkbox configuration

        :param col: column name
        :param text: page text. If no text is given, for database only.
        :return:
        """
        if text is None:
            # unset the checkbox
            text = {}
        self.result.update({col: {"checkbox": text}})

    def set_url(self, col: str, text=None):
        """
        url configuration

        :param col: column name
        :param text: page text. If no text is given, for database only.
        :return:
        """
        if not text:
            text = {}
        self.result.update({col: {"url": text}})

    def set_email(self, col: str, text=None):
        """
        email configuration

        :param col: column name
        :param text: page text. If no text is given, for database only.
        :return:
        """
        if not text:
            text = {}
        self.result.update({col: {"email": text}})

    def set_phone_number(self, col: str, text=None):
        """
        phone_number configuration

        :param col: column name
        :param text: page text. If no text is given, for database only.
        :return:
        """
        if not text:
            text = {}
        self.result.update({col: {"phone_number": text}})

    def set_date(self, col: str, start: str = None, end: str = None):
        """
        date configuration

        :param col: column name
        :param start: ISO 8601 format date, with optional time.
        :param end: ISO 8601 formatted date, with optional time. Represents the end of a date range.
        :return:
        """
        if (not start) and (not end):
            self.result.update({col: {"date": {}}})
        elif not start:
            start = datetime.now().isoformat()
            self.result.update({col: {"date": {"start": start}}})
        elif not end:
            self.result.update({col: {"date": {"start": start}}})
        else:
            self.result.update({col: {"date": {"start": start, "end": end}}})

    def set_files(self, col: str, files_list: List[str] = None):
        """
        files configuration. Only supports external links.

        :param col: column name
        :param files_list: page files url list. If no files is given, for database only.
        :return:
        """
        if files_list:
            data = []
            for i in files_list:
                data.append({"type": "external", "name": i.split("/")[-1], "external": {"url": i}})
        else:
            data = {}

        self.result.update({col: {"files": data}})

    def clear(self):
        """
        Clear result

        :return:
        """
        self.result.clear()


class Children:  # pylint: disable=too-few-public-methods
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
