# -*- coding: utf-8 -*-
import types

def value_cache(attr_name=None):
    """
    Decorator used to temporary cache function value as an object attribute.
    Used in case of running many calculations which aren't saved in database but can be reused before object removal.

    Can be used without arguments(temporary attribute will be _function_name):

    >>> class Bar(object):
    >>>     def __init__(self,a,b,c):
    >>>         self.a = a
    >>>         self.b = b
    >>>         self.c = c
    >>>     @value_cache
    >>>     def foo(self):
    >>>         #some aggravating calculations based on self.a, self.b and self.c
    >>>         return result
    >>> a = Bar(100,200,300)
    >>> a.foo()
    >>> #result is out and is cached so:
    >>> a._foo
    >>> #gives the same result as:
    >>> a.foo() #but now value isn't calculated again

    Or with argument(temporary attribute will be decorators argument):

    >>> class Bar(object):
    >>>     def __init__(self,a,b,c):
    >>>         self.a = a
    >>>         self.b = b
    >>>         self.c = c
    >>>     @value_cache('some_name')
    >>>     def foo(self):
    >>>         #some aggravating calculations based on self.a, self.b and self.c
    >>>         return result
    >>> a = Bar(100,200,300)
    >>> a.foo()
    >>> #result is out and is cached so:
    >>> a.some_name
    >>> #gives the same result as:
    >>> a.foo() #but now value isn't calculated again

    """
    an = attr_name

    def decorate(function):
        def decorate_inside(self, *args, **kwargs):
            attr_name = an if isinstance(an, types.StringTypes) else "_val_%s" % function.__name__
            value = getattr(self, attr_name, None)
            if value is not None:
                return value
            real_value = function(self, *args, **kwargs)
            setattr(self, attr_name, real_value)
            return real_value

        return decorate_inside

    attr_type = type(an)
    if attr_type == types.MethodType or attr_type == types.FunctionType: #jesli nie ma argumentu
        return decorate(an)
    else:
        return decorate