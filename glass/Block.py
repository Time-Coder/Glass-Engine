from OpenGL import GL
from .utils import di
from functools import wraps

from .BlockVar import BlockVar


class Block:

    _bound_vars = {}

    class HostClass:
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
                Block.upload_var(self)
                self._dirty = False

        @staticmethod
        def not_const(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                self = args[0]
                result = func(*args, **kwargs)
                self._dirty = True
                return result

            return wrapper

    def __init__(self, program):
        self._program_id = id(program)
        self._vars = {}
        self._auto_upload = True

    @property
    def program(self):
        return di(self._program_id)

    @property
    def auto_upload(self) -> bool:
        return self._auto_upload

    @auto_upload.setter
    def auto_upload(self, flag: bool) -> None:
        self._auto_upload = flag

    def upload(self, force_upload: bool = False) -> None:
        for block_var in self._block_var_map.values():
            block_var.upload(force_upload)

    @classmethod
    def upload_var(cls, var: object, force_upload: bool = False) -> None:
        id_var = id(var)
        if id_var not in cls._bound_vars:
            return

        for ssubo in cls._bound_vars[id_var].values():
            ssubo.upload(force_upload)

    @property
    def _attr_name(self)->str:
        if self.__class__.__name__ == "UniformBlock":
            return "uniform_blocks"
        elif self.__class__.__name__ == "ShaderStorageBlock":
            return "shader_storage_blocks"

    def __contains__(self, name: str) -> bool:
        if name in self._vars:
            return True

        for shader in self.program.shaders.values():
            if name in getattr(shader.parser, self._attr_name):
                return True
            
        return False

    def __getitem__(self, name: str) -> BlockVar:
        if name in self._vars:
            return self._vars[name]

        for shader in self.program.shaders.values():
            blocks = getattr(shader.parser, self._attr_name)
            if name in blocks:
                self._vars[name] = BlockVar(self, blocks[name])
                return self._vars[name]
        
        raise NameError(f"block '{name}' is not defined")

    def __setitem__(self, name: str, var: object) -> None:
        self[name].bind(var)
