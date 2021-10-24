import warnings
import functools


def deprecated_warn(arg):
    @functools.wraps(arg)
    def func(*args, **kwargs):
        warnings.simplefilter('always', DeprecationWarning)
        warnings.warn("deprecated function {}.".format(func.__name__), category=DeprecationWarning)
        warnings.warn("{}".format(func.__doc__), category=DeprecationWarning)
        warnings.simplefilter('default', DeprecationWarning)
        return arg(*args, **kwargs)
    return func
