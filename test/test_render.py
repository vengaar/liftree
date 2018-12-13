import unittest
import yaml
import json
from bs4 import BeautifulSoup

# liftree import
import sys
sys.path.append('../bin')
from liftree import LifTree
from constants import HTTP_200, CONTENT_TYPE_HTML

class TestRender(unittest.TestCase):

    test_file_json = '/home/liftree/liftree/example/data/test.json'
    test_file_secret = '/home/liftree/liftree/example/data/test.secret'

    def test_is_valid(self):
        liftree = LifTree()

        # Valid file
        folder = liftree._is_valid_path(self.test_file_json)
        self.assertEqual(folder['name'], 'liftree')

        # Valid file event forbidden in mapping
        folder = liftree._is_valid_path(self.test_file_secret)
        self.assertEqual(folder['name'], 'liftree')

        # File not in folder
        folder = liftree._is_valid_path('/etc/passwd')
        self.assertIsNone(folder)

        # File in folder but in excludes list
        folder = liftree._is_valid_path('/home/liftree/liftree/.git/config')
        self.assertIsNone(folder)

    def test_get_renderer(self):
        liftree = LifTree()

        # Json file
        renderer = liftree._get_renderer(self.test_file_json)
        self.assertEqual(renderer.name, 'json')

        # File forbidden in mapping
        renderer = liftree._get_renderer(self.test_file_secret)
        self.assertEqual(renderer.name, 'forbidden')

        # Files not valid but matching pattern
        # Security concern of _is_valid_path not _get_renderer
        for path in ('/etc/passwd', '/home/liftree/liftree/.git/config'):
            renderer = liftree._get_renderer('/etc/passwd')
            self.assertEqual(renderer.name, 'raw')

    def test_render(self):
        liftree = LifTree()
        status, content_type, output = liftree.render(self.test_file_json)
        self.assertEqual(status, HTTP_200)
        self.assertEqual(content_type, CONTENT_TYPE_HTML)
        soup = BeautifulSoup(output, 'html.parser')
        code = soup.find(id='liftree_data')
        text = code.get_text()
        data = yaml.load(text)
        with open(self.test_file_json, 'r') as file:
            expected_data = json.load(file)
            self.assertEqual(data, expected_data)

if __name__ == '__main__':
    unittest.main()
