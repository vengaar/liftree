import unittest, pprint
import os
from bs4 import BeautifulSoup

# liftree import
import sys
sys.path.append('.')
import liftree
import liftree.loaders.get_git_info
import liftree.loaders.file_json_loader
import liftree.loaders.file_yaml_loader
import liftree.loaders.file_markdown_loader
import tests as liftree_tests

class TestLiftreeLoaders(unittest.TestCase):

    def test_json(self):
        path =f'{liftree_tests.LIFTREE_PATH_TEST}/data/test.json'
        params = dict()
        data = liftree.loaders.file_json_loader.get_data(path, params)
#         pprint.pprint(data)
        self.assertEqual(data['markers'][1]['name'], 'Shangri-La Hotel')

    def test_yaml(self):
        path =f'{liftree_tests.LIFTREE_PATH_TEST}/data/test.yaml'
        params = dict()
        data = liftree.loaders.file_yaml_loader.get_data(path, params)
#         pprint.pprint(data)
        self.assertEqual(data['items'][1]['part_no'], 'E1628')

    def test_markdown(self):
        path =f'{liftree_tests.LIFTREE_PATH_TEST}/data/test.md'
        params = dict()
        data = liftree.loaders.file_markdown_loader.get_data(path, params)
#         pprint.pprint(data)
        soup = BeautifulSoup(data, 'html.parser')
#         print(soup.prettify())
        h1 = soup.h1.string
#         print(h1)
        self.assertEqual(h1, 'Markdown: Syntax')

    def test_git(self):
        path =f'{liftree_tests.LIFTREE_PATH_TEST}/data/test.secret'
#         print(path)
        os.system(f'git checkout {path}')
        params = dict(
            repo = liftree_tests.LIFTREE_PATH_ROOT
        )
        data = liftree.loaders.get_git_info.get_data(path, params)
#         pprint.pprint(data)
        self.assertEqual(data['status'], 'Unknown')
        self.assertFalse(data['untracked'])
        with open(path, 'a') as fst:
            fst.write("new text fot unittest")
        data = liftree.loaders.get_git_info.get_data(path, params)
#         pprint.pprint(data)
        self.assertEqual(data['status'], 'M')
        self.assertFalse(data['untracked'])
        os.system(f'git checkout {path}')

        path =f'{liftree_tests.LIFTREE_PATH_TEST}/data/test.unittest'
        print(path)
        with open(path, "w") as fst:
            fst.write("new text fot unittest")
        data = liftree.loaders.get_git_info.get_data(path, params)
#         pprint.pprint(data)
        self.assertEqual(data['status'], 'Unknown')
        self.assertTrue(data['untracked'])
        os.remove(path)

if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.INFO)
    unittest.main()
