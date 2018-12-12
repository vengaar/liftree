import unittest

# liftree import
import sys
sys.path.append('../bin')
from liftree import LifTree

class TestSearch(unittest.TestCase):

    def test_search(self):
        liftree = LifTree()
        parameters = dict(path=['/home/liftree/liftree/example/data/test.yaml'])
        parameters = dict(path=['/home/liftree/liftree/example/data/test.md'])
        parameters = dict(path=['/home/liftree/liftree/example/data/test.text'])
        parameters = dict(path=['/home/liftree/liftree/example/data/test.json'])
        status, content_type, output = liftree.render(parameters)
        print(status, content_type, output)

if __name__ == '__main__':
    unittest.main()
