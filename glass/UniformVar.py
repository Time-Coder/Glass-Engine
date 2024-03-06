from .utils import di
from .ShaderParser import Var
from .GlassConfig import GlassConfig
from .GLInfo import GLInfo

from OpenGL import GL
from typing import Union, Dict, Any

def setter(self, name:Union[int,str], value:Any):
    if isinstance(name, str):
        old_value = getattr(self, name)
    else:
        old_value = self[name]

    if old_value == value:
        return
    
    id_normal_var = id(self)
    id_normal_cls = id(self.__class__)
    old_setter = UniformVar._old_methods[id_normal_cls]["setter"]

    if id_normal_var not in UniformVar._bound_vars:
        old_setter(self, name, value)
        return
    
    for uniform_var in UniformVar._bound_vars[id_normal_var]:
        for key, child_var in uniform_var._var.children.items():
            if child_var.type in GLInfo.atom_type_map:
                if isinstance(key, str):
                    setattr(uniform_var, key, getattr(value, key))
                elif isinstance(key, int):
                    uniform_var[key] = value[key]
            else:
                if isinstance(key, str):
                    attr = getattr(value, key)
                elif isinstance(key, int):
                    attr = value[key]
                    
                attr_cls = attr.__class__
                id_attr_cls = id(attr_cls)
                if id_attr_cls not in UniformVar._old_methods:
                    if "[" not in child_var.type:
                        if hasattr(attr_cls, "__setattr__"):
                            UniformVar._old_methods[id_attr_cls]["__setattr__"] = attr_cls.__setattr__

                        attr_cls.__setattr__ = setter
                    else:
                        if hasattr(attr_cls, "__setitem__"):
                            UniformVar._old_methods[id_attr_cls]["__setitem__"] = attr_cls.__setitem__

                        attr_cls.__setitem__ = setter

    
                

class UniformVar:
    _all_attrs = {
        "__init__",
        "__getitem__",
        "__setitem__",
        "__getattr__",
        "__setattr__",
        "__hash__",
        "__eq__",
        "_uniform_id",
        "_var",
        "_children",
        "uniform",
        "program",
        "type",
        "full_name",
        "location",
    }

    _bound_vars = {}
    _old_methods = {}

    def __init__(self, uniform_id:int, var:Var):
        self._uniform_id:int = uniform_id
        self._var:Var = var
        self._normal_var:Any = None
        self._children:Dict[Union[str,int], UniformVar] = {}

    @property
    def uniform(self):
        return di(self._uniform_id)
    
    @property
    def program(self):
        return self.uniform.program
    
    @property
    def full_name(self)->str:
        return self._var.full_name
    
    @property
    def type(self)->str:
        return self._var.type

    @property
    def location(self):
        if self._var.location == -1:
            self._var.location = GL.glGetUniformLocation(
                self.uniform.program._id, self.full_name
            )

        return self._var.location

    def set_value(self, value):
        if not self._var.children:
            self.uniform._set_atom(self.full_name, value)
            return
        
        for child_name in self._var.children:
            sub_value = None
            if isinstance(child_name, str):
                sub_value = getattr(value, child_name)
            elif isinstance(child_name, int):
                sub_value = value[child_name]

            self._children[child_name].set_value(sub_value)
        
    def __hash__(self):
        return id(self)

    def __eq__(self, other):
        return id(self) == id(other)

    def __contains__(self, name: Union[str, int]):
        return name in self._var.children

    def __getitem__(self, name: Union[str, int]):
        if name not in self._children:
            if GlassConfig.debug and name not in self._var.children:
                if isinstance(name, int):
                    if "[" not in self._var.type:
                        raise TypeError(f"'{self._var.type}' object is not subscriptable")
                    else:
                        raise IndexError("list index out of range")
                else:
                    raise AttributeError(f"'{self._var.type}' object has no attribute '{name}'")
            
            self._children[name] = UniformVar(self.uniform, self._var.children[name])

        return self._children[name]

    def __setitem__(self, name: Union[str, int], value):
        self[name].set_value(value)

    def __getattr__(self, name: str):
        if name in UniformVar._all_attrs:
            return super().__getattr__(name)

        return self[name]

    def __setattr__(self, name: str, value):
        if name in UniformVar._all_attrs:
            return super().__setattr__(name, value)

        self[name] = value

    def bind(self, normal_var):
        if self._normal_var is not None and self._normal_var is not normal_var:
            self.unbind()

        if self._var.type in GLInfo.atom_type_map:
            raise TypeError(f"cannot bind to primitive type '{self._var.type}'")
        
        id_normal_var = id(normal_var)
        if id_normal_var not in UniformVar._bound_vars:
            UniformVar._bound_vars[id_normal_var] = set()
            normal_cls = normal_var.__class__
            id_normal_cls = id(normal_var.__class__)
            if id_normal_cls not in UniformVar._old_methods:
                UniformVar._old_methods[id_normal_cls] = {}

                if hasattr(normal_var, "__setattr__"):
                    UniformVar._old_methods[id_normal_cls]["__setattr__"] = normal_cls.__setattr__

                if hasattr(normal_var, "__setitem__"):
                    UniformVar._old_methods[id_normal_cls]["__setitem__"] = normal_cls.__setitem__

        if self not in UniformVar._bound_vars[id_normal_var]:
            UniformVar._bound_vars[id_normal_var].add(self)
