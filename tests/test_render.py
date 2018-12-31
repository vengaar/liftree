import unittest, pprint
import yaml, json
import os
from bs4 import BeautifulSoup

# liftree import
import sys
sys.path.append('.')
import liftree
from liftree import LifTree
import tests as liftree_tests
from liftree.utils import format_search_results_for_sui

class TestRender(unittest.TestCase):

    test_file_json = f'{liftree_tests.LIFTREE_PATH_TEST}/data/test.json'
    # Not existing file => unavailable
    test_file_none = '/tmp/flgkgkiejjk/158468764'
    # Out of folders  => unavailable
    test_file_out = '/etc/passwd'
    # Excluded from folder => unavailable
    test_file_exclude = f'{liftree_tests.LIFTREE_PATH_ROOT}/search_test_raw.json'
    # Marked as forbidden in mapping  => unavailable
    test_file_forbidden = f'{liftree_tests.LIFTREE_PATH_TEST}/data/test.secret'

    def test_is_valid(self):
        # Valid file
        _liftree = LifTree()
        folder = _liftree._is_valid_path(self.test_file_json)
        self.assertEqual(folder.name, 'liftree unittest files')

        # Valid file but forbidden in mapping
        folder = _liftree._is_valid_path(self.test_file_forbidden)
        self.assertEqual(folder.name, 'liftree unittest files')

        for path in [
            self.test_file_out,
            self.test_file_exclude
        ]:
            folder = _liftree._is_valid_path(path)
            self.assertIsNone(folder)

    def test_get_renderer(self):
        _liftree = LifTree()

        # Json file
        renderer = _liftree._get_renderer(self.test_file_json)
        self.assertEqual(renderer.name, 'json')

        # File forbidden in mapping
        renderer = _liftree._get_renderer(self.test_file_forbidden)
        self.assertEqual(renderer.name, 'forbidden')

        # Files not valid but matching pattern
        # Security is concern of _is_valid_path not _get_renderer
        renderer = _liftree._get_renderer(self.test_file_out)
        self.assertEqual(renderer.name, 'raw')
        renderer = _liftree._get_renderer(self.test_file_exclude)
        self.assertEqual(renderer.name, 'json')

    def test_build_extra(self):
        _liftree = LifTree()
        folder = _liftree._is_valid_path(self.test_file_json)
        renderer = _liftree._get_renderer(self.test_file_json)
        extra_sources = _liftree._build_extra(renderer, folder)
        # pprint.pprint(extra_sources)
        self.assertIsInstance(extra_sources['loaders'], dict)
        self.assertIsInstance(extra_sources['files'], dict)
        self.assertEqual(extra_sources['loaders']['test']['name'], 'get_test_folder')

        test_file = self.test_file_none
        folder = _liftree._is_valid_path(test_file)
        renderer = _liftree._get_renderer(test_file)
        extra_sources = _liftree._build_extra(renderer, folder)
        self.assertIsInstance(extra_sources['loaders'], dict)
        self.assertIsInstance(extra_sources['files'], dict)

    def test_extra(self):
        _liftree = LifTree()
        test_file = self.test_file_json
        folder = _liftree._is_valid_path(test_file)
        renderer = _liftree._get_renderer(test_file)
        extra_sources = _liftree._build_extra(renderer, folder)
        extra = LifTree()._get_extra(extra_sources, test_file)
        self.assertEqual(extra['test'], 'I love Liftree')

        renderer._add_extra_loader('test', dict(name='get_test_page'))
        renderer._add_extra_file('secret', self.test_file_forbidden)
        extra_sources = _liftree._build_extra(renderer, folder)
        extra = LifTree()._get_extra(extra_sources, self.test_file_json)
        self.assertEqual(extra['test'], 'I love this page')
        self.assertEqual(extra['secret'], 'The secret file')

    def test_render(self):
        _liftree = LifTree()
        status, content_type, output = _liftree.render(self.test_file_json)
        self.assertEqual(status, liftree.HTTP_200)
        self.assertEqual(content_type, liftree.CONTENT_TYPE_HTML)
        soup = BeautifulSoup(output, 'html.parser')
        # print(soup.prettify())
        code = soup.find(id='liftree_data')
        text = code.get_text()
        data = yaml.load(text)
        with open(self.test_file_json, 'r') as file:
            expected_data = json.load(file)
            self.assertEqual(data, expected_data)

        # print(liftree.render('/home/liftree/liftree/setup/playbooks/setup.yml'))

if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.INFO)
    unittest.main()
