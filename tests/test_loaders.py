import unittest, pprint
import os

# liftree import
import sys
sys.path.append('.')
import liftree
import liftree.loaders.get_git_info
import tests as liftree_tests

class TestLiftreeLoaders(unittest.TestCase):

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
