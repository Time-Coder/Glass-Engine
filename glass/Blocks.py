from typing import Dict

from .ShaderParser import Var
from .BlockVar import BlockVar


class Blocks:

    _bound_vars = {}

    def __init__(self, program):
        self._program = program
        self.info:Dict[str, Var] = {}

        self._block_var_map = {}
        self._auto_upload = True

    @property
    def program(self):
        return self._program

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

    def __contains__(self, name: str) -> bool:
        return name in self.info

    def __getitem__(self, name: str) -> BlockVar:
        if name not in self.info:
            raise NameError(f"block '{name}' is not defined")

        if name not in self._block_var_map:
            self._block_var_map[name] = BlockVar(self, name)

        return self._block_var_map[name]

    def __setitem__(self, name: str, var: object) -> None:
        self[name].bind(var)
