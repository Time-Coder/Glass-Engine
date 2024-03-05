from .utils import di
from .ShaderParser import Var
from .GlassConfig import GlassConfig

from OpenGL import GL
from typing import Union, Dict

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

    def __init__(self, uniform_id:int, var:Var):
        self._uniform_id:int = uniform_id
        self._var:Var = var
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
