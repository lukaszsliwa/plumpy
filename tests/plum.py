# -*- coding: utf-8 -*-

import unittest
from plumpy import Router, Plum, render, redirect
from webob import Request
import webob.exc

class  PlumTestCase(unittest.TestCase):

    def test_empty_router(self):
        router = Router()
        plum = Plum(router)
        request = Request.blank('/')
        self.assertEqual(request.get_response(plum).status, '404 Not Found')

    def test_router_with_default_routing(self):
        import hello
        router = Router()
        router.resource('hello', hello)
        plum = Plum(router)

        status_ok = '200 OK'

        self.assertEqual(Request.blank('/hello').get_response(plum).status, status_ok)
        self.assertEqual(Request.blank('/hello/new').get_response(plum).status, status_ok)
        self.assertEqual(Request.blank('/hello/dir').get_response(plum).status, status_ok)
        self.assertEqual(Request.blank('/hello/dir/edit').get_response(plum).status, status_ok)
        self.assertEqual(Request.blank('/hello', {'REQUEST_METHOD': 'POST'}).get_response(plum).status, status_ok)
        self.assertEqual(Request.blank('/hello/123', {'REQUEST_METHOD': 'POST'}).get_response(plum).status, status_ok)
        self.assertEqual(Request.blank('/hello/456/delete', {'REQUEST_METHOD': 'POST'}).get_response(plum).status, status_ok)

        not_found = '404 Not Found'
        self.assertEqual(Request.blank('/').get_response(plum).status, not_found)
        self.assertEqual(Request.blank('/123').get_response(plum).status, not_found)

    def test_render(self):
        self.assertRaises(webob.exc.HTTPOk, render, text='text')

    def test_redirect(self):
        self.assertRaises(webob.exc.HTTPSeeOther, redirect, to='/')

if __name__ == '__main__':
    unittest.main()

