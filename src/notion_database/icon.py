class Icon:
    def __init__(self):
        """
        init
        """
        self.result = {}

    def set_icon_emoji(self, text=None):
        """
        Page icon emoji.
        emoji character is supported

        :param text: icon emoji.
        :return:
        """
        if not text:
            text = ""

        self.result = {
            "icon": {
                "type": "emoji",
                "emoji": text
            },
        }

    def set_icon_image(self, text=None):
        """
        Page icon image.
        type of "external" is supported

        :param text: icon URL.
        :return:
        """
        if not text:
            text = ""

        self.result = {
            "icon": {
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
