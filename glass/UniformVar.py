
from __future__ import annotations

from OpenGL import GL
from typing import Union, Dict, Any, Set

from .utils import checktype, setmethod
from .GlassConfig import GlassConfig
from .GLInfo import GLInfo
from .ShaderParser import Var


class UniformVar:

    _all_attrs:Set[str] = {
        "__init__",
        "__getitem__",
        "__setitem__",
        "__getattr__",
        "__setattr__",
        "_uniforms",
        "_name",
        "_info",
        "_bound_var",
        "bind",
        "unbind",
        "bound_var",
        "is_bound",
        "location",
    }

    _bound_vars:Dict[Any, Set[UniformVar]] = {}

    def __init__(self, uniforms, var_token:Var):
        self._uniforms = uniforms
        self._var_token:Var = var_token
        self._bound_var:Any = None

    def __contains__(self, name: Union[str, int])->bool:
        full_name = self._var_token.name
        if isinstance(name, str):
            full_name += "." + name
        elif isinstance(name, int):
            full_name += "[" + str(name) + "]"

        return full_name in self._var_token.descendants

    def __getitem__(self, name: Union[str, int])->UniformVar:
        full_name = self._var_token.name
        if isinstance(name, str):
            full_name += "." + name
        elif isinstance(name, int):
            full_name += "[" + str(name) + "]"

        uniforms = self._uniforms
        program = uniforms.program
        if GlassConfig.debug and full_name not in self._var_token.descendants:
            error_message = (
                "uniform variable '"
                + full_name
                + "' is not defined in following files:\n"
            )
            error_message += "\n".join(program.related_files)
            raise NameError(error_message)

        if full_name not in uniforms._uniform_var_map:
            uniforms._uniform_var_map[full_name] = UniformVar(
                uniforms, self._var_token.descendants[full_name]
            )

        return uniforms._uniform_var_map[full_name]

    @checktype
    def __setitem__(self, name: Union[str, int], value)->None:
        full_name = self._var_token.name
        if isinstance(name, str):
            full_name += "." + name
        elif isinstance(name, int):
            full_name += "[" + str(name) + "]"

        uniforms = self.uniforms
        program = uniforms.program
        if GlassConfig.debug and full_name not in self._var_token.descendants:
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

    @property
    def location(self)->int:
        uniforms = self._uniforms
        program = uniforms.program

        if GlassConfig.debug and self._var_token.type not in GLInfo.atom_type_names:
            raise ValueError("'" + self._var_token.name + "' is not an atom uniform variable")

        if self._var_token.location == -2:
            program.use()
            location = GL.glGetUniformLocation(program._id, self._var_token.name)
            self._var_token.location = location
            return location
        else:
            return self._var_token.location
    
    @property
    def is_bound(self)->bool:
        return (self._bound_var is not None)
    
    @property
    def bound_var(self)->Any:
        return self._bound_var

    def bind(self, python_var:Any, set_at_bind:bool=True)->bool:
        if python_var is None:
            self.unbind()
            return True
        
        if set_at_bind:
            self._uniforms[self._var_token.name] = python_var

        if self._bound_var is python_var:
            return True
        
        if self._var_token.type in GLInfo.atom_type_names:
            return False

        def __setattr__(self, name:str, value)->None:
            if hasattr(self.__class__, "__setattr__"):
                self.__class__.__setattr__(self, name, value)

            used_value = getattr(self, name)

            for uniform_var in UniformVar._bound_vars[python_var]:
                if name in uniform_var:
                    uniform_var[name].bind(used_value)

        def __setitem__(self, index:int, value)->None:
            if hasattr(self.__class__, "__setitem__"):
                self.__class__.__setitem__(self, index, value)

            used_value = self[index]

            for uniform_var in UniformVar._bound_vars[python_var]:
                if index in uniform_var:
                    uniform_var[index].bind(used_value)
        
        if python_var not in UniformVar._bound_vars:
            UniformVar._bound_vars[python_var] = set()
            setmethod(python_var, "__setattr__", __setattr__)
            setmethod(python_var, "__setitem__", __setitem__)

        UniformVar._bound_vars[python_var].add(self)
        for child_name, child in self._var_token.children.items():
            if child.type in GLInfo.atom_type_names:
                continue # to-do

            suffix:str = child_name[len(self._var_token.name):]
            if suffix.startswith("."):
                self._uniforms[child_name].bind(getattr(python_var, suffix[1:]), False)
            elif suffix.startswith("["):
                self._uniforms[child_name].bind(python_var[int(suffix[1:-1])], False)

    def unbind(self)->None:
        python_var = self._bound_var
        self._bound_var = None

        if python_var is None:
            return

        if python_var not in UniformVar._bound_vars:
            return
        
        if self not in UniformVar._bound_vars[python_var]:
            return
        
        UniformVar._bound_vars[python_var].remove(self)
        if not UniformVar._bound_vars[python_var]:
            del UniformVar._bound_vars[python_var]

            if hasattr(python_var.__class__, "__setattr__"):
                setmethod(python_var, "__setattr__", python_var.__class__.__setattr__)
            else:
                del python_var.__setattr__

            if hasattr(python_var.__class__, "__setitem__"):
                setmethod(python_var, "__setitem__", python_var.__class__.__setitem__)
            else:
                del python_var.__setitem__

        for child_name, child in self._var_token.children.items():
            if child.type in GLInfo.atom_type_names:
                continue # to-do

            suffix:str = child_name[len(self._var_token.name):]
            if suffix.startswith("."):
                if self._uniforms[child_name]._bound_var is getattr(python_var, suffix[1:]):
                    self._uniforms[child_name].unbind()

            elif suffix.startswith("["):
                if self._uniforms[child_name]._bound_var is python_var[int(suffix[1:-1])]:
                    self._uniforms[child_name].unbind()