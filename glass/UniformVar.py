from .utils import di
from .ShaderParser import Var
from .GlassConfig import GlassConfig
from .GLInfo import GLInfo
from .WeakSet import WeakSet

from OpenGL import GL
from typing import Union, Dict, Any

class MethodsInstaller:

    list_methods = [
        "__setitem__", "__delitem__", "append", "extend",
        "insert", "remove", "pop", "clear", "sort", "reverse"
    ]

    def __setitem__(self, index:Union[int,slice], value:Any):
        id_normal_var = id(self)
        id_normal_cls = id(self.__class__)
        old_setitem = UniformVar._old_methods[id_normal_cls]["__setitem__"]
        old_setitem(self, index, value)

        if id_normal_var not in UniformVar._bound_vars:
            return
        
        if isinstance(index, int):            
            for uniform_var in UniformVar._bound_vars[id_normal_var]:
                if index in uniform_var:
                    uniform_var[index].bind(value)
        elif isinstance(index, slice):
            len_self = len(self)

            start = index.start
            stop = index.stop
            step = index.step
            if step is None:
                step = 1

            if start is None:
                start = (0 if step > 0 else len_self - 1)
            elif start < 0:
                start += len_self
            
            if stop is None:
                stop = (len_self if step > 0 else -1)
            elif stop < 0:
                stop += len_self

            indices = list(range(start, stop, step))
            if len(value) == len(indices):
                for uniform_var in UniformVar._bound_vars[id_normal_var]:
                    for i in indices:
                        if i in uniform_var:
                            uniform_var[i].bind(self[i])
            else:
                if step > 0:
                    start_index = start
                else:
                    start_index = stop + 1

                for uniform_var in UniformVar._bound_vars[id_normal_var]:
                    for i in range(start_index, len(self)):
                        if i in uniform_var:
                            uniform_var[i].bind(self[i])

    def __delitem__(self, index:Union[int,slice]):
        id_normal_var = id(self)
        id_normal_cls = id(self.__class__)
        old_delitem = UniformVar._old_methods[id_normal_cls]["__delitem__"]
        old_delitem(self, index)

        if id_normal_var not in UniformVar._bound_vars:
            return
        
        if isinstance(index, int):
            start_index = index
            for uniform_var in UniformVar._bound_vars[id_normal_var]:
                if index in uniform_var:
                    uniform_var[index].unbind()
        elif isinstance(index, slice):
            len_self = len(self)

            start = index.start
            stop = index.stop
            step = index.step
            if step is None:
                step = 1

            if start is None:
                start = (0 if step > 0 else len_self - 1)
            elif start < 0:
                start += len_self
            
            if stop is None:
                stop = (len_self if step > 0 else -1)
            elif stop < 0:
                stop += len_self

            if step > 0:
                start_index = start
            else:
                start_index = stop + 1

            for uniform_var in range():
                if index in uniform_var:
                    uniform_var[index].unbind()
            
        for uniform_var in UniformVar._bound_vars[id_normal_var]:
            for i in range(start_index, len(self)):
                if i in uniform_var:
                    uniform_var[i].bind(self[i])

    def __setattr__(self, name: str, value: Any):
        old_value = getattr(self, name)
        if id(old_value) == id(value):
            return
        
        id_normal_var = id(self)
        id_normal_cls = id(self.__class__)
        old_setattr = UniformVar._old_methods[id_normal_cls]["__setattr__"]
        old_setattr(self, name, value)

        if id_normal_var not in UniformVar._bound_vars:
            return
        
        for uniform_var in UniformVar._bound_vars[id_normal_var]:
            if name in uniform_var:
                uniform_var[name].bind(value)

    def append(self, value:Any):
        id_normal_var = id(self)
        id_normal_cls = id(self.__class__)
        old_append = UniformVar._old_methods[id_normal_cls]["append"]
        last_index = len(self)
        old_append(self, value)

        if id_normal_var not in UniformVar._bound_vars:
            return
        
        for uniform_var in UniformVar._bound_vars[id_normal_var]:
            if last_index in uniform_var:
                uniform_var[last_index].bind(value)

    def extend(self, values):
        id_normal_var = id(self)
        id_normal_cls = id(self.__class__)
        old_extend = UniformVar._old_methods[id_normal_cls]["extend"]
        last_index = len(self)
        old_extend(self, values)

        if id_normal_var not in UniformVar._bound_vars:
            return
        
        for uniform_var in UniformVar._bound_vars[id_normal_var]:
            for sub_index, value in enumerate(values):
                index = last_index + sub_index
                if index in uniform_var:
                    uniform_var[index].bind(value)

    def insert(self, index:int, value:Any):
        id_normal_var = id(self)
        id_normal_cls = id(self.__class__)
        old_insert = UniformVar._old_methods[id_normal_cls]["insert"]
        old_insert(self, index, value)

        if id_normal_var not in UniformVar._bound_vars:
            return
        
        for uniform_var in UniformVar._bound_vars[id_normal_var]:
            for i in range(index, len(self)):
                if i in uniform_var:
                    uniform_var[i].bind(self[i])

    def remove(self, value:Any):
        try:
            index = self.index(value)
            value = self[index]
        except:
            pass

        id_normal_var = id(self)
        id_normal_cls = id(self.__class__)
        old_remove = UniformVar._old_methods[id_normal_cls]["remove"]
        old_remove(self, value)

        if id_normal_var not in UniformVar._bound_vars:
            return
        
        for uniform_var in UniformVar._bound_vars[id_normal_var]:
            if index in uniform_var:
                uniform_var[index].unbind(value)

            for i in range(index, len(self)):
                if i in uniform_var:
                    uniform_var[i].bind(self[i])
                

    def pop(self, index:int):
        id_normal_var = id(self)
        id_normal_cls = id(self.__class__)
        old_pop = UniformVar._old_methods[id_normal_cls]["pop"]
        value = old_pop(self, index)

        if id_normal_var not in UniformVar._bound_vars:
            return
        
        for uniform_var in UniformVar._bound_vars[id_normal_var]:
            if index in uniform_var:
                uniform_var[index].unbind()
                
            for i in range(index, len(self)):
                if i in uniform_var:
                    uniform_var[i].bind(self[i])

        return value

    def clear(self):
        id_normal_var = id(self)
        id_normal_cls = id(self.__class__)
        old_clear = UniformVar._old_methods[id_normal_cls]["clear"]
        old_clear(self)

        if id_normal_var not in UniformVar._bound_vars:
            return
        
        for uniform_var in UniformVar._bound_vars[id_normal_var]:                
            for i in range(len(self)):
                if i in uniform_var:
                    uniform_var[i].unbind()

    def sort(self, *args, key=None, reverse=False):
        id_normal_var = id(self)
        id_normal_cls = id(self.__class__)
        old_sort = UniformVar._old_methods[id_normal_cls]["sort"]
        old_sort(self, *args, key=key, reverse=reverse)

        if id_normal_var not in UniformVar._bound_vars:
            return
        
        for uniform_var in UniformVar._bound_vars[id_normal_var]:                
            for i in range(len(self)):
                if i in uniform_var:
                    uniform_var[i].bind(self[i])

    def reverse(self):
        id_normal_var = id(self)
        id_normal_cls = id(self.__class__)
        old_reverse = UniformVar._old_methods[id_normal_cls]["reverse"]
        old_reverse(self)

        if id_normal_var not in UniformVar._bound_vars:
            return
        
        for uniform_var in UniformVar._bound_vars[id_normal_var]:
            for i in range(len(self)):
                if i in uniform_var:
                    uniform_var[i].bind(self[i])

class UniformVar:

    _bound_vars = {}
    _old_methods = {}
    _class_count = {}

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
        if name not in self._var.children:
            return super().__getattr__(name)

        return self[name]

    def __setattr__(self, name: str, value):
        if name not in self._var.children:
            return super().__setattr__(name, value)

        self[name] = value

    def bind(self, normal_var:Any):
        if id(self._normal_var) == id(normal_var):
            return

        if self._var.type in GLInfo.atom_type_map:
            self.set_value(normal_var)
            return

        if normal_var is None:
            self.unbind()
            return
        
        self.unbind()
        
        normal_cls = normal_var.__class__
        id_normal_cls = id(normal_var.__class__)
        if id_normal_cls not in UniformVar._class_count:
            UniformVar._class_count[id_normal_cls] = 0

        id_normal_var = id(normal_var)
        if id_normal_var not in UniformVar._bound_vars:
            UniformVar._bound_vars[id_normal_var] = WeakSet()

        UniformVar._bound_vars[id_normal_var].add(self)
        self._normal_var = normal_var

        if id_normal_cls not in UniformVar._old_methods:
            old_methods = {}
            UniformVar._old_methods[id_normal_cls] = old_methods
            if "[" not in self._var.type:
                if hasattr(normal_cls, "__setattr__"):
                    old_methods["__setattr__"] = normal_cls.__setattr__

                normal_cls.__setattr__ = MethodsInstaller.__setattr__
            else: # list
                for method_name in MethodsInstaller.list_methods:
                    if hasattr(normal_cls, method_name):
                        old_methods[method_name] = getattr(normal_cls, method_name)

                    setattr(normal_cls, method_name, getattr(MethodsInstaller, method_name))

        UniformVar._class_count[id_normal_cls] += 1

        for key in self._var.children:
            if isinstance(key, int):
                sub_normal_var = normal_var[key]
            else:
                sub_normal_var = getattr(normal_cls, key)

            self[key].bind(sub_normal_var)

    def unbind(self):
        if self._normal_var is None:
            return
        
        id_normal_var = id(self._normal_var)
        if id_normal_var not in UniformVar._bound_vars or self not in UniformVar._bound_vars[id_normal_var]:
            self._normal_var = None
            return
        
        uniform_var_set = UniformVar._bound_vars[id_normal_var]
        uniform_var_set.remove(self)
        if len(uniform_var_set) == 0:
            del UniformVar._bound_vars[id_normal_var]

        normal_cls = id(self._normal_var.__class__)
        id_normal_cls = id(normal_cls)
        UniformVar._class_count[id_normal_cls] -= 1
        if UniformVar._class_count[id_normal_cls] == 0:
            del UniformVar._class_count[id_normal_cls]

        if id_normal_var not in UniformVar._class_count:
            for method_name, old_method in UniformVar._old_methods[id_normal_cls].items():
                setattr(normal_cls, method_name, old_method)

            del UniformVar._old_methods[id_normal_cls]
