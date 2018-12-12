import unittest
import json

# liftree import
import sys
sys.path.append('../bin')
from utils import format_search_results_for_sui
from liftree import LifTree

class TestSearch(unittest.TestCase):

    def test_search(self):
        liftree = LifTree()
        results = liftree.search('example/data/test')
        with open('references/search_test_raw.json', 'r') as file:
            expected_results = json.load(file)
        self.assertEqual(results, expected_results)

        formatted_results = format_search_results_for_sui(results['files'])
        with open('references/search_test_sui.json', 'r') as file:
            expected_results = json.load(file)
        self.assertEqual(formatted_results, expected_results)

if __name__ == '__main__':
    unittest.main()
