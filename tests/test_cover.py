import unittest

from notion_database.service.cover import Cover


class TestCoverMethods(unittest.TestCase):

    def test_cover(self):
        cover_object = Cover()
        cover_object.set_cover_image(text="https://github.githubassets.com/images/modules/logos_page/Octocat.png")
        api_value = {
            'cover': {
                'external': {
                    'url': 'https://github.githubassets.com/images/modules/logos_page/Octocat.png'},
                'type': 'external'
            }
        }
        self.assertEqual(cover_object.result, api_value)


if __name__ == '__main__':
    unittest.main()
