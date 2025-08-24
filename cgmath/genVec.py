from __future__ import annotations

from typing import Set, List, Dict, Tuple, Union, Any
import ctypes
from .helper import generate_getter_swizzles, generate_setter_swizzles, from_import


class genVecIterator:

    def __init__(self, vec:genVec):
        self.__current:int = 0
        self.__vec:genVec = vec

    def __next__(self):
        if self.__current < self.__vec.size:
            value = self.__vec._data[self.__current]
            self.__current += 1
            return value
        else:
            raise StopIteration

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
    __type_order:List[type] = [
        bool, ctypes.c_bool,
        int, ctypes.c_int, ctypes.c_uint,
        float, ctypes.c_float, ctypes.c_double
    ]
    __uint_index:int = __type_order.index(ctypes.c_uint)
    __vec_type_map:Dict[Tuple[type,int], type] = {}
    __dtype_prefix_map:Dict[type, str] = {
        ctypes.c_bool: 'b',
        ctypes.c_int: 'i',
        ctypes.c_uint: 'u',
        ctypes.c_float: '',
        ctypes.c_double: 'd',
        bool: 'b',
        int: 'i',
        float: ''
    }

    namespaces:List[str] = []
    dtype:type = ctypes.c_float
    size:int = 0

    def __init__(self):
        self._data = (self.dtype * self.size)()

    def __getattr__(self, name:str):
        if name not in self._getter_swizzles():
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
        
        if len(name) == 1:
            return self._data[self._attr_index_map[name]]
        
        if len(name) == 2:
            _vec2 = self.__vec_type(self.dtype, 2)
            return _vec2(self._data[self._attr_index_map[name[0]]], self._data[self._attr_index_map[name[1]]])
        
        if len(name) == 3:
            _vec3 = self.__vec_type(self.dtype, 3)
            return _vec3(
                self._data[self._attr_index_map[name[0]]],
                self._data[self._attr_index_map[name[1]]],
                self._data[self._attr_index_map[name[2]]]
            )
        
        if len(name) == 4:
            _vec4 = self.__vec_type(self.dtype, 4)
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
    
    def __getitem__(self, index:Union[int,slice])->Union[float,int,bool,genVec]:
        result = self._data[index]
        if isinstance(result, list):
            if len(result) == 1:
                return result[0]
            else:
                result_type = self.__vec_type(self.dtype, len(result))
                return result_type(*result)
        else:
            return result
    
    def __setitem__(self, index:Union[int,slice], value:Union[float,int,bool,genVec])->None:
        if isinstance(index, slice):
            start, stop, step = index.indices(self.size)
            if isinstance(value, (float,int,bool)):
                for i in range(start, stop, step):
                    self._data[i] = value
            else:
                for i in range(start, stop, step):
                    self._data[i] = value[i]
        else:
            self._data[index] = value

    def value_ptr(self):
        return self._data
        
    @classmethod
    def _getter_swizzles(cls):
        if not cls._all_getter_swizzles:
            cls._all_getter_swizzles = set(generate_getter_swizzles(cls.namespaces))

        return cls._all_getter_swizzles
    
    @classmethod
    def _setter_swizzles(cls):
        if not cls._all_setter_swizzles:
            cls._all_setter_swizzles = set(generate_setter_swizzles(cls.namespaces))

        return cls._all_setter_swizzles
    
    @staticmethod
    def _total_swizzles():
        if not genVec.__total_swizzles:
            genVec.__total_swizzles = set(generate_getter_swizzles(['xyzw', 'rgba', 'stpq']))

        return genVec.__total_swizzles
    
    @staticmethod
    def __vec_type(dtype:type, size:int)->type:
        key:Tuple[type, int] = (dtype, size)
        if key not in genVec.__vec_type_map:
            result_name:str = f"{genVec.__dtype_prefix_map[dtype]}vec{size}"
            genVec.__vec_type_map[key] = from_import("." + result_name, result_name)

        return genVec.__vec_type_map[key]
    
    @staticmethod
    def __vec_has_negative(vec:Union[float,bool,int,genVec]):
        if isinstance(vec, (float,int,bool)):
            return (vec < 0)
        elif isinstance(vec, genVec):
            for i in range(vec.size):
                if vec._data[i] < 0:
                    return True
                
            return False
        else:
            raise TypeError(type(vec))

    def __iter__(self)->genVecIterator:
        return genVecIterator(self)

    def __len__(self)->int:
        return self.size
    
    def __contains__(self, value:Any)->bool:
        for i in range(self.size):
            if self._data[i] == value:
                return True
            
        return False

    def __repr__(self)->str:
        value_strs = []
        for i in range(self.size):
            value_strs.append(str(self._data[i]))

        return f"{self.__class__.__name__}({', '.join(value_strs)})"
    
    @staticmethod
    def __operator_dtype(type1:type, operator:str, type2:type, type2_has_negative:bool)->type:
        type1_order = genVec.__type_order.index(type1)
        type2_order = genVec.__type_order.index(type2)
        if type1_order <= genVec.__uint_index and type2_order <= genVec.__uint_index and (
            operator == "/" or (operator == "**" and type2_has_negative)
        ):
            return ctypes.c_float
        else:
            return (type1 if type1_order > type2_order else type2)

    def __operator_type(self, operator:str, other:Union[float, bool, int, genVec], reverse:bool, second_has_negative:bool=False)->type:
        other_dtype:type = None
        if isinstance(other, (float, bool, int)):
            other_dtype = type(other)
        elif isinstance(other, genVec) and self.size == other.size:
            other_dtype = other.dtype
        else:
            if not reverse:
                raise TypeError(f"unsupported operand type(s) for {operator}: '{self.__class__.__name__}' and '{other.__class__.__name__}'")
            else:
                raise TypeError(f"unsupported operand type(s) for {operator}: '{other.__class__.__name__}' and '{self.__class__.__name__}'")

        if not reverse:
            result_dtype:type = self.__operator_dtype(self.dtype, operator, other_dtype, second_has_negative)
        else:
            result_dtype:type = self.__operator_dtype(other_dtype, operator, self.dtype, second_has_negative)

        result_type:type = self.__vec_type(result_dtype, self.size)
        return result_type

    def __neg__(self)->genVec:
        result_type = self.__class__
        if self.dtype == ctypes.c_uint:
            result_type = self.__vec_type(ctypes.c_int, self.size)

        result = result_type()
        if self.dtype == ctypes.c_bool:
            for i in range(result.size):
                result._data[i] = (not self._data[i])
        else:
            for i in range(result.size):
                result._data[i] = -self._data[i]

        return result

    def __add__(self, other:Union[float, bool, int, genVec])->genVec:
        result_type = self.__operator_type("+", other, reverse=False)
        result = result_type()

        if isinstance(other, (float, bool, int)):
            for i in range(result.size):
                result._data[i] = self._data[i] + other

        elif isinstance(other, genVec) and self.size == other.size:
            for i in range(result.size):
                result._data[i] = self._data[i] + other._data[i]

        return result
    
    def __radd__(self, other:Union[float, bool, int])->genVec:
        result_type = self.__operator_type("+", other, reverse=True)
        result = result_type()

        if isinstance(other, (float, bool, int)):
            for i in range(result.size):
                result._data[i] = self._data[i] + other

        else:
            raise TypeError(f"unsupported operand type(s) for +: '{other.__class__.__name__}' and '{self.__class__.__name__}'")

        return result
    
    def __iadd__(self, other:Union[float, bool, int, genVec]):
        if isinstance(other, (float, bool, int)):
            for i in range(self.size):
                self._data[i] += other

        elif isinstance(other, genVec) and self.size == other.size:
            for i in range(self.size):
                self._data[i] += other._data[i]

        else:
            raise TypeError(f"unsupported operand type(s) for +=: '{self.__class__.__name__}' and '{other.__class__.__name__}'")
        
    def __sub__(self, other:Union[float, bool, int, genVec])->genVec:
        result_type = self.__operator_type("-", other, reverse=False)
        result = result_type()

        if isinstance(other, (float, bool, int)):
            for i in range(result.size):
                result._data[i] = self._data[i] - other

        elif isinstance(other, genVec) and self.size == other.size:
            for i in range(result.size):
                result._data[i] = self._data[i] - other._data[i]

        return result
    
    def __rsub__(self, other:Union[float, bool, int])->genVec:
        result_type = self.__operator_type("-", other, reverse=True)
        result = result_type()

        if isinstance(other, (float, bool, int)):
            for i in range(result.size):
                result._data[i] = other - self._data[i]

        else:
            raise TypeError(f"unsupported operand type(s) for -: '{other.__class__.__name__}' and '{self.__class__.__name__}'")

        return result
    
    def __isub__(self, other:Union[float, bool, int, genVec]):
        if isinstance(other, (float, bool, int)):
            for i in range(self.size):
                self._data[i] -= other

        elif isinstance(other, genVec) and self.size == other.size:
            for i in range(self.size):
                self._data[i] -= other._data[i]

        else:
            raise TypeError(f"unsupported operand type(s) for -=: '{self.__class__.__name__}' and '{other.__class__.__name__}'")
        
    def __mul__(self, other:Union[float, bool, int, genVec])->genVec:
        result_type = self.__operator_type("*", other, reverse=False)
        result = result_type()

        if isinstance(other, (float, bool, int)):
            for i in range(result.size):
                result._data[i] = self._data[i] * other

        elif isinstance(other, genVec) and self.size == other.size:
            for i in range(result.size):
                result._data[i] = self._data[i] * other._data[i]

        return result
    
    def __rmul__(self, other:Union[float, bool, int])->genVec:
        result_type = self.__operator_type("*", other, reverse=True)
        result = result_type()

        if isinstance(other, (float, bool, int)):
            for i in range(result.size):
                result._data[i] = other * self._data[i]

        else:
            raise TypeError(f"unsupported operand type(s) for *: '{other.__class__.__name__}' and '{self.__class__.__name__}'")

        return result
    
    def __imul__(self, other:Union[float, bool, int, genVec]):
        if isinstance(other, (float, bool, int)):
            for i in range(self.size):
                self._data[i] *= other

        elif isinstance(other, genVec) and self.size == other.size:
            for i in range(self.size):
                self._data[i] *= other._data[i]

        else:
            raise TypeError(f"unsupported operand type(s) for *=: '{self.__class__.__name__}' and '{other.__class__.__name__}'")
        
    def __truediv__(self, other:Union[float, bool, int, genVec])->genVec:
        result_type = self.__operator_type("/", other, reverse=False)
        result = result_type()

        if isinstance(other, (float, bool, int)):
            for i in range(result.size):
                result._data[i] = self._data[i] / other

        elif isinstance(other, genVec) and self.size == other.size:
            for i in range(result.size):
                result._data[i] = self._data[i] / other._data[i]

        return result
    
    def __rtruediv__(self, other:Union[float, bool, int])->genVec:
        result_type = self.__operator_type("/", other, reverse=True)
        result = result_type()

        if isinstance(other, (float, bool, int)):
            for i in range(result.size):
                result._data[i] = other / self._data[i]

        else:
            raise TypeError(f"unsupported operand type(s) for /: '{other.__class__.__name__}' and '{self.__class__.__name__}'")

        return result
    
    def __itruediv__(self, other:Union[float, bool, int, genVec]):
        if isinstance(other, (float, bool, int)):
            for i in range(self.size):
                self._data[i] /= other

        elif isinstance(other, genVec) and self.size == other.size:
            for i in range(self.size):
                self._data[i] /= other._data[i]

        else:
            raise TypeError(f"unsupported operand type(s) for /=: '{self.__class__.__name__}' and '{other.__class__.__name__}'")
        
    def __floordiv__(self, other:Union[float, bool, int, genVec])->genVec:
        result_type = self.__operator_type("//", other, reverse=False)
        result = result_type()

        if isinstance(other, (float, bool, int)):
            for i in range(result.size):
                result._data[i] = self._data[i] // other

        elif isinstance(other, genVec) and self.size == other.size:
            for i in range(result.size):
                result._data[i] = self._data[i] // other._data[i]

        return result
    
    def __rfloordiv__(self, other:Union[float, bool, int])->genVec:
        result_type = self.__operator_type("//", other, reverse=True)
        result = result_type()

        if isinstance(other, (float, bool, int)):
            for i in range(result.size):
                result._data[i] = other // self._data[i]

        else:
            raise TypeError(f"unsupported operand type(s) for //: '{other.__class__.__name__}' and '{self.__class__.__name__}'")

        return result
    
    def __ifloordiv__(self, other:Union[float, bool, int, genVec]):
        if isinstance(other, (float, bool, int)):
            for i in range(self.size):
                self._data[i] //= other

        elif isinstance(other, genVec) and self.size == other.size:
            for i in range(self.size):
                self._data[i] //= other._data[i]

        else:
            raise TypeError(f"unsupported operand type(s) for //=: '{self.__class__.__name__}' and '{other.__class__.__name__}'")
        
    def __mod__(self, other:Union[float, bool, int, genVec])->genVec:
        result_type = self.__operator_type("%", other, reverse=False)
        result = result_type()

        if isinstance(other, (float, bool, int)):
            for i in range(result.size):
                result._data[i] = self._data[i] % other

        elif isinstance(other, genVec) and self.size == other.size:
            for i in range(result.size):
                result._data[i] = self._data[i] % other._data[i]

        return result
    
    def __rmod__(self, other:Union[float, bool, int])->genVec:
        result_type = self.__operator_type("%", other, reverse=True)
        result = result_type()

        if isinstance(other, (float, bool, int)):
            for i in range(result.size):
                result._data[i] = other % self._data[i]

        else:
            raise TypeError(f"unsupported operand type(s) for %: '{other.__class__.__name__}' and '{self.__class__.__name__}'")

        return result
    
    def __imod__(self, other:Union[float, bool, int, genVec]):
        if isinstance(other, (float, bool, int)):
            for i in range(self.size):
                self._data[i] %= other

        elif isinstance(other, genVec) and self.size == other.size:
            for i in range(self.size):
                self._data[i] %= other._data[i]

        else:
            raise TypeError(f"unsupported operand type(s) for %=: '{self.__class__.__name__}' and '{other.__class__.__name__}'")
        
    def __pow__(self, other:Union[float, bool, int, genVec])->genVec:
        result_type = self.__operator_type("**", other, reverse=False, second_has_negative=self.__vec_has_negative(other))
        result = result_type()

        if isinstance(other, (float, bool, int)):
            for i in range(result.size):
                result._data[i] = self._data[i] ** other

        elif isinstance(other, genVec) and self.size == other.size:
            for i in range(result.size):
                result._data[i] = self._data[i] ** other._data[i]

        return result
    
    def __rpow__(self, other:Union[float, bool, int])->genVec:
        result_type = self.__operator_type("**", other, reverse=True, second_has_negative=self.__vec_has_negative(self))
        result = result_type()

        if isinstance(other, (float, bool, int)):
            for i in range(result.size):
                result._data[i] = other ** self._data[i]
        else:
            raise TypeError(f"unsupported operand type(s) for **: '{other.__class__.__name__}' and '{self.__class__.__name__}'")

        return result
    
    def __ipow__(self, other:Union[float, bool, int, genVec]):
        if isinstance(other, (float, bool, int)):
            for i in range(self.size):
                self._data[i] **= other

        elif isinstance(other, genVec) and self.size == other.size:
            for i in range(self.size):
                self._data[i] **= other._data[i]

        else:
            raise TypeError(f"unsupported operand type(s) for **=: '{self.__class__.__name__}' and '{other.__class__.__name__}'")
        
    def __eq__(self, other:Union[float, bool, int, genVec])->genVec:
        bvec = self.__vec_type(ctypes.c_bool, self.size)
        result = bvec()

        if isinstance(other, (float, bool, int)):
            for i in range(result.size):
                result._data[i] = (self._data[i] == other)

        elif isinstance(other, genVec) and self.size == other.size:
            for i in range(self.size):
                result._data[i] = (self._data[i] == other._data[i])

        else:
            raise TypeError(f"unsupported operand type(s) for ==: '{self.__class__.__name__}' and '{other.__class__.__name__}'")
        
        return result
    
    def __req__(self, other:Union[float, bool, int, genVec])->genVec:
        bvec = self.__vec_type(ctypes.c_bool, self.size)
        result = bvec()

        if isinstance(other, (float, bool, int)):
            for i in range(result.size):
                result._data[i] = (other == self._data[i])

        else:
            raise TypeError(f"unsupported operand type(s) for ==: '{other.__class__.__name__}' and '{self.__class__.__name__}'")
        
        return result
    
    def __ne__(self, other:Union[float, bool, int, genVec])->genVec:
        bvec = self.__vec_type(ctypes.c_bool, self.size)
        result = bvec()

        if isinstance(other, (float, bool, int)):
            for i in range(result.size):
                result._data[i] = (self._data[i] != other)

        elif isinstance(other, genVec) and self.size == other.size:
            for i in range(self.size):
                result._data[i] = (self._data[i] != other._data[i])

        else:
            raise TypeError(f"unsupported operand type(s) for !=: '{self.__class__.__name__}' and '{other.__class__.__name__}'")
        
        return result
    
    def __rne__(self, other:Union[float, bool, int, genVec])->genVec:
        bvec = self.__vec_type(ctypes.c_bool, self.size)
        result = bvec()

        if isinstance(other, (float, bool, int)):
            for i in range(result.size):
                result._data[i] = (other != self._data[i])

        else:
            raise TypeError(f"unsupported operand type(s) for !=: '{other.__class__.__name__}' and '{self.__class__.__name__}'")
        
        return result
    
    def __gt__(self, other:Union[float, bool, int, genVec])->genVec:
        bvec = self.__vec_type(ctypes.c_bool, self.size)
        result = bvec()

        if isinstance(other, (float, bool, int)):
            for i in range(result.size):
                result._data[i] = (self._data[i] > other)

        elif isinstance(other, genVec) and self.size == other.size:
            for i in range(self.size):
                result._data[i] = (self._data[i] > other._data[i])

        else:
            raise TypeError(f"unsupported operand type(s) for >: '{self.__class__.__name__}' and '{other.__class__.__name__}'")
        
        return result
    
    def __rgt__(self, other:Union[float, bool, int, genVec])->genVec:
        bvec = self.__vec_type(ctypes.c_bool, self.size)
        result = bvec()

        if isinstance(other, (float, bool, int)):
            for i in range(result.size):
                result._data[i] = (other > self._data[i])

        else:
            raise TypeError(f"unsupported operand type(s) for >: '{other.__class__.__name__}' and '{self.__class__.__name__}'")
        
        return result
    
    def __lt__(self, other:Union[float, bool, int, genVec])->genVec:
        bvec = self.__vec_type(ctypes.c_bool, self.size)
        result = bvec()

        if isinstance(other, (float, bool, int)):
            for i in range(result.size):
                result._data[i] = (self._data[i] < other)

        elif isinstance(other, genVec) and self.size == other.size:
            for i in range(self.size):
                result._data[i] = (self._data[i] < other._data[i])

        else:
            raise TypeError(f"unsupported operand type(s) for <: '{self.__class__.__name__}' and '{other.__class__.__name__}'")
        
        return result
    
    def __rlt__(self, other:Union[float, bool, int, genVec])->genVec:
        bvec = self.__vec_type(ctypes.c_bool, self.size)
        result = bvec()

        if isinstance(other, (float, bool, int)):
            for i in range(result.size):
                result._data[i] = (other < self._data[i])

        else:
            raise TypeError(f"unsupported operand type(s) for <: '{other.__class__.__name__}' and '{self.__class__.__name__}'")
        
        return result
    
    def __ge__(self, other:Union[float, bool, int, genVec])->genVec:
        bvec = self.__vec_type(ctypes.c_bool, self.size)
        result = bvec()

        if isinstance(other, (float, bool, int)):
            for i in range(result.size):
                result._data[i] = (self._data[i] >= other)

        elif isinstance(other, genVec) and self.size == other.size:
            for i in range(self.size):
                result._data[i] = (self._data[i] >= other._data[i])

        else:
            raise TypeError(f"unsupported operand type(s) for >=: '{self.__class__.__name__}' and '{other.__class__.__name__}'")
        
        return result
    
    def __rge__(self, other:Union[float, bool, int, genVec])->genVec:
        bvec = self.__vec_type(ctypes.c_bool, self.size)
        result = bvec()

        if isinstance(other, (float, bool, int)):
            for i in range(result.size):
                result._data[i] = (other >= self._data[i])

        else:
            raise TypeError(f"unsupported operand type(s) for >=: '{other.__class__.__name__}' and '{self.__class__.__name__}'")
        
        return result
    
    def __le__(self, other:Union[float, bool, int, genVec])->genVec:
        bvec = self.__vec_type(ctypes.c_bool, self.size)
        result = bvec()

        if isinstance(other, (float, bool, int)):
            for i in range(result.size):
                result._data[i] = (self._data[i] <= other)

        elif isinstance(other, genVec) and self.size == other.size:
            for i in range(self.size):
                result._data[i] = (self._data[i] <= other._data[i])

        else:
            raise TypeError(f"unsupported operand type(s) for <=: '{self.__class__.__name__}' and '{other.__class__.__name__}'")
        
        return result
    
    def __rle__(self, other:Union[float, bool, int, genVec])->genVec:
        bvec = self.__vec_type(ctypes.c_bool, self.size)
        result = bvec()

        if isinstance(other, (float, bool, int)):
            for i in range(result.size):
                result._data[i] = (other <= self._data[i])

        else:
            raise TypeError(f"unsupported operand type(s) for <=: '{other.__class__.__name__}' and '{self.__class__.__name__}'")
        
        return result