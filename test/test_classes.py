import logging
import unittest
import pprint

# liftree import
import liftree_test
from classes import LifTreeFolder, LifTreeLoader, Renderer

class TestLiftreeClasses(unittest.TestCase):

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

    def test_liftree_loader(self):

        loader_desc = {
            'name': 'file_extract_loader',
            'params': {
                'prefix': '### DOC ###',
                'format': 'yaml'
            }
        }
        loader = LifTreeLoader(**loader_desc)
        data = loader.get_data('/home/liftree/liftree/setup/playbooks/setup.yml')
        self.assertEqual(data['author'], 'olivier perriot')
        self.assertEqual(data['state'], 'dev')

    def test_liftree_folder(self):

        liftree_folder = LifTreeFolder(name='name', path='path', extra=self.extra)
        # print(liftree_folder)
        self.assertEqual(liftree_folder.name, 'name')
        self.assertEqual(liftree_folder.path, 'path')
        self.assertEqual(liftree_folder.excludes, [])
        self.assertEqual(liftree_folder.extra_loaders, dict())
        self.assertEqual(liftree_folder.extra_files['test'], 'test')
        self.assertEqual(liftree_folder.name, 'name')

        liftree_folder2 = LifTreeFolder(**self.data_dict)
        # print(liftree_folder)
        self.assertEqual(liftree_folder._get_data(), liftree_folder2._get_data())

        excludes=['pattern1', 'pattern2']
        liftree_folder = LifTreeFolder(**self.data_dict, excludes=excludes)
        # print(liftree_folder)
        self.assertEqual(liftree_folder.excludes, excludes)

    def test_renderer(self):
        renderer = Renderer(name='name', template='template', extra=self.extra)
        # print(renderer)
        self.assertEqual(renderer.name, 'name')
        self.assertEqual(renderer.template, 'template')
        self.assertEqual(renderer.extra_files['test'], 'test')
        self.assertEqual(renderer.extra_loaders, dict())

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    unittest.main()
