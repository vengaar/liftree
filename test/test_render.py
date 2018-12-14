import unittest
import yaml
import json
from bs4 import BeautifulSoup
import logging

# liftree import
from liftree_test import LIFTREE_PATH_DATA, LIFTREE_PATH_ROOT
from liftree import LifTree
from constants import HTTP_200, CONTENT_TYPE_HTML

class TestRender(unittest.TestCase):

    test_file_json = f'{LIFTREE_PATH_DATA}/test.json'
    test_file_secret = f'{LIFTREE_PATH_DATA}/test.secret'
    test_file_out = '/etc/passwd'
    test_file_exclude = f'{LIFTREE_PATH_ROOT}/.git/config'
    test_file_none = '/tmp/flgkgkiejjk/158468764'

    def test_extra(self):
        extra_def = {
            'files': {
                'secret': self.test_file_secret
            },
            'scripts': {
                'test': f'{LIFTREE_PATH_ROOT}/example/scripts/get_test.py'
            }
        }
        extra = LifTree()._get_extra(self.test_file_json, extra_def)
        self.assertEqual(extra['test'], 'I love Liftree')
        self.assertEqual(extra['secret'], 'The secret file')

    def test_is_valid(self):
        liftree = LifTree()

        # Valid file
        folder = liftree._is_valid_path(self.test_file_json)
        self.assertEqual(folder['name'], 'liftree')

        # Valid file event forbidden in mapping
        folder = liftree._is_valid_path(self.test_file_secret)
        self.assertEqual(folder['name'], 'liftree')

        # File not in folder
        folder = liftree._is_valid_path(self.test_file_out)
        self.assertIsNone(folder)

        # File in folder but in excludes list
        folder = liftree._is_valid_path(self.test_file_exclude)
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
        for path in (self.test_file_out, self.test_file_exclude):
            renderer = liftree._get_renderer(path)
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

        # print(liftree.render('/home/liftree/liftree/setup/playbooks/setup.yml'))

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    unittest.main()
