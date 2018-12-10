from cgi import parse_qs
from jinja2 import Environment, FileSystemLoader
import json
import yaml
import re
import logging, logging.config
import importlib
import sys, os, grp, stat
import glob

# liftree import
from constants import *

class LifTreeObject:

    def _get_data(self):
        return dict(
            (key, value)
            for key, value in self.__dict__.items()
            if not key.startswith('_')
        )

    def __str__(self):
        return str(self._get_data())

class Renderer(LifTreeObject):
    def __init__(self, name, renderers):
        self.name = name
        self.method = renderers[name].get('content')
        self.template = renderers[name].get('template')
        self.content_type = renderers[name].get('content_type', CONTENT_TYPE_HTML)

class LifTreeConfig(LifTreeObject):

    root_config_dir = '/etc/liftree'
    root_config_file = os.path.join(root_config_dir, 'liftree.conf')
    generated_config_file = os.path.join(root_config_dir, 'generated_liftree.conf')
    root_include_dir = os.path.join(root_config_dir, 'conf.d')
    root_include_pattern = os.path.join(root_include_dir, '*.conf')

    def __init__(self):

        generated_config_exist = os.path.isfile(self.generated_config_file)
        if generated_config_exist:
            self._init_from_file(self.generated_config_file)
        else:
            self._init_from_file(self.root_config_file)

        log_config = self.defaults.get('log_config')
        if log_config is not None:
            logging.config.fileConfig(log_config)
        self._logger = logging.getLogger(self.__class__.__name__)

        generate = False
        generate_config = self.defaults.get('generate_config')
        if generate_config == 'always':
            generate = True
        elif generate_config == 'once' and not generated_config_exist:
            generate = True
        self._logger.debug(f'generate_config={generate_config}')
        self._logger.debug(f'generated_config_exist={generated_config_exist}')
        self._logger.debug(f'generate={generate}')
        if generate:
            self._init_from_file(self.root_config_file)
            for file in glob.glob(self.root_include_pattern):
                self._logger.debug(f'include={file}')
                with open(file, 'r') as stream:
                    config_include = yaml.load(stream)
                self._import_config(config_include)
            # self._write()

        self._logger.debug(f'folders={self.folders}')
        self._logger.debug(f'templates={self.templates}')
        self._logger.debug(f'mappings={self.mappings}')

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
        self._logger.debug(config_file)
        with open(config_file, 'r') as stream:
            config = yaml.load(stream)
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
        self.liftree_config = LifTreeConfig()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.debug(self.liftree_config)

    def search(self, parameters):

        by_cat = parameters.get('by_cat', ["false"])[0]
        query = parameters.get('query', [''])[0]
        pattern = query.replace(' ', '.*')
        re_pattern = re.compile(f'.*{pattern}.*')

        result_files = []
        result_folders = []

        for folder in self.liftree_config.folders:
            root_dir = folder['path']
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

        if by_cat == "true":
            result = dict()
            for file in result_files:
                renderer = self._get_renderer(file)
                if renderer.name not in result:
                    result[renderer.name] = []
                result[renderer.name].append(file)
            result['dirs'] = result_folders
        else:
            result = dict(files=result_files, dirs=result_folders)
        return result

    def render(self, parameters):
        path = self._get_path(parameters)
        renderer = self._get_renderer(path)

        self.logger.debug(f'renderer={renderer}')
        if renderer.method is not None:
            content = renderer.method
            loader = importlib.import_module(f'loaders.{content}')
            data = loader.load(path)
        else:
            data = None

        current_dir = '/usr/local/liftree/template'
        j2_env = Environment(
            loader=FileSystemLoader(self.liftree_config.templates),
            trim_blocks=True
        )

        dir_path = os.path.dirname(os.path.realpath(__file__))
        dir_filters = os.path.join(dir_path, 'filters')
        for file in os.listdir(dir_filters):
            result = re.search('^(?P<filter>.*).py$', file)
            if result:
                filter_name = result.group('filter')
                filter = importlib.import_module(f'filters.{filter_name}')
                j2_env.filters[filter_name] = getattr(filter, filter_name)

        template = j2_env.get_template(renderer.template)
        meta = dict(
            path = path,
            renderer = renderer._get_data(),
            config = self.liftree_config._get_data()
        )
        extra = dict()
        output = template.render(data=data, meta=meta, extra=extra)
        status = HTTP_200
        content_type = CONTENT_TYPE_HTML
        return(status, content_type, output.encode('utf-8'))

    def _is_valid_path(self, path):
        self.logger.debug(path)
        print(path)
        for folder in self.liftree_config.folders:
            self.logger.debug(folder)
            print(folder)
            if path.startswith(folder['path']):
                self.logger.debug(f'{path} IS VALID')
                return True
        return False

    def _get_renderer(self, path):
        renderer = Renderer('forbidden', self.liftree_config.renderers)
        if self._is_valid_path(path):
            for mapping in self.liftree_config.mappings:
                self.logger.debug(mapping)
                if re.match(mapping['path'], path) is not None:
                    renderer_name = mapping['renderer']
                    self.logger.debug(renderer_name)
                    renderer = Renderer(renderer_name, self.liftree_config.renderers)
                    break
        self.logger.debug(renderer)
        return renderer

    def _get_path(self, parameters):
        if 'path' in parameters:
            path = parameters['path'][0]
        else:
            path = self.liftree_config.defaults['path']
        self.logger.debug(path)
        return path

if __name__ == "__main__":
    #logging.basicConfig(filename='/tmp/liftree.log',level=logging.DEBUG)
    liftree = LifTree()
    parameters = dict(path=['/home/liftree/liftree/example/data/test.yaml'])
    parameters = dict(path=['/home/liftree/liftree/example/data/test.md'])
    parameters = dict(path=['/home/liftree/liftree/example/data/test.text'])
    parameters = dict(path=['/home/liftree/liftree/example/data/test.json'])
    # parameters = dict(path=['/home/liftree/liftree/example/data/test.secret'])
    status, content_type, output = liftree.render(parameters)
    print(status, content_type, output)
