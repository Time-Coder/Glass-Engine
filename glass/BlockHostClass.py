from .Blocks import Blocks

from functools import wraps


class BlockHostClass:

    def __init__(self):
        self._dirty = True

    @property
    def dirty(self):
        return self._dirty

    @dirty.setter
    def dirty(self, flag: bool):
        self._dirty = flag

    def upload(self):
        if self._dirty:
            Blocks.upload_var(self)
            self._dirty = False

    def not_const(func):
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            self = args[0]
            result = func(*args, **kwargs)
            self._dirty = True
            return result

        return wrapper