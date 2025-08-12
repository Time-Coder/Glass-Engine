from OpenGL import GL
from .utils import checktype

from typing import Union
from .GlassConfig import GlassConfig


class UniformVar:

    _all_attrs = {
        "__init__",
        "__getitem__",
        "__setitem__",
        "__getattr__",
        "__setattr__",
        "_uniform",
        "_name",
        "_bound_var",
        "bind",
        "unbind",
        "location",
    }

    def __init__(self, uniforms, name):
        self._uniforms = uniforms
        self._name = name

    @property
    def uniforms(self):
        return self._uniforms

    def __hash__(self):
        return id(self)

    def __eq__(self, other):
        return id(self) == id(other)

    @property
    def location(self):
        program = self.uniforms.program
        if program.info[self._name].location < 0:
            program.use()
            location = GL.glGetUniformLocation(program._id, self._name)
            program.info[self._name].location = location
            return location
        else:
            return program.info[self._name].location

    def __contains__(self, name: Union[str, int]):
        full_name = self._name
        if isinstance(name, str):
            full_name += "." + name
        elif isinstance(name, int):
            full_name += "[" + str(name) + "]"

        return full_name in self.uniforms._uniforms_info

    def __getitem__(self, name: Union[str, int]):
        full_name = self._name
        if isinstance(name, str):
            full_name += "." + name
        elif isinstance(name, int):
            full_name += "[" + str(name) + "]"

        uniforms = self.uniforms
        program = uniforms.program
        if GlassConfig.debug and full_name not in program.info:
            error_message = (
                "uniform variable '"
                + full_name
                + "' is not defined in following files:\n"
            )
            error_message += "\n".join(program.related_files)
            raise NameError(error_message)

        if full_name not in uniforms._uniform_var_map:
            uniforms._uniform_var_map[full_name] = UniformVar(
                self._uniform, full_name
            )

        return uniforms._uniform_var_map[full_name]

    @checktype
    def __setitem__(self, name: Union[str, int], value):
        full_name = self._name
        if isinstance(name, str):
            full_name += "." + name
        elif isinstance(name, int):
            full_name += "[" + str(name) + "]"

        uniforms = self.uniforms
        program = uniforms.program
        if GlassConfig.debug and full_name not in self.info:
            error_message = (
                "uniform variable '"
                + full_name
                + "' is not defined in following files:\n"
            )
            error_message += "\n".join(program.related_files)
            raise NameError(error_message)

        uniforms[full_name] = value

    def __getattr__(self, name: str):
        if name in UniformVar._all_attrs:
            return super().__getattribute__(name)

        return self.__getitem__(name)

    def __setattr__(self, name: str, value):
        if name in UniformVar._all_attrs:
            return super().__setattr__(name, value)

        self.__setitem__(name, value)
