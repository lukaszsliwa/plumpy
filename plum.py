# -*- coding: utf-8 -*-

from webob import Response, Request
import webob.exc
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
                    function(*args)
                else:
                    function(**args)
            else:
                raise webob.exc.HTTPNotFound('Page %s doesn\'t exists.' % request.path_info).exception
        except webob.exc.HTTPException, e:
            return e(environ, start_response)
        return response(environ, start_response)

def render(text, status=200, format='html'):
    '''
    Function raises HTTP* exception with given status and content_type.
    '''
    formats = {
        'html': 'text/html',
        'plain': 'text/plain',
        'xml': 'application/xml',
        'json': 'application/json'
    }
    raise webob.exc.status_map[int(status)](body=text, content_type=formats[format])

def redirect(to, status=303):
    '''
    Function redirects to given location
    '''
    raise webob.exc.status_map[int(status)](location=to)