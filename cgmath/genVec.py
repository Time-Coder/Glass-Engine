from typing import Set, List, Dict
import ctypes
from .helper import generate_getter_swizzles, generate_setter_swizzles, from_import


class genVec:

    _attr_index_map:Dict[str, int] = {
        'x': 0,
        'y': 1,
        'z': 2,
        'w': 3,
        'r': 0,
        'g': 1,
        'b': 2,
        'a': 3,
        's': 0,
        't': 1,
        'p': 2,
        'q': 3
    }

    _all_attrs:Set[str] = {
        '_data'
    }
    _all_getter_swizzles:Set[str] = set()
    _all_setter_swizzles:Set[str] = set()
    __total_swizzles:Set[str] = set()

    namespaces:List[str] = []
    dtype:type = ctypes.c_float
    size:int = 0
    prefix:str = ""

    def __init__(self):
        self._data = (self.dtype * self.size)()

    def __getattr__(self, name:str):
        if name not in self._getter_swizzles():
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
        
        if len(name) == 1:
            return self._data[self._attr_index_map[name]]
        
        if len(name) == 2:
            _vec2 = self.__class__
            if _vec2.__name__ != f"{self.prefix}vec2":
                _vec2 = from_import(f".{self.prefix}vec2", f"{self.prefix}vec2")
            return _vec2(self._data[self._attr_index_map[name[0]]], self._data[self._attr_index_map[name[1]]])
        
        if len(name) == 3:
            _vec3 = self.__class__
            if _vec3.__name__ != f"{self.prefix}vec3":
                _vec3 = from_import(f".{self.prefix}vec3", f"{self.prefix}vec3")

            return _vec3(
                self._data[self._attr_index_map[name[0]]],
                self._data[self._attr_index_map[name[1]]],
                self._data[self._attr_index_map[name[2]]]
            )
        
        if len(name) == 4:
            _vec4 = self.__class__
            if _vec4.__name__ != f"{self.prefix}vec4":
                _vec4 = from_import(f".{self.prefix}vec4", f"{self.prefix}vec4")

            return _vec4(
                self._data[self._attr_index_map[name[0]]],
                self._data[self._attr_index_map[name[1]]],
                self._data[self._attr_index_map[name[2]]],
                self._data[self._attr_index_map[name[3]]]
            )
        
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    def __setattr__(self, name, value):
        if name in self._all_attrs:
            super().__setattr__(name, value)
            return
        
        if name not in self._setter_swizzles():
            if name in self._getter_swizzles():
                raise AttributeError(f"property '{name}' of '{self.__class__.__name__}' object has no setter")
            
            if name in self._total_swizzles():
                raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
            
            super().__setattr__(name, value)
            return

        if len(name) == 1:
            self._data[self._attr_index_map[name]] = value
            return
        
        if len(name) == 2:
            if isinstance(value, genVec) and value.size == 2:
                self._data[self._attr_index_map[name[0]]] = self.dtype(value[0])
                self._data[self._attr_index_map[name[1]]] = self.dtype(value[1])
            elif isinstance(value, (bool, float, int)):
                self._data[self._attr_index_map[name[0]]] = self.dtype(value)
                self._data[self._attr_index_map[name[1]]] = self.dtype(value)
            else:
                raise TypeError(f"can not set '{value.__class__.__name__}' object to property '{name}' of '{self.__class__.__name__}' object")

            return
        
        if len(name) == 3:
            if isinstance(value, genVec) and value.size == 3:
                self._data[self._attr_index_map[name[0]]] = self.dtype(value[0])
                self._data[self._attr_index_map[name[1]]] = self.dtype(value[1])
                self._data[self._attr_index_map[name[2]]] = self.dtype(value[2])
            elif isinstance(value, (bool, float, int)):
                self._data[self._attr_index_map[name[0]]] = self.dtype(value)
                self._data[self._attr_index_map[name[1]]] = self.dtype(value)
                self._data[self._attr_index_map[name[2]]] = self.dtype(value)
            else:
                raise TypeError(f"can not set '{value.__class__.__name__}' object to property '{name}' of '{self.__class__.__name__}' object")
            
            return
        
        if len(name) == 4:
            if isinstance(value, genVec) and value.size == 3:
                self._data[self._attr_index_map[name[0]]] = self.dtype(value[0])
                self._data[self._attr_index_map[name[1]]] = self.dtype(value[1])
                self._data[self._attr_index_map[name[2]]] = self.dtype(value[2])
                self._data[self._attr_index_map[name[3]]] = self.dtype(value[3])
            elif isinstance(value, (bool, float, int)):
                self._data[self._attr_index_map[name[0]]] = self.dtype(value)
                self._data[self._attr_index_map[name[1]]] = self.dtype(value)
                self._data[self._attr_index_map[name[2]]] = self.dtype(value)
                self._data[self._attr_index_map[name[3]]] = self.dtype(value)
            else:
                raise TypeError(f"can not set '{value.__class__.__name__}' object to property '{name}' of '{self.__class__.__name__}' object")
            
            return
        
        super().__setattr__(name, value)
    
    def __getitem__(self, index:int)->float:
        return self._data[index]
    
    def __setitem__(self, index:int, value:float)->None:
        self._data[index] = value

    def value_ptr(self):
        return self._data
        
    @classmethod
    def _getter_swizzles(cls):
        if not cls._all_getter_swizzles:
            cls._all_getter_swizzles = generate_getter_swizzles(cls.namespaces)

        return cls._all_getter_swizzles
    
    @classmethod
    def _setter_swizzles(cls):
        if not cls._all_setter_swizzles:
            cls._all_setter_swizzles = generate_setter_swizzles(cls.namespaces)

        return cls._all_setter_swizzles
    
    @staticmethod
    def _total_swizzles():
        if not genVec.__total_swizzles:
            genVec.__total_swizzles = generate_getter_swizzles(['xyzw', 'rgba', 'stpq'])

        return genVec.__total_swizzles
        
    def __repr__(self)->str:
        value_strs = []
        for i in range(self.size):
            value_strs.append(str(self._data[i]))

        return f"{self.__class__.__name__}({', '.join(value_strs)})"