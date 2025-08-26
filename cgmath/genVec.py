from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Set, List, Dict, Tuple, Union, Any, Optional, Callable, TYPE_CHECKING
import ctypes
from .helper import generate_getter_swizzles, generate_setter_swizzles, from_import

if TYPE_CHECKING:
    from .genMat import genMat


class genVec(ABC):

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
        '_data', '_related_mat', '_mat_start_index', '_on_changed'
    }
    _all_getter_swizzles:Set[str] = set()
    _all_setter_swizzles:Set[str] = set()
    __all_total_swizzles:Set[str] = set()
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

    __namespaces:List[str] = ['xyzw', 'rgba', 'stpq']
    __operator_funcs:Dict[str, Callable[[Any,Any], Any]] = {
        "+": lambda x, y: x + y,
        "-": lambda x, y: x - y,
        "*": lambda x, y: x * y,
        "/": lambda x, y: x / y,
        "//": lambda x, y: x // y,
        "%": lambda x, y: x % y,
        "**": lambda x, y: x ** y,
        ">": lambda x, y: x > y,
        ">=": lambda x, y: x >= y,
        "<": lambda x, y: x < y,
        "<=": lambda x, y: x <= y,
        "==": lambda x, y: x == y,
        "!=": lambda x, y: x != y
    }

    def __init__(self):
        self._data = (self.dtype * len(self))()
        self._related_mat:Optional[genMat] = None
        self._mat_start_index:int = -1
        self._on_changed:Optional[Callable[[genVec], None]] = None

    @property
    @abstractmethod
    def dtype(self)->type:
        pass
    
    @abstractmethod
    def __len__(self)->int:
        pass

    def __update_data(self, indices:Optional[List[int]] = None):
        if self._on_changed is not None:
            self._on_changed(self)

        if self._related_mat is not None:
            if indices is None:
                indices = range(len(self))

            for index in indices:
                self._related_mat._data[self._mat_start_index + index] = self._data[index]

            if self._related_mat._on_changed is not None:
                self._related_mat._on_changed(self._related_mat)

    def __getattr__(self, name:str)->Union[float,bool,int,genVec]:
        if name not in self.__getter_swizzles():
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
        
        if len(name) == 1:
            return self._data[self._attr_index_map[name]]
        
        if len(name) == 2:
            _vec2 = self.vec_type(self.dtype, 2)
            return _vec2(self._data[self._attr_index_map[name[0]]], self._data[self._attr_index_map[name[1]]])
        
        if len(name) == 3:
            _vec3 = self.vec_type(self.dtype, 3)
            return _vec3(
                self._data[self._attr_index_map[name[0]]],
                self._data[self._attr_index_map[name[1]]],
                self._data[self._attr_index_map[name[2]]]
            )
        
        if len(name) == 4:
            _vec4 = self.vec_type(self.dtype, 4)
            return _vec4(
                self._data[self._attr_index_map[name[0]]],
                self._data[self._attr_index_map[name[1]]],
                self._data[self._attr_index_map[name[2]]],
                self._data[self._attr_index_map[name[3]]]
            )
        
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    def __setattr__(self, name:str, value:Union[float,bool,int,genVec]):
        if name in self._all_attrs:
            super().__setattr__(name, value)
            return
        
        if name not in self.__setter_swizzles():
            if name in self.__getter_swizzles():
                raise AttributeError(f"property '{name}' of '{self.__class__.__name__}' object has no setter")
            
            if name in self.__total_swizzles():
                raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
            
            super().__setattr__(name, value)
            return

        update_indices:List[int] = []
        value_is_vec:bool = (isinstance(value, genVec) and len(value) == len(name))
        if not value_is_vec and not isinstance(value, (bool, float, int)):
            raise TypeError(f"can not set '{value.__class__.__name__}' object to property '{name}' of '{self.__class__.__name__}' object")
        
        for i, ch in enumerate(name):
            index:int = self._attr_index_map[ch]
            self._data[index] = value[i] if value_is_vec else value
            update_indices.append(index)
        self.__update_data(update_indices)
    
    def __getitem__(self, index:Union[int,slice])->Union[float,int,bool,genVec]:
        result = self._data[index]
        if isinstance(result, list):
            if len(result) == 1:
                return result[0]
            else:
                result_type = self.vec_type(self.dtype, len(result))
                return result_type(*result)
        else:
            return result
    
    def __setitem__(self, index:Union[int,slice], value:Union[float,int,bool,genVec])->None:
        if isinstance(index, int):
            self._data[index] = value
            self.__update_data([index])
            return

        start, stop, step = index.indices(len(self))
        value_is_vec:bool = (not isinstance(value, (float, int, bool)))
        update_indices:List[int] = []
        for i in range(start, stop, step):
            self._data[i] = value[i] if value_is_vec else value
            update_indices.append(i)

        self.__update_data(update_indices)
        
    def value_ptr(self):
        return self._data
        
    def __getter_swizzles(self):
        if not self.__class__._all_getter_swizzles:
            n:int = len(self)
            namespaces:List[str] = [namespace[:n] for namespace in genVec.__namespaces]
            self._all_getter_swizzles = set(generate_getter_swizzles(namespaces))

        return self._all_getter_swizzles
    
    def __setter_swizzles(self):
        if not self._all_setter_swizzles:
            n:int = len(self)
            namespaces:List[str] = [namespace[:n] for namespace in genVec.__namespaces]
            self._all_setter_swizzles = set(generate_setter_swizzles(namespaces))

        return self._all_setter_swizzles
    
    @staticmethod
    def __total_swizzles():
        if not genVec.__all_total_swizzles:
            genVec.__all_total_swizzles = set(generate_getter_swizzles(genVec.__namespaces))

        return genVec.__all_total_swizzles
    
    @staticmethod
    def vec_type(dtype:type, size:int)->type:
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
            for i in range(len(vec)):
                if vec._data[i] < 0:
                    return True
                
            return False
        else:
            raise TypeError(type(vec))

    def __iter__(self):
        return iter(self._data)
    
    def __contains__(self, value:Any)->bool:
        return (value in self._data)

    def __repr__(self)->str:
        value_strs = []
        for i in range(len(self)):
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
        elif isinstance(other, genVec) and len(self) == len(other):
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

        result_type:type = self.vec_type(result_dtype, len(self))
        return result_type

    def __neg__(self)->genVec:
        result_type = self.__class__
        if self.dtype == ctypes.c_uint:
            result_type = self.vec_type(ctypes.c_int, len(self))

        result:genVec = result_type()
        for i in range(len(result)):
            result._data[i] = ((not self._data[i]) if self.dtype == ctypes.c_bool else -self._data[i])

        return result

    def __op(self, operator:str, other:Union[float, bool, int, genVec])->genVec:
        second_has_negative:bool = False
        if operator == "**":
            second_has_negative = self.__vec_has_negative(other)

        result_type = self.__operator_type(operator, other, reverse=False, second_has_negative=second_has_negative)
        result:genVec = result_type()
        other_is_vec:bool = (isinstance(other, genVec) and len(self) == len(other))
        operator_func:Callable[[Any,Any], Any] = self.__operator_funcs[operator]
        for i in range(len(result)):
            result._data[i] = operator_func(self._data[i], other._data[i] if other_is_vec else other)

        return result
    
    def __rop(self, operator:str, other:Union[float, bool, int, genVec])->genVec:
        second_has_negative:bool = False
        if operator == "**":
            second_has_negative = self.__vec_has_negative(other)

        result_type = self.__operator_type(operator, other, reverse=True, second_has_negative=second_has_negative)
        result:genVec = result_type()
        operator_func:Callable[[Any,Any], Any] = self.__operator_funcs[operator]
        for i in range(len(result)):
            result._data[i] = operator_func(self._data[i], other)

        return result
    
    def __iop(self, operator:str, other:Union[float, bool, int, genVec])->genVec:
        other_is_vec:bool = (isinstance(other, genVec) and len(self) == len(other))
        if not other_is_vec and not isinstance(other, (float, bool, int)):
            raise TypeError(f"unsupported operand type(s) for {operator}=: '{self.__class__.__name__}' and '{other.__class__.__name__}'")
        
        operator_func:Callable[[Any,Any], Any] = self.__operator_funcs[operator]
        for i in range(len(self)):
            self._data[i] = operator_func(self._data[i], other._data[i] if other_is_vec else other)

        self.__update_data()

        return self
    
    def __compare_op(self, operator:str, other:Union[float, bool, int, genVec])->genVec:
        bvec = self.vec_type(ctypes.c_bool, len(self))
        result:genVec = bvec()

        other_is_vec:bool = (isinstance(other, genVec) and len(self) == len(other))
        if not other_is_vec and not isinstance(other, (float, bool, int)):
            raise TypeError(f"unsupported operand type(s) for ==: '{self.__class__.__name__}' and '{other.__class__.__name__}'")
        
        operator_func:Callable[[Any,Any], Any] = self.__operator_funcs[operator]
        for i in range(len(self)):
            result._data[i] = operator_func(self._data[i], other._data[i] if other_is_vec else other)
        
        return result
    
    def __compare_rop(self, operator:str, other:Union[float, bool, int, genVec])->genVec:
        bvec = self.vec_type(ctypes.c_bool, len(self))
        result:genVec = bvec()

        operator_func:Callable[[Any,Any], Any] = self.__operator_funcs[operator]
        for i in range(len(result)):
            result._data[i] = operator_func(other, self._data[i])
        
        return result
    
    def __add__(self, other:Union[float, bool, int, genVec])->genVec:
        return self.__op("+", other)
    
    def __radd__(self, other:Union[float, bool, int])->genVec:
        return self.__rop("+", other)
    
    def __iadd__(self, other:Union[float, bool, int, genVec])->genVec:
        return self.__iop("+", other)

    def __sub__(self, other:Union[float, bool, int, genVec])->genVec:
        return self.__op("-", other)
    
    def __rsub__(self, other:Union[float, bool, int])->genVec:
        return self.__rop("-", other)
    
    def __isub__(self, other:Union[float, bool, int, genVec])->genVec:
        return self.__iop("-", other)

    def __mul__(self, other:Union[float, bool, int, genVec])->genVec:
        return self.__op("*", other)
    
    def __rmul__(self, other:Union[float, bool, int])->genVec:
        return self.__rop("*", other)
    
    def __imul__(self, other:Union[float, bool, int, genVec])->genVec:
        return self.__iop("*", other)

    def __truediv__(self, other:Union[float, bool, int, genVec])->genVec:
        return self.__op("/", other)
    
    def __rtruediv__(self, other:Union[float, bool, int])->genVec:
        return self.__rop("/", other)
    
    def __itruediv__(self, other:Union[float, bool, int, genVec]):
        return self.__iop("/", other)

    def __floordiv__(self, other:Union[float, bool, int, genVec])->genVec:
        return self.__op("//", other)
    
    def __rfloordiv__(self, other:Union[float, bool, int])->genVec:
        return self.__rop("//", other)
    
    def __ifloordiv__(self, other:Union[float, bool, int, genVec]):
        return self.__iop("//", other)

    def __mod__(self, other:Union[float, bool, int, genVec])->genVec:
        return self.__op("%", other)
    
    def __rmod__(self, other:Union[float, bool, int])->genVec:
        return self.__rop("%", other)
    
    def __imod__(self, other:Union[float, bool, int, genVec]):
        return self.__iop("%", other)

    def __pow__(self, other:Union[float, bool, int, genVec])->genVec:
        return self.__op("**", other)
    
    def __rpow__(self, other:Union[float, bool, int])->genVec:
        return self.__rop("**", other)
    
    def __ipow__(self, other:Union[float, bool, int, genVec]):
        return self.__iop("**", other)

    def __eq__(self, other:Union[float, bool, int, genVec])->genVec:
        return self.__compare_op("==", other)
    
    def __req__(self, other:Union[float, bool, int, genVec])->genVec:
        return self.__compare_rop("==", other)
    
    def __ne__(self, other:Union[float, bool, int, genVec])->genVec:
        return self.__compare_op("!=", other)
    
    def __rne__(self, other:Union[float, bool, int, genVec])->genVec:
        return self.__compare_rop("!=", other)
    
    def __gt__(self, other:Union[float, bool, int, genVec])->genVec:
        return self.__compare_op(">", other)
    
    def __rgt__(self, other:Union[float, bool, int, genVec])->genVec:
        return self.__compare_rop(">", other)
    
    def __lt__(self, other:Union[float, bool, int, genVec])->genVec:
        return self.__compare_op("<", other)
    
    def __rlt__(self, other:Union[float, bool, int, genVec])->genVec:
        return self.__compare_rop("<", other)
    
    def __ge__(self, other:Union[float, bool, int, genVec])->genVec:
        return self.__compare_op(">=", other)
    
    def __rge__(self, other:Union[float, bool, int, genVec])->genVec:
        return self.__compare_rop(">=", other)
    
    def __le__(self, other:Union[float, bool, int, genVec])->genVec:
        return self.__compare_op("<=", other)
    
    def __rle__(self, other:Union[float, bool, int, genVec])->genVec:
        return self.__compare_rop("<=", other)