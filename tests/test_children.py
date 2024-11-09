import unittest

from notion_database.service.children import Children


class TestChildrenMethods(unittest.TestCase):
    def setUp(self):
        self.default_test_text = {
            'rich_text':
                [
                    {
                        'type': 'text', 'text': {'content': 'test'}
                    }
                ],
            'color': 'default'
        }

    def tearDown(self):
        del self.default_test_text

    def test_paragraph(self):
        children_object = Children()
        children_object.set_paragraph(text="test")
        api_value = [
            {
                'object': 'block',
                'type': 'paragraph',
                'paragraph': self.default_test_text
            }
        ]
        self.assertEqual(children_object.result, api_value)

    def test_heading_1(self):
        children_object = Children()
        children_object.set_heading_1(text="test")
        api_value = [
            {
                'object': 'block',
                'type': 'heading_1',
                'heading_1': self.default_test_text
            }
        ]
        self.assertEqual(children_object.result, api_value)

    def test_heading_2(self):
        children_object = Children()
        children_object.set_heading_2(text="test")
        api_value = [
            {
                'object': 'block',
                'type': 'heading_2',
                'heading_2': self.default_test_text
            }
        ]
        self.assertEqual(children_object.result, api_value)

    def test_heading_3(self):
        children_object = Children()
        children_object.set_heading_3(text="test")
        api_value = [
            {
                'object': 'block',
                'type': 'heading_3',
                'heading_3': self.default_test_text
            }
        ]
        self.assertEqual(children_object.result, api_value)

    def test_callout(self):
        children_object = Children()
        children_object.set_callout(text="test")
        api_value = [
            {
                'object': 'block',
                'type': 'callout',
                'callout': self.default_test_text
            }
        ]
        self.assertEqual(children_object.result, api_value)

    def test_quote(self):
        children_object = Children()
        children_object.set_quote(text="test")
        api_value = [
            {
                'object': 'block',
                'type': 'quote',
                'quote': self.default_test_text
            }
        ]
        self.assertEqual(children_object.result, api_value)

    def test_bulleted_list_item(self):
        children_object = Children()
        children_object.set_bulleted_list_item(text="test")
        api_value = [
            {
                'object': 'block',
                'type': 'bulleted_list_item',
                'bulleted_list_item': self.default_test_text
            }
        ]
        self.assertEqual(children_object.result, api_value)

    def test_numbered_list_item(self):
        children_object = Children()
        children_object.set_numbered_list_item(text="test")
        api_value = [
            {
                'object': 'block',
                'type': 'numbered_list_item',
                'numbered_list_item': self.default_test_text
            }
        ]
        self.assertEqual(children_object.result, api_value)

    def test_to_do(self):
        children_object = Children()
        children_object.set_to_do(text="test")
        todo_test_text = self.default_test_text
        todo_test_text["checked"] = False
        api_value = [
            {
                'object': 'block',
                'type': 'to_do',
                'to_do': todo_test_text
            }
        ]
        self.assertEqual(children_object.result, api_value)

    def test_toggle(self):
        children_object = Children()
        children_object.set_toggle(text="test", children_text="test2")
        toggle_test_text = self.default_test_text
        toggle_test_text["children"] = [{
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "color": 'default',
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": 'test2'
                        }
                    }
                ]
            }
        }]
        api_value = [
            {
                'object': 'block',
                'type': 'toggle',
                'toggle': toggle_test_text
            }
        ]
        self.assertEqual(children_object.result, api_value)

    def test_code(self):
        children_object = Children()
        children_object.set_code(code="test", lang="python")
        code_test_text = self.default_test_text
        code_test_text["language"] = "python"
        del code_test_text["color"]
        api_value = [
            {
                'object': 'block',
                'type': 'code',
                'code': code_test_text
            }
        ]
        self.assertEqual(children_object.result, api_value)

    def test_embed(self):
        children_object = Children()
        children_object.set_embed(url="www.google.com")
        api_value = [
            {
                'object': 'block',
                'type': 'embed',
                'embed': {
                    "url": "www.google.com"
                }
            }
        ]
        self.assertEqual(children_object.result, api_value)

    def test_image(self):
        children_object = Children()
        children_object.set_external_image(url="www.google.com/img.gif")
        api_value = [
            {
                'object': 'block',
                'type': 'image',
                'image': {
                    "type": "external",
                    "external": {
                        "url": "www.google.com/img.gif"
                    }
                }
            }
        ]
        self.assertEqual(children_object.result, api_value)

    def test_video(self):
        children_object = Children()
        children_object.set_external_video(url="www.google.com/vod.avi")
        api_value = [
            {
                'object': 'block',
                'type': 'video',
                'video': {
                    "type": "external",
                    "external": {
                        "url": "www.google.com/vod.avi"
                    }
                }
            }
        ]
        self.assertEqual(children_object.result, api_value)

    def test_file(self):
        children_object = Children()
        children_object.set_external_file(url="www.google.com/file.pdf")
        api_value = [
            {
                'object': 'block',
                'type': 'file',
                'file': {
                    "type": "external",
                    "external": {
                        "url": "www.google.com/file.pdf"
                    }
                }
            }
        ]
        self.assertEqual(children_object.result, api_value)

    def test_pdf(self):
        children_object = Children()
        children_object.set_external_pdf(url="www.google.com/file.pdf")
        api_value = [
            {
                'object': 'block',
                'type': 'pdf',
                'pdf': {
                    "type": "external",
                    "external": {
                        "url": "www.google.com/file.pdf"
                    }
                }
            }
        ]
        self.assertEqual(children_object.result, api_value)

    def test_bookmark(self):
        children_object = Children()
        children_object.set_bookmark(url="www.google.com")
        api_value = [
            {
                'object': 'block',
                'type': 'bookmark',
                'bookmark': {
                    "url": "www.google.com"
                }
            }
        ]
        self.assertEqual(children_object.result, api_value)

    def test_equation(self):
        children_object = Children()
        children_object.set_equation(exp="e=mc^2")
        api_value = [
            {
                'object': 'block',
                'type': 'equation',
                'equation': {
                    "expression": "e=mc^2"
                }
            }
        ]
        self.assertEqual(children_object.result, api_value)


if __name__ == '__main__':
    unittest.main()
