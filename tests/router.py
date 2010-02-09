# -*- coding: utf-8 -*-

import unittest

from plumpy.router import Router

class  RouterTestCase(unittest.TestCase):

    def test__init__(self):
        self.assertTrue(Router())

    def test_resource(self):
        import hello
        router = Router()
        router.resource('hello', hello)
        self.assertEqual(router.match('/hello', method='get'), (hello, 'index', ()), 'index')
        self.assertEqual(router.match('/hello/lucas/', method='get'), (hello, 'show', ('lucas',)), 'show')
        self.assertEqual(router.match('/hello/lucas/edit/', method='get'), (hello, 'edit', ('lucas',)), 'edit')
        self.assertEqual(router.match('/hello/new/', method='get'), (hello, 'new', ()), 'new')
        self.assertEqual(router.match('/hello/', method='post'), (hello, 'create', ()), 'create')
        self.assertEqual(router.match('/hello/lucas/', method='post'), (hello, 'update', ('lucas',)), 'update')
        self.assertEqual(router.match('/hello/lucas/delete/', method='post'), (hello, 'delete', ('lucas',)), 'delete')

        router.resource('', hello)
        self.assertEqual(router.match('/', method='get'), (hello, 'index', ()), 'index')
        self.assertEqual(router.match('/lucas', method='get'), (hello, 'show', ('lucas',)), 'show')
        self.assertEqual(router.match('/new', method='get'), (hello, 'new', ()), 'new')
        self.assertEqual(router.match('/', method='post'), (hello, 'create', ()), 'create')
        self.assertEqual(router.match('/lucas/edit', method='get'), (hello, 'edit', ('lucas',)), 'edit')
        self.assertEqual(router.match('/lucas', method='post'), (hello, 'update', ('lucas',)), 'update')
        self.assertEqual(router.match('/lucas/delete', method='post'), (hello, 'delete', ('lucas',)), 'delete')

        self.assertFalse(router.match('/my/own/fail'))

    def test_resource_with_names(self):
        import hello
        router = Router()
        router.resource('([a-z]{2})/hello', hello, names={ 'index': 'index', 'new': 'touch', 'show': '([0-9]{2})-([0-9]{2})-([0-9]{2})'})
        self.assertEqual(router.match('/pl/hello/index/', method='get'), (hello, 'index', ('pl',)), 'index')
        self.assertEqual(router.match('/en/hello/touch/', method='get'), (hello, 'new', ('en',)), 'new')
        self.assertEqual(router.match('/en/hello/12-34-56/', method='get'), (hello, 'show', ('en', 12, 34, 56)), 'show')

    def test_resource_with_methods(self):
        import hello
        router = Router()
        router.resource('hello', hello, methods={'own': 'get', 'Luke': 'get'}, names={'person': 'Luke'})
        self.assertEqual(router.match('/hello/Luke'), (hello, 'person', ()), 'person')
        self.assertEqual(router.match('/hello/own'), (hello, 'own', ()), 'own')

    def test_resource_with_only(self):
        import hello
        router = Router()
        router.resource('h', hello, only=['index'])
        self.assertEqual(router.match('/h'), (hello, 'index', ()), 'index')
        self.assertFalse(router.match('/h/lucas/', method='get'), 'show')
        self.assertFalse(router.match('/h/lucas/edit/', method='get'), 'edit')
        self.assertFalse(router.match('/h/new/', method='get'), 'new')
        self.assertFalse(router.match('/h/', method='post'), 'create')
        self.assertFalse(router.match('/h/lucas/', method='post'), 'update')
        self.assertFalse(router.match('/h/lucas/delete/', method='post'), 'delete')

    def test_resource_with_hide(self):
        import hello
        router = Router()
        router.resource('h', hello, hide=['show', 'edit', 'new', 'update', 'create', 'delete'])
        self.assertEqual(router.match('/h'), (hello, 'index', ()), 'index')
        self.assertFalse(router.match('/h/lucas/', method='get'), 'show')
        self.assertFalse(router.match('/h/lucas/edit/', method='get'), 'edit')
        self.assertFalse(router.match('/h/new/', method='get'), 'new')
        self.assertFalse(router.match('/h/', method='post'), 'create')
        self.assertFalse(router.match('/h/lucas/', method='post'), 'update')
        self.assertFalse(router.match('/h/lucas/delete/', method='post'), 'delete')

    def test_root(self):
        import hello
        router1 = Router()
        router2 = Router()
        router1.root(hello)
        router2.resource('', hello)

        self.assertEqual(router1.routing, router2.routing)

    def test_connect(self):
        import hello
        router = Router()
        router.connect('/333', hello, 'index')
        self.assertEqual(router.match('/333'), (hello, 'index', ()), '/333 to index')
        
        router.connect('/my-sweet-plum', hello, 'sweet')
        self.assertEqual(router.match('/my-sweet-plum'), (hello, 'sweet', ()), '/my-sweet-plum to sweet')

    def test_str(self):
        import hello
        router = Router()
        router.resource('hello', hello)
        print str(router)
        assert str(router)

if __name__ == '__main__':
    unittest.main()

