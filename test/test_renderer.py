import logging
import unittest
import pprint

# liftree import
import liftree_test
from liftree_object import Renderer

class TestRenderer(unittest.TestCase):

    extra = dict(
        files=dict(
            test='test'
        )
    )

    def test(self):
        pass
        # renderer = Renderer(name='name', template='teplate', extra=extra)
        # print(renderer)
        # self.assertEqual(liftree_folder.name, 'name')
        # self.assertEqual(liftree_folder.path, 'path')
        # self.assertEqual(liftree_folder.excludes, [])
        # self.assertEqual(liftree_folder.extra['loaders'], dict())
        # self.assertEqual(liftree_folder.extra['files']['test'], 'test')
        # self.assertEqual(liftree_folder.name, 'name')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    unittest.main()
