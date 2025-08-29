import ctypes


class quat:

    def __init__(self, *args):
        self._data = (ctypes.c_float * 4)(1, 0, 0, 0)

        if len(args) == 1:
            arg = args[0]
            if isinstance(arg, (quat))