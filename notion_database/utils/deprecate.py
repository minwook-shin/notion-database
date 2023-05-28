"""
custom deprecated util
"""
import warnings
import functools


def deprecated_warn(arg):
    """
    deprecated warning
    :param arg:
    :return:
    """
    @functools.wraps(arg)
    def func(*args, **kwargs):
        warnings.simplefilter('always', DeprecationWarning)
        warnings.warn(f"deprecated function : {func.__name__}.", category=DeprecationWarning)
        warnings.warn(f"{func.__doc__}", category=DeprecationWarning)
        warnings.simplefilter('default', DeprecationWarning)
        return arg(*args, **kwargs)
    return func
