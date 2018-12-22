import logging
import importlib
from constants import CONTENT_TYPE_HTML

class LifTreeObject:

    def __init__(self, **kwargs):
        self._logger = logging.getLogger(self.__class__.__name__)

    def _get_data(self):
        return dict(
            (key, value)
            for key, value in self.__dict__.items()
            if not key.startswith('_')
        )

    def __str__(self):
        return str(self._get_data())

class LifTreeLoader(LifTreeObject):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = kwargs.get('name')
        self.params = kwargs.get('params', dict())

    def get_data(self, path):
        loader = importlib.import_module(f'loaders.{self.name}')
        return loader.get_data(path, self.params)

class LifTreeExtra(LifTreeObject):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = kwargs['name']
        extra = kwargs.get('extra', dict())
        self.extra_loaders = extra.get('loaders', dict())
        self.extra_files = extra.get('files', dict())

    def _add_extra_file(self, name, file):
        self.extra_files[name] = file

    def _add_extra_loader(self, name, loader_desc):
        self.extra_loaders[name] = loader_desc

    def get_loader(self, name):
        return LifTreeLoader(**self.extra_loaders[name])

class LifTreeFolder(LifTreeExtra):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.path = kwargs['path']
        self.excludes = kwargs.get('excludes', [])

class Renderer(LifTreeExtra):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if 'loader' in kwargs:
            # self._logger.error(kwargs)
            name = kwargs['loader']
            params = kwargs.get('loader_params', dict())
            self.loader = LifTreeLoader(name=name, params=params)
        else:
            self.loader = None
        self.template = kwargs.get('template')
        self.content_type = kwargs.get('content_type', CONTENT_TYPE_HTML)
