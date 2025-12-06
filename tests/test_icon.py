import unittest

from notion_database.service.icon import Icon


class TestIconMethods(unittest.TestCase):

    def test_icon_image(self):
        icon_object = Icon()
        icon_object.set_icon_image(text="https://github.githubassets.com/images/modules/logos_page/Octocat.png")
        api_value = {
            'icon': {
                'external': {
                    'url': 'https://github.githubassets.com/images/modules/logos_page/Octocat.png'},
                'type': 'external'
            }
        }
        self.assertEqual(icon_object.result, api_value)

    def test_icon_emoji(self):
        icon_object = Icon()
        icon_object.set_icon_emoji(text="📚")
        api_value = {
            'icon': {
                'emoji': "📚",
                'type': 'emoji'
            }
        }
        self.assertEqual(icon_object.result, api_value)


if __name__ == '__main__':
    unittest.main()
