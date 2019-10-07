# memoize.py

# memoization recipes
import functools

def memoize(f):
    """ Memoization decorator for functions taking one or more arguments. """
    class memodict(dict):
        def __init__(self, f):
            self.f = f
        def __get__(self, obj, objtype):
            """Support instance methods."""
            return functools.partial(self.__call__, obj)
        def __call__(self, *args):
            return self[args]
        def __missing__(self, key):
            #print("New Object: " + str(self.f) + "(" + str(key) + ")")
            ret = self[key] = self.f(*key)
            return ret
    return memodict(f)
