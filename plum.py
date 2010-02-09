# -*- coding: utf-8 -*-

from webob import Response, Request
from webob.exc import HTTPException, HTTPNotFound
import types

__author__="Łukasz Śliwa"
__date__ ="$2010-02-09 15:32:14$"

class Plum(object):
    '''
    WSGI Application class
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
        request = Request(environ)
        response = Response()
        try:
            object = self.router.match(request.path_info, request.method)
            if object:
                module, function, args = object
                module.request = request
                module.response = response
                if isinstance(args, types.TupleType):
                    response.unicode_body = module.__dict__[function](*args)
                else:
                    response.unicode_body = module.__dict__[function](**args)
            else:
                raise HTTPNotFound('Page %s doesn\'t exists.' % request.path_info).exception
        except HTTPException, e:
            return e(environ, start_response)
        return response(environ, start_response)

if __name__ == '__main__':

    from plumpy import Router
    import plumpy.tests.hello

    router = Router()
    router.root(plumpy.tests.hello)
    router.resource('hello', plumpy.tests.hello)

    from paste import httpserver

    app = Plum(router)
    httpserver.serve(app, host='127.0.0.1', port='8080')
