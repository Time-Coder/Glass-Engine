
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


def __setattr__(self, name:str, value:Any):
    old_setattr = UniformVar._old_setattrs[self.__class__]
    old_setattr(self, name, value)
    used_value:Any = None

    id_self:int = id(self)
    for uniform_var in UniformVar._bound_vars[id_self]:
        if name in uniform_var:
            if used_value is None:
                used_value:Any = getattr(self, name)

            uniform_var[name].bind(used_value)


def __setitem__(self, index:int, value:Any):
    old_setitem = UniformVar._old_setitems[self.__class__]
    old_setitem(self, index, value)
    used_value:Any = None

    id_self:int = id(self)
    for uniform_var in UniformVar._bound_vars[id_self]:
        if index in uniform_var:
            if used_value is None:
                used_value = self[index]

            uniform_var[index].bind(used_value)


class ItemSetter:

    def __init__(self, var_class:type):
        self._old_setitem = None
        if hasattr(var_class, "__setitem__"):
            self._old_setitem = var_class.__setitem__

        self._var_class:Any = var_class

    def __call__(self, var:Any, index, value)->None:
        if self._old_setitem is not None:
            self._old_setitem(var, index, value)

        used_value = self[index]

        id_var:int = id(var)
        for uniform_var in UniformVar._bound_vars[id_var]:
            if index in uniform_var:
                uniform_var[index].bind(used_value)

    def unbind(self):
        if not hasattr(self._var_class, "__setitem__") or self._var_class.__setitem__ is not self:
            return
        
        if self._old_setitem is None:
            del self._var_class.__setitem__
        else:
            self._var_class.__setitem__ = self._old_setitem


class OnGenTypeChanged:

    def __init__(self, var:genType):
        self._var:genType = var
        self._old_on_changed:Optional[Callable[[], None]] = var.on_changed
        var.on_changed = self

    def __call__(self):
        id_var:int = id(self._var)
        for uniform_var in UniformVar._bound_vars[id_var]:
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

    _bound_vars:Dict[type, Dict[int, Set[UniformVar]]] = {}
    _old_setattrs:Dict[type, Callable[[Any,str,Any], None]] = {}
    _old_setitems:Dict[type, Callable[[Any,str,Any], None]] = {}

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
        
        var_class:type = python_var.__class__
        if var_class not in UniformVar._bound_vars:
            UniformVar._bound_vars[var_class] = {}
            if not isinstance(python_var, genType):
                if var_class.__setattr__ is not __setattr__:
                    UniformVar._old_setattrs[var_class] = var_class.__setattr__
                    var_class.__setattr__ = __setattr__

                if hasattr(var_class, '__setitem__') and var_class.__setitem__ is not __setitem__:
                    UniformVar._old_setitems[var_class] = var_class.__setitem__
                    var_class.__setitem__ = __setitem__

        id_python_var:int = id(python_var)
        if id_python_var not in UniformVar._bound_vars[var_class]:
            UniformVar._bound_vars[var_class][id_python_var] = set()
            if isinstance(python_var, genType):
                python_var.on_changed = OnGenTypeChanged(python_var)

        UniformVar._bound_vars[var_class][id_python_var].add(self)
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

        self._bound_var = python_var

    def unbind(self)->None:
        python_var = self._bound_var
        self._bound_var = None

        if python_var is None:
            return

        var_class:type = python_var.__class__
        if var_class not in UniformVar._bound_vars:
            return
        
        id_python_var = id(python_var)
        if id_python_var not in UniformVar._bound_vars[var_class]:
            return

        if self not in UniformVar._bound_vars[var_class][id_python_var]:
            return
        
        UniformVar._bound_vars[var_class][id_python_var].remove(self)
        if not UniformVar._bound_vars[var_class][id_python_var]:
            del UniformVar._bound_vars[var_class][id_python_var]

            if isinstance(python_var, genType) and isinstance(python_var.on_changed, OnGenTypeChanged):
                python_var.on_changed.unbind()

        if not UniformVar._bound_vars[var_class]:
            del UniformVar._bound_vars[var_class]

            if var_class.__setattr__ is __setattr__:
                var_class.__setattr__ = UniformVar._old_setattrs[var_class]

            if hasattr(var_class, '__setitem__') and var_class.__setitem__ is __setitem__:
                var_class.__setitem__ = UniformVar._old_setitems[var_class]


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
