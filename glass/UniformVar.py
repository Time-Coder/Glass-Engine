
from __future__ import annotations

from OpenGL import GL
from typing import Union, Dict, Any, Set, Optional, Callable, TYPE_CHECKING
from cgmath import genType

from .utils import checktype, setmethod
from .GlassConfig import GlassConfig
from .GLInfo import GLInfo
from .ShaderParser import Var

if TYPE_CHECKING:
    from .Uniforms import Uniforms


def __setattr__(self, name:str, value)->None:
    if hasattr(self.__class__, "__setattr__"):
        self.__class__.__setattr__(self, name, value)

    used_value = getattr(self, name)

    for uniform_var in UniformVar._bound_vars[self]:
        if name in uniform_var:
            uniform_var[name].bind(used_value)

def __setitem__(self, index:int, value)->None:
    if hasattr(self.__class__, "__setitem__"):
        self.__class__.__setitem__(self, index, value)

    used_value = self[index]

    for uniform_var in UniformVar._bound_vars[self]:
        if index in uniform_var:
            uniform_var[index].bind(used_value)


class OnGenTypeChanged:

    def __init__(self, var:genType):
        self._var:genType = var
        self._old_on_changed:Optional[Callable[[], None]] = var.on_changed
        var.on_changed = self

    def __call__(self):
        for uniform_var in UniformVar._bound_vars[self._var]:
            uniform_var.set_value(self._var)

        if self._old_on_changed is not None:
            self._old_on_changed()

    def unbind(self):
        if self._var.on_changed is not self:
            return
        
        self._var.on_changed = self._old_on_changed

class UniformVar:

    _all_attrs:Set[str] = {
        "_uniforms",
        "_var_token",
        "_bound_var",
    }

    _bound_vars:Dict[Any, Set[UniformVar]] = {}

    def __init__(self, uniforms:Uniforms, var_token:Var):
        self._uniforms:Uniforms = uniforms
        self._var_token:Var = var_token
        self._bound_var:Any = None

    def __contains__(self, name: Union[str, int])->bool:
        full_name = self._var_token.name
        if isinstance(name, str):
            full_name += "." + name
        elif isinstance(name, int):
            full_name += "[" + str(name) + "]"

        return full_name in self._var_token.descendants
    
    def set_value(self, value:Any)->None:
        self._uniforms[self._var_token.name] = value

    def __getitem__(self, name: Union[str, int])->UniformVar:
        full_name = self._var_token.name
        if isinstance(name, str):
            full_name += "." + name
        elif isinstance(name, int):
            full_name += "[" + str(name) + "]"

        if GlassConfig.debug and full_name not in self._var_token.descendants:
            error_message = (
                "uniform variable '"
                + full_name
                + "' is not defined in following files:\n"
            )
            error_message += "\n".join(self._uniforms._program.related_files)
            raise NameError(error_message)

        if full_name not in self._uniforms._uniform_var_map:
            self._uniforms._uniform_var_map[full_name] = UniformVar(
                self._uniforms, self._var_token.descendants[full_name]
            )

        return self._uniforms._uniform_var_map[full_name]

    @checktype
    def __setitem__(self, name: Union[str, int], value:Any)->None:
        full_name = self._var_token.name
        if isinstance(name, str):
            full_name += "." + name
        elif isinstance(name, int):
            full_name += "[" + str(name) + "]"

        if GlassConfig.debug and full_name not in self._var_token.descendants:
            error_message = (
                "uniform variable '"
                + full_name
                + "' is not defined in following files:\n"
            )
            error_message += "\n".join(self._uniforms._program.related_files)
            raise NameError(error_message)

        self._uniforms[full_name] = value

    def __getattr__(self, name: str)->UniformVar:
        if name in UniformVar._all_attrs:
            return super().__getattribute__(name)

        return self.__getitem__(name)

    def __setattr__(self, name: str, value: Any)->None:
        if name in UniformVar._all_attrs:
            return super().__setattr__(name, value)

        self.__setitem__(name, value)

    @property
    def location(self)->int:
        uniforms = self._uniforms
        program = uniforms.program

        if GlassConfig.debug and self._var_token.type not in GLInfo.atom_types:
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
        
        if self._var_token.type in GLInfo.basic_types:
            return False

        
        if python_var not in UniformVar._bound_vars:
            UniformVar._bound_vars[python_var] = set()
            if self._var_token.type not in GLInfo.gen_types:
                setmethod(python_var, "__setattr__", __setattr__)
                setmethod(python_var, "__setitem__", __setitem__)
            else:
                python_var.on_changed = OnGenTypeChanged(python_var)

        UniformVar._bound_vars[python_var].add(self)
        for child_name, child in self._var_token.children.items():
            if child.type in GLInfo.basic_types:
                continue

            suffix:str = child_name[len(self._var_token.name):]
            used_var = None
            if suffix.startswith("."):
                used_var = getattr(python_var, suffix[1:])
            elif suffix.startswith("["):
                used_var = python_var[int(suffix[1:-1])]

            self._uniforms[child_name].bind(used_var, False)

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

            if hasattr(python_var, "on_changed") and isinstance(python_var.on_changed, OnGenTypeChanged):
                python_var.on_changed.unbind()

        for child_name, child in self._var_token.children.items():
            if child.type in GLInfo.basic_types:
                continue

            suffix:str = child_name[len(self._var_token.name):]
            used_var:Any = None
            if suffix.startswith("."):
                used_var = getattr(python_var, suffix[1:])
            elif suffix.startswith("["):
                used_var = python_var[int(suffix[1:-1])]

            if self._uniforms[child_name]._bound_var is used_var:
                self._uniforms[child_name].unbind()
