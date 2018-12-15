import unittest
import json
import pprint

# liftree import
from liftree_test import LIFTREE_PATH_TEST
from utils import format_search_results_for_sui
from liftree import LifTree

class TestSearch(unittest.TestCase):

    def test_search(self):
        liftree = LifTree()
        results = liftree.search('test/data/test')
        # pprint.pprint(results)
        with open(f'{LIFTREE_PATH_TEST}/references/search_test_raw.json', 'r') as file:
            expected_results = json.load(file)
        self.assertEqual(results, expected_results)

        formatted_results = format_search_results_for_sui(results['files'])
        with open(f'{LIFTREE_PATH_TEST}/references/search_test_sui.json', 'r') as file:
            expected_results = json.load(file)
        self.assertEqual(formatted_results, expected_results)

if __name__ == '__main__':
    unittest.main()
