import unittest
import logging
import pprint
import sys

# liftree import
from liftree_test import LIFTREE_PATH_TEST, LIFTREE_PATH_ROOT
from liftree import LifTreeConfig
# from constants import HTTP_200, CONTENT_TYPE_HTML

class TestRender(unittest.TestCase):

    def test_import_path(self):
        expeced_path = [
            f'{LIFTREE_PATH_ROOT}/apps/example',
            f'{LIFTREE_PATH_ROOT}/apps/ansible',
        ]
        liftreec_config = LifTreeConfig()
        # pprint.pprint(expeced_path)
        # pprint.pprint(liftreec_config.import_path)
        # pprint.pprint(sys.path)
        # pprint.pprint(sys.path[-1:])
        self.assertEqual(liftreec_config.import_path, expeced_path)
        self.assertEqual(sys.path[-2:], liftreec_config.import_path)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    unittest.main()
