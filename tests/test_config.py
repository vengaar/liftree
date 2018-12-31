import unittest, pprint
import sys,os

# liftree import
import sys
sys.path.append('.')
import liftree
import tests as liftree_tests

class TestRender(unittest.TestCase):

    def test_import_path(self):
        expeced_path = f'{liftree_tests.LIFTREE_PATH_ROOT}/apps/example'
        liftree_config = liftree.core.LifTreeConfig()
        # pprint.pprint(expeced_path)
        # pprint.pprint(liftreec_config.import_path)
        # pprint.pprint(sys.path)
        self.assertIn(expeced_path, liftree_config.import_path)
        self.assertIn(expeced_path, sys.path)

if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.INFO)
    unittest.main()
