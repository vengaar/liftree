from constants import CONTENT_TYPE_HTML

class LifTreeObject:

    def __init__(self,  data_dict=dict(), **kwargs):
        # print(data_dict)
        # print(kwargs)
        data_dict.update(kwargs)

    def _get_data(self):
        return dict(
            (key, value)
            for key, value in self.__dict__.items()
            if not key.startswith('_')
        )

    def __str__(self):
        return str(self._get_data())

class LifTreeExtra(LifTreeObject):
    def __init__(self,  data_dict=dict(), **kwargs):
        super().__init__(data_dict, **kwargs)
        self.name = data_dict['name']
        extra = data_dict.get('extra', dict())
        self.extra_loaders = extra.get('loaders', dict())
        self.extra_files = extra.get('files', dict())

    def _add_extra_file(self, name, file):
        self.extra_files[name] = file

    def _add_extra_loader(self, name, loader):
        self.extra_loaders[name] = loader

class LifTreeFolder(LifTreeExtra):

    def __init__(self,  data_dict=dict(), **kwargs):
        super().__init__(data_dict, **kwargs)
        self.path = data_dict['path']
        self.excludes = data_dict.get('excludes',[])

class Renderer(LifTreeExtra):
    
    def __init__(self, data_dict, **kwargs):
        super().__init__(data_dict, **kwargs)
        self.loader = data_dict.get('loader')
        self.template = data_dict.get('template')
        self.content_type = data_dict.get('content_type', CONTENT_TYPE_HTML)
