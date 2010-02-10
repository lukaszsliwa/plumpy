# -*- coding: utf-8 -*-

import types
import re

__author__="Łukasz Śliwa"
__date__ ="$2010-02-09 15:30:42$"

class Router(object):
    '''
    Class setup urls with modules, functions and methods.
    '''
    names = {
        'index': ('', 'get'),
        'new': ('new', 'get'),
        'show': (r'(.+)', 'get'),
        'edit': (r'(.+)/edit', 'get'),
        'create': ('', 'post'),
        'update': (r'(.+)', 'post'),
        'delete': (r'(.+)/delete', 'post')
    }

    def __init__(self):
        self.routing = {}

    def root(self, module, **kwargs):
        self.resource('', module, **kwargs)

    def resource(self, name, module, **kwargs):
        '''
        Method adds standard functions to routing
        '''
        assert isinstance(name, types.StringType)

        name = name.strip('/')
        if name:
           name = '/' + name

        functions = self.__default(self.names)
        functions = self.__methods(functions, **kwargs)
        functions = self.__names(functions, **kwargs)
        functions = self.__only(functions, **kwargs)
        functions = self.__hide(functions, **kwargs)

        for function, (path, method) in functions.items():
            pattern = '/'.join([name, path])
            self.connect(pattern, module, getattr(module, function), method)

    def connect(self, path, module, function, method='get'):
        '''
        Method connects path to module and function with method.
        '''
        self.routing[(method.lower(), path.rstrip('/'))] = (module, function)

    def __default(self, names={}):
        return dict([ (key, value) for key, value in names.items() ])

    @classmethod
    def __methods(self, functions={}, **kwargs):
        _functions = dict(functions)
        try:    
            for function, method in kwargs['methods'].items():
                if _functions.has_key(function):
                    name, = _functions[function]
                    _functions[function] = (name, method.lower())
                else:
                    _functions[function] = (function, method.lower())
            return _functions
        except KeyError:
            return _functions

    @classmethod
    def __names(self, functions={}, **kwargs):
        _functions = dict(functions)
        try:
            for function, name in kwargs['names'].items():
                if _functions.has_key(function):
                    n, method = _functions[function]
                    _functions[function] = (name, method)
                else:
                    _functions[function] = (name, 'get')
            return _functions
        except KeyError:
            return _functions

    @classmethod
    def __only(self, functions={}, **kwargs):
        _functions = dict(functions)
        try:
            for function in _functions.keys():
                if function not in kwargs['only']:
                    del _functions[function]
            return _functions
        except KeyError:
            return _functions

    @classmethod
    def __hide(self, functions={}, **kwargs):
        _functions = dict(functions)
        try:
            for function in kwargs['hide']:
                if _functions.has_key(function):
                    del _functions[function]
            return _functions
        except KeyError:
            return _functions

    def match(self, path, method='get'):
        '''
        Method matchs got path to paths in dictionary routing.
        '''
        method = method.lower()
        if path.endswith('/'):
            path = path[:-1]
        if self.routing.has_key((method, path)):
            module, function = self.routing[(method, path)]
            return module, function, ()
        for (_method, _path), (module, function) in self.routing.items():
            if _method == method:
                params = self.__match(_path, path)
                if params:
                    return module, function, params
        return None

    def __match(self, a, b):
        _items = a.split('/')
        items = b.split('/')
        if len(_items) == len(items):
            params_a = []
            params_k = {}
            for _item, item in zip(_items, items):
                e = re.match('^' + _item + '$', item)
                if e:
                    if e.groups():
                        params_a += e.groups()
                    if e.groupdict():
                        params_k.update(e.groupdict())
                else:
                    return None
            def uni_or_int(string):
                try:
                    return int(string)
                except:
                    return unicode(string)
            if params_k:
                return dict([(key, uni_or_int(val)) for key, val in params_k])
            elif params_a:
                return tuple([uni_or_int(item) for item in params_a])
        return None

    def urls(self):
        '''
        Generator returns (method, path).
        '''
        for (method, path) in self.routing.keys():
            yield method, path

    def __str__(self):
        output = ''
        width = max([len(module.__name__) + len(function.__name__) for (m,p), (module, function) in self.routing.items()]) + 2
        for (method, path), (module, function) in self.routing.items():
            d = '%s.%s' % (module.__name__, function.__name__)
            output += '%s %s %s\n' % (d.ljust(width), method.upper().ljust(5), path)
        return output