import unittest, pprint
import json

# liftree import
import sys
sys.path.append('.')
import liftree
from liftree import LifTree
import tests as liftree_tests
from liftree.utils import format_search_results_for_sui


class TestSearch(unittest.TestCase):

    def test_search(self):
        # print(dir(liftree))
        # print(liftree_tests.LIFTREE_PATH_TEST)
        _liftree = LifTree()
        expected_results = {
            'files': {
                'forbidden': [
                    f'{liftree_tests.LIFTREE_PATH_TEST}/data/test.secret'
                ],
                'json': [
                    f'{liftree_tests.LIFTREE_PATH_TEST}/data/test.json'
                ],
                'markdown': [
                    f'{liftree_tests.LIFTREE_PATH_TEST}/data/test.md'
                ],
                'plugins': [
                    f'{liftree_tests.LIFTREE_PATH_TEST}/data/test.plugins'
                ],
                'text': [
                    f'{liftree_tests.LIFTREE_PATH_TEST}/data/test.text'
                ],
                'yaml': [
                    f'{liftree_tests.LIFTREE_PATH_TEST}/data/test.yaml'
                ]
            }
        }
        # pprint.pprint(expected_results)
        results = _liftree.search('tests/data/test')
        # pprint.pprint(results)
        self.assertEqual(results, expected_results)

        # Test SUI format
        expected_results = {
            'forbidden': {
                'name': 'forbidden',
                'results': [
                    {
                        'title': f'{liftree_tests.LIFTREE_PATH_TEST}/data/test.secret',
                        'url': f'/show?path={liftree_tests.LIFTREE_PATH_TEST}/data/test.secret'
                    }
                ]
            },
            'json': {
                'name': 'json',
                'results': [
                    {
                        'title': f'{liftree_tests.LIFTREE_PATH_TEST}/data/test.json',
                        'url': f'/show?path={liftree_tests.LIFTREE_PATH_TEST}/data/test.json'
                    }
                ]
            },
            'markdown': {
                'name': 'markdown',
                'results': [
                    {
                        'title': f'{liftree_tests.LIFTREE_PATH_TEST}/data/test.md',
                        'url': f'/show?path={liftree_tests.LIFTREE_PATH_TEST}/data/test.md'
                    }
                ]
            },
            'plugins': {
                'name': 'plugins',
                'results': [
                    {
                        'title': '/home/vengaar/liftree/tests/data/test.plugins',
                        'url': '/show?path=/home/vengaar/liftree/tests/data/test.plugins'
                    }
                ]
            },
            'text': {
                'name': 'text',
                'results': [
                    {
                        'title': f'{liftree_tests.LIFTREE_PATH_TEST}/data/test.text',
                        'url': f'/show?path={liftree_tests.LIFTREE_PATH_TEST}/data/test.text'
                    }
                ]
            },
            'yaml': {
                'name': 'yaml',
                'results': [
                    {
                        'title': f'{liftree_tests.LIFTREE_PATH_TEST}/data/test.yaml',
                        'url': f'/show?path={liftree_tests.LIFTREE_PATH_TEST}/data/test.yaml'
                    }
                ]
            }
        }
#         pprint.pprint(expected_results)
        formatted_results = format_search_results_for_sui(results['files'])
#         pprint.pprint(formatted_results)
        self.assertEqual(formatted_results, expected_results)


if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.INFO)
    unittest.main()
