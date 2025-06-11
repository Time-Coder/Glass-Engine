from glass import GLConfig


class RenderHints:

    inherit = "inherit"
    __all_attrs = {
        "__class__",
        "__delattr__",
        "__dict__",
        "__dir__",
        "__doc__",
        "__enter__",
        "__eq__",
        "__exit__",
        "__format__",
        "__ge__",
        "__getattribute__",
        "__getstate__",
        "__gt__",
        "__hash__",
        "__init__",
        "__init_subclass__",
        "__le__",
        "__lt__",
        "__module__",
        "__ne__",
        "__new__",
        "__reduce__",
        "__reduce_ex__",
        "__repr__",
        "__setattr__",
        "__sizeof__",
        "__str__",
        "__subclasshook__",
        "__weakref__",
        "__getattr__",
        "_temp_env",
        "_values"
    }

    def __init__(self):
        self._temp_env = GLConfig.LocalEnv()
        self._values = {}

    def __enter__(self):
        self._temp_env.__enter__()
        for key, value in self._values.items():
            setattr(GLConfig, key, value)

    def __exit__(self, *exc_details):
        self._temp_env.__exit__(*exc_details)

    def __getattr__(self, name):
        if name in RenderHints.__all_attrs:
            return super().__getattr__(name)
        
        if not GLConfig.hassetter(name):
            raise AttributeError(f"GLConfig has no attribute '{name}'")

        if name in self._values:
            return self._values[name]
        else:
            return RenderHints.inherit

    def __setattr__(self, name, value):
        if name in RenderHints.__all_attrs:
            return super().__setattr__(name, value)

        if not GLConfig.hassetter(name):
            raise AttributeError(f"GLConfig has no attribute '{name}'")

        if value == RenderHints.inherit:
            del self._values[name]
        else:
            self._values[name] = value
