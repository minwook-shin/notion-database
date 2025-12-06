"""
Notion API Cover
"""
from typing import Dict


class Cover:
    """
    Notion API Cover class
    """
    def __init__(self):
        """
        init
        """
        self.result: Dict = {}

    def set_cover_image(self, text: str = None):
        """
        Page cover image
        only type of "external" is supported currently

        :param text: image URL.
        :return:
        """
        if not text:
            text = ""

        self.result = {
            "cover": {
                "type": "external",
                "external": {
                    "url": text
                }
            },
        }

    def clear(self):
        """
        Clear result

        :return:
        """
        self.result.clear()
