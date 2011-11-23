# -*- coding: utf-8 -*-
import unittest, types
from ditb.decorators import value_cache

class TestValueCacheWithoutArg(unittest.TestCase):
    def setUp(self):
        class Foo(object):
            def __init__(self, **kwargs):
                names = []
                for argname, argvalue in kwargs.items():
                    if type(argvalue) is types.IntType:
                        setattr(self, argname, argvalue)
                        names.append(argname)
                self.names = names

            @value_cache
            def multiply(self):
                result = 1
                for name in self.names:
                    val = getattr(self, name)
                    result *= val
                return result
        self.Foo = Foo

    def test_value(self):
        a = self.Foo(a=1,b=2,c=3)
        result = a.multiply()
        self.assertEqual(result,6)
        a.a = 3
        self.assertEqual(a.multiply(),6)

    def test_cache(self):
        a = self.Foo(a=1, b=2, c=3)
        result = a.multiply()
        self.assertEqual(a._val_multiply,result)
        a.a = 5
        self.assertEqual(a.multiply(),result)


class TestValueCacheWithArg(unittest.TestCase):
    def setUp(self):
        class Foo(object):
            def __init__(self, **kwargs):
                names = []
                for argname, argvalue in kwargs.items():
                    if type(argvalue) is types.IntType:
                        setattr(self, argname, argvalue)
                        names.append(argname)
                self.names = names

            @value_cache('cache_decorator')
            def multiply(self):
                result = 1
                for name in self.names:
                    val = getattr(self, name)
                    result *= val
                return result

        self.Foo = Foo

    def test_value(self):
        a = self.Foo(a=1, b=2, c=3)
        result = a.multiply()
        self.assertEqual(result, 6)
        a.a = 3
        self.assertEqual(a.multiply(), 6)

    def test_cache(self):
        a = self.Foo(a=1, b=2, c=3)
        result = a.multiply()
        self.assertEqual(a.cache_decorator, result)
        a.a = 5
        self.assertEqual(a.multiply(), result)

    def test_exceptions(self):
        a = self.Foo(a=1, b=2, c=3)
        result = a.multiply()
        self.assertRaises(AttributeError,getattr,a,'_val_multiply')

if __name__ == '__main__':
    unittest.main()
