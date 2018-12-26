from jinja2 import Environment, FileSystemLoader
import json
import yaml
import re, fnmatch
import logging, logging.config
import importlib, inspect
import sys, os, grp, stat
import glob

# liftree import
from constants import *
from loaders.file_yaml_loader import get_data as load_yaml_file
from classes import LifTreeObject, LifTreeFolder, LifTreeLoader, Renderer

class LifTreeConfig(LifTreeObject):

    root_config_dir = '/etc/liftree'
    root_config_file = os.path.join(root_config_dir, 'liftree.conf')
    generated_config_file = os.path.join(root_config_dir, 'generated_liftree.conf')
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
        self.import_path = []
        if generate:
            self._init_from_file(self.root_config_file)
            for file in sorted(glob.glob(self.root_include_pattern)):
                # print(file)
                self._logger.info(f'include={file}')
                with open(file, 'r') as stream:
                    config_include = yaml.load(stream)
                self._import_config(config_include)
            # self._write()

        sys.path = sys.path + self.import_path

        self._logger.debug(f'folders={self.folders}')
        self._logger.debug(f'templates={self.templates}')
        self._logger.debug(f'mappings={self.mappings}')

    def get_renderer(self, name):
        renderer_data = self.renderers[name]
        return Renderer(name=name, **renderer_data)

    def _init_from_file(self, file):
        with open(self.root_config_file, 'r') as stream:
            config = yaml.load(stream)
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
        # self.import_path.append(os.path.join(config_folder, 'loaders'))
        # self.import_path.append(os.path.join(config_folder, 'filters'))

        self._logger.debug(config_file)
        with open(config_file, 'r') as stream:
            config = yaml.load(stream)
        renderers = config.get('renderers', dict())
        self.renderers.update(renderers)
        folders = config.get('folders', [])
        folders = [
            LifTreeFolder(**data)
            for data in config.get('folders', [])
        ]
        self.folders.extend(folders)
        mappings = config.get('mappings', [])
        self.mappings = mappings + self.mappings
        templates = os.path.join(config_folder, 'templates')
        self.templates.insert(0, templates)
        default = config.get('defaults', dict())
        self.defaults.update(default)

class LifTree:

    def __init__(self):
        self.liftree_config = LifTreeConfig()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.debug(self.liftree_config)

    def search(self, query):
        pattern = query.replace(' ', '.*')
        re_pattern = re.compile(f'.*{pattern}.*')
        result_files = []
        result_folders = []
        for folder in self.liftree_config.folders:
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

    def render(self, path):
        path = self.liftree_config.defaults['path'] if path is None else path
        folder = self._is_valid_path(path)
        if folder is None:
            renderer = self.liftree_config.get_renderer('forbidden')
        else:
            renderer = self._get_renderer(path)
        self.logger.debug(f'renderer={renderer}')
        if renderer.loader is not None:
            data = renderer.loader.get_data(path)
        else:
            data = None
        j2_env = Environment(
            loader=FileSystemLoader(self.liftree_config.templates),
            trim_blocks=True
        )

        # Add custom filters
        filters = []
        import_dirs = [os.path.dirname(os.path.realpath(__file__))] + self.liftree_config.import_path
        for import_dir in import_dirs:
            filter_dir = os.path.join(import_dir, 'filters')
            if os.path.isdir(filter_dir):
                for file in os.listdir(filter_dir):
                    result = re.search('^(?P<module_name>.*).py$', file)
                    if result is not None:
                        module_name = result.group('module_name')
                        module_filter = importlib.import_module(f'filters.{module_name}')
                        for tuple_function in inspect.getmembers(module_filter, predicate=inspect.isfunction):
                            (name, function) = tuple_function
                            filter_prefix = 'filter_'
                            if name.startswith(filter_prefix):
                                filter_name = name[len(filter_prefix):]
                                filters.append(filter_name)
                                j2_env.filters[filter_name] = function

        template = j2_env.get_template(renderer.template)
        meta = dict(
            path = path,
            folder = folder,
            renderer = renderer._get_data(),
            config = self.liftree_config._get_data(),
            filters = filters,
            self = id(self)
        )
        extra_sources = self._build_extra(renderer, folder)
        extra = self._get_extra(extra_sources, path)
        output = template.render(data=data, meta=meta, extra=extra, extra_sources=extra_sources)
        status = HTTP_200
        content_type = CONTENT_TYPE_HTML
        return(status, content_type, output.encode('utf-8'))

    def _build_extra(self, renderer, folder):
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

    def _get_extra(self, extra_sources, path):
        data = dict()
        for key, file in extra_sources['files'].items():
            data[key] = load_yaml_file(file, None)
        self.logger.error(extra_sources)
        for key, loader_desc in extra_sources['loaders'].items():
            self.logger.error(key)
            self.logger.error(loader_desc)
            data[key] = LifTreeLoader(**loader_desc).get_data(path)
            #data[key] = dict()
        return data

    def _is_valid_path(self, path):
        """
        """
        self.logger.debug(path)
        for folder in self.liftree_config.folders:
            self.logger.debug(folder)
            if path.startswith(folder.path):
                for exclude in folder.excludes:
                    if re.match(exclude, path) is not None:
                        return None
                return folder
        return None

    def _get_renderer(self, path):
        for mapping in self.liftree_config.mappings:
            self.logger.debug(mapping)
            if re.match(mapping['path'], path) is not None:
                renderer_name = mapping['renderer']
                self.logger.debug(renderer_name)
                renderer = self.liftree_config.get_renderer(renderer_name)
                break
        return renderer
