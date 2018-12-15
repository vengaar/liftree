import logging
import unittest
import pprint

# liftree import
import liftree_test
from liftree_object import LifTreeFolder

class TestFolder(unittest.TestCase):

    def test(self):

        extra = dict(
            files=dict(
                test='test'
            )
        )

        data_dict = dict(
            name='name',
            path='path',
            extra=extra,
        )

        liftree_folder = LifTreeFolder(name='name', path='path', extra=extra)
        # print(liftree_folder)
        self.assertEqual(liftree_folder.name, 'name')
        self.assertEqual(liftree_folder.path, 'path')
        self.assertEqual(liftree_folder.excludes, [])
        self.assertEqual(liftree_folder.extra_loaders, dict())
        self.assertEqual(liftree_folder.extra_files['test'], 'test')
        self.assertEqual(liftree_folder.name, 'name')

        liftree_folder2 = LifTreeFolder(data_dict)
        # print(liftree_folder)
        self.assertEqual(liftree_folder._get_data(), liftree_folder2._get_data())

        excludes=['pattern1', 'pattern2']
        liftree_folder = LifTreeFolder(data_dict, excludes=excludes)
        # print(liftree_folder)
        self.assertEqual(liftree_folder.excludes, excludes)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    unittest.main()
