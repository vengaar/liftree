from jinja2 import Environment, FileSystemLoader
import yaml
import re
import logging
import importlib
import inspect
import sys
import os
import grp
import stat
import glob
from typing import Dict  # , Tuple, Sequence
import pathlib

# liftree import
from .constants import *
from .loaders.file_yaml_loader import get_data as load_yaml_file
from .classes import LifTreeObject, LifTreeFolder, LifTreeLoader, LifTreeRenderer


class LifTreeConfig(LifTreeObject):

    root_config_dir = '/etc/liftree'
    root_config_file = os.path.join(root_config_dir, 'liftree.conf')
    generated_config_file = os.path.join(str(pathlib.Path.home()), 'generated_liftree.conf')
    root_include_dir = os.path.join(root_config_dir, 'conf.d')
    root_include_pattern = os.path.join(root_include_dir, '*.conf')

    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)
        generated_config_exist = os.path.isfile(self.generated_config_file)
        if generated_config_exist:
            self._init_from_file(self.generated_config_file)
        else:
            self._init_from_file(self.root_config_file)
        generate = False
        generate_config = self.defaults.get('generate_config')
        if generate_config == 'always':
            generate = True
        elif generate_config == 'once' and not generated_config_exist:
            generate = True
        self._logger.debug(f'generate_config={generate_config}')
        self._logger.debug(f'generated_config_exist={generated_config_exist}')
        self._logger.debug(f'generate={generate}')
        # liftree path for core loaders and filers
        self.import_path = [os.path.dirname(os.path.realpath(__file__))]
        if generate:
            self._init_from_file(self.root_config_file)
            for file in sorted(glob.glob(self.root_include_pattern)):
                # print(file)
                self._logger.info(f'include={file}')
                config_include = load_yaml_file(file, None)
                self._import_config(config_include)
#             self._write()

        for lib_path in self.import_path:
            if lib_path not in sys.path:
                sys.path.append(lib_path)

        self._logger.debug(f'folders={self.folders}')
        self._logger.debug(f'templates={self.templates}')
        self._logger.debug(f'mappings={self.mappings}')

    def get_renderer(self, name: str) -> LifTreeRenderer:
        renderer_data = self.renderers[name]
        return LifTreeRenderer(name=name, **renderer_data)

    def _init_from_file(self, file):
        config = load_yaml_file(self.root_config_file, None)
        self.renderers = config.get('renderers', dict())
        self.defaults = config.get('defaults', dict())
        self.folders = config.get('folders', [])
        self.templates = config.get('templates', [])
        self.mappings = config.get('mapping', [])

    def _write(self):
        with open(self.generated_config_file, 'w') as outfile:
            yaml.dump(
                self._get_data(),
                outfile,
                default_flow_style=False
            )
        os.chmod(self.generated_config_file, 0o666)
        os.chown(self.generated_config_file, -1, grp.getgrnam("users").gr_gid)

    def _import_config(self, config_include):
        self._logger.debug(config_include)
        config_folder = config_include['name']
        config_file = os.path.join(config_folder, 'liftree.conf')
        self.import_path.append(os.path.join(config_folder))
        self._logger.debug(config_file)
        config = load_yaml_file(config_file, None)
        renderers = config.get('renderers', dict())
        self.renderers.update(renderers)
        folders = config.get('folders', [])
        self.folders.extend(folders)
        mappings = config.get('mappings', [])
        self.mappings = mappings + self.mappings
        templates = os.path.join(config_folder, 'templates')
        self.templates.insert(0, templates)
        default = config.get('defaults', dict())
        self.defaults.update(default)


class LifTree:

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.liftree_config = LifTreeConfig()
        self.logger.debug(self.liftree_config)
        self.folders = [
            LifTreeFolder(**data)
            for data in self.liftree_config.folders
        ]

    def search(self, query: str) -> Dict:
        pattern = query.replace(' ', '.*')
        re_pattern = re.compile(f'.*{pattern}.*')
        result_files = []
        result_folders = []
        for folder in self.folders:
            if folder.name not in self.liftree_config.defaults.get('search_excludes', []):
                root_dir = folder.path
                result_folders.append(root_dir)
                for root, dirs, files in os.walk(root_dir):
                    fullpath_files = [
                        os.path.join(root, file)
                        for file in files
                    ]
                    selected_files = [
                        path
                        for path in fullpath_files
                        if re_pattern.match(path) is not None
                    ]
                    result_files.extend(selected_files)

                    fullpath_foders = [
                        os.path.join(root, folder)
                        for folder in dirs
                    ]
                    result_folders.extend(fullpath_foders)

            valids_files = dict()
            for file in result_files:
                folder = self._is_valid_path(file)
                if folder is not None:
                    renderer = self._get_renderer(file)
                    if renderer.name not in valids_files:
                        valids_files[renderer.name] = []
                    valids_files[renderer.name].append(file)
            results = dict(files=valids_files)
        return results

    def render(self, path: str, renderer_name: str=None):
        if path is None:
            path = os.path.expanduser(self.liftree_config.defaults['path'])
        folder = self._is_valid_path(path)
        if folder is None:
            renderer = self.liftree_config.get_renderer('forbidden')
        else:
            renderer = self._get_renderer(path)
            if renderer.name != 'forbidden' and renderer_name is not None:
                renderer = self.liftree_config.get_renderer(renderer_name)
        self.logger.debug(f'renderer={renderer}')
        if renderer.loader is not None:
            data = renderer.loader.get_data(path)
        else:
            data = None
        j2_env = Environment(
            loader=FileSystemLoader(self.liftree_config.templates),
            trim_blocks=True
        )
        plugins = self._extend_j2(j2_env)
        template = j2_env.get_template(renderer.template)
        stat = os.stat(path) if os.path.isfile(path) else None
        meta = dict(
            path=path,
            stat=stat,
            folder=folder._get_data() if folder is not None else None,
            renderer=renderer._get_data(),
            config=self.liftree_config._get_data(),
            plugins=plugins,
            self=id(self)
        )
        extra_sources = self._build_extra(renderer, folder)
        extra = self._get_extra(extra_sources, path)
        output = template.render(data=data, meta=meta, extra=extra, extra_sources=extra_sources)
        status = HTTP_200
        content_type = CONTENT_TYPE_HTML
        return(status, content_type, output.encode('utf-8'))

    def _extend_j2(self, j2_env):
        extends = {'filters': [], 'tests': []}
        import_dirs = self.liftree_config.import_path
        self.logger.debug(import_dirs)
        for import_dir in import_dirs:
            folder_path = os.path.join(import_dir, 'plugins')
            if os.path.isdir(folder_path):
                for file in os.listdir(folder_path):
                    result = re.search('^(?P<module_name>.*).py$', file)
                    if result is not None:
                        module_name = result.group('module_name')
                        module_extend = importlib.import_module(f'plugins.{module_name}')
                        for tuple_function in inspect.getmembers(module_extend, predicate=inspect.isfunction):
                            (name, function) = tuple_function

                            if name.startswith('filter_'):
                                filter = name[len('filter_'):]
                                extends['filters'].append(filter)
                                j2_env.filters[filter] = function
                            if name.startswith('test_'):
                                test = name[len('test_'):]
                                extends['tests'].append(test)
                                j2_env.tests[test] = function
        return extends

    def _build_extra(self, renderer: LifTreeRenderer, folder: LifTreeFolder) -> Dict:
        """
            Build precedence between extra
            renderer > folder
        """
        files = dict()
        loaders = dict()
        if folder is not None:
            files.update(folder.extra_files)
            loaders.update(folder.extra_loaders)
        files.update(renderer.extra_files)
        loaders.update(renderer.extra_loaders)
        extra_sources = dict(
            files=files,
            loaders=loaders
        )
        return extra_sources

    def _get_extra(self, extra_sources: Dict, path: str) -> Dict:
        data = dict()
        for key, file in extra_sources['files'].items():
            data[key] = load_yaml_file(file, None)
        self.logger.debug(extra_sources)
        for key, loader_desc in extra_sources['loaders'].items():
            self.logger.debug(key)
            self.logger.debug(loader_desc)
            data[key] = LifTreeLoader(**loader_desc).get_data(path)
        return data

    def _is_valid_path(self, path) -> LifTreeFolder:
        """
        """
        # self.logger.debug(path)
        if os.path.isfile(path):
            for folder in self.folders:
                # self.logger.debug(folder)
                if path.startswith(folder.path):
                    for exclude in folder.excludes:
                        if re.match(exclude, path) is not None:
                            return None
                    return folder
        return None

    def _get_renderer(self, path: str) -> LifTreeRenderer:
        for mapping in self.liftree_config.mappings:
            # self.logger.debug(mapping)
            if re.match(mapping['path'], path) is not None:
                renderer_name = mapping['renderer']
                # self.logger.debug(renderer_name)
                renderer = self.liftree_config.get_renderer(renderer_name)
                break
        return renderer
