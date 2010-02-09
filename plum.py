# -*- coding: utf-8 -*-

from webob import Response

__author__="Łukasz Śliwa"
__date__ ="$2010-02-09 15:32:14$"

class Plum(object):
    '''
    Application class
    '''
    def __init__(self, *args, **kwargs):
        '''
        Constructor gets a router as an argument.
            import plumpy
            router = plumpy.Router()
            ...
            application = Plum(router)
            ...
        '''
        router = kwargs.get('router') or args[0]
        self.router = router

    def __call__(self, environ, start_response):
        '''
        Method returns callable wsgi object.
        '''
        response = Response()
        return response(environ, start_response)
