from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Dict, Tuple, Union, Any, Optional, Callable
import ctypes
from .helper import from_import, is_number
import math
from enum import Enum


class MathForm(Enum):
    Vec = 0
    Mat = 1
    Quat = 2


class genType(ABC):

    __type_order:List[type] = [
        bool, ctypes.c_bool,
        int, ctypes.c_int, ctypes.c_uint,
        float, ctypes.c_float, ctypes.c_double
    ]
    __uint_index:int = __type_order.index(ctypes.c_uint)
    __gen_type_map:Dict[Tuple[type,int], type] = {}
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
    __dtype_python_type_map:Dict[type, type] = {
        ctypes.c_bool: bool,
        ctypes.c_int: int,
        ctypes.c_uint: int,
        ctypes.c_float: float,
        ctypes.c_double: float,
    }

    _operator_funcs:Dict[str, Callable[[Any,Any], Any]] = {
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
        self._data = (self.dtype * math.prod(self.shape))()
        self._on_changed:Optional[Callable[[genType], None]] = None

    def __repr__(self)->str:
        return f"{self.__class__.__name__}({', '.join([str(value) for value in self])})"

    @property
    def on_changed(self)->Optional[Callable[[genType], None]]:
        return self._on_changed
    
    @on_changed.setter
    def on_changed(self, on_changed:Optional[Callable[[genType], None]]):
        if not callable(on_changed):
            raise TypeError('on_changed should be a function')

        self._on_changed = on_changed

    @property
    @abstractmethod
    def math_form(self)->MathForm:
        pass

    @property
    @abstractmethod
    def dtype(self)->type:
        pass
    
    @property
    @abstractmethod
    def shape(self)->Tuple[int]:
        pass

    @staticmethod
    def gen_type(dtype:type, shape:Tuple[int])->type:
        key:Tuple[type, int] = (dtype, shape)
        if key not in genType.__gen_type_map:
            if math.prod(shape) == 1:
                genType.__gen_type_map[key] = genType.__dtype_python_type_map[dtype]
            else:
                if len(shape) == 1:
                    result_name:str = f"{genType.__dtype_prefix_map[dtype]}vec{shape[0]}"
                else:
                    result_name:str = f"{genType.__dtype_prefix_map[dtype]}mat{shape[0]}x{shape[1]}"
                genType.__gen_type_map[key] = from_import("." + result_name, result_name)

        return genType.__gen_type_map[key]
        
    def value_ptr(self):
        return self._data
    
    def _update_data(self, indices:Optional[List[int]] = None):
        if self._on_changed is not None:
            self._on_changed(self)

    @staticmethod
    def __has_negative(value:Union[float,bool,int,genType]):
        if is_number(value):
            return (value < 0)
        elif isinstance(value, genType):
            for i in range(len(value._data)):
                if value._data[i] < 0:
                    return True
                
            return False
        else:
            raise TypeError(type(value))
    
    @staticmethod
    def _operator_dtype(type1:type, operator:str, type2:type, type2_has_negative:bool)->type:
        type1_order = genType.__type_order.index(type1)
        type2_order = genType.__type_order.index(type2)
        if type1_order <= genType.__uint_index and type2_order <= genType.__uint_index and (
            operator == "/" or (operator == "**" and type2_has_negative)
        ):
            return ctypes.c_float
        else:
            return (type1 if type1_order > type2_order else type2)

    def _operator_type(self, operator:str, other:Union[float, bool, int, genType], reverse:bool, second_has_negative:bool=False)->type:
        other_dtype:type = None
        if is_number(other):
            other_dtype = type(other)
        elif isinstance(other, genType) and self.shape == other.shape:
            other_dtype = other.dtype
        else:
            if not reverse:
                raise TypeError(f"unsupported operand type(s) for {operator}: '{self.__class__.__name__}' and '{other.__class__.__name__}'")
            else:
                raise TypeError(f"unsupported operand type(s) for {operator}: '{other.__class__.__name__}' and '{self.__class__.__name__}'")

        if not reverse:
            result_dtype:type = self._operator_dtype(self.dtype, operator, other_dtype, second_has_negative)
        else:
            result_dtype:type = self._operator_dtype(other_dtype, operator, self.dtype, second_has_negative)

        result_type:type = self.gen_type(result_dtype, self.shape)
        return result_type

    def __neg__(self)->genType:
        result_type = self.__class__
        if self.dtype == ctypes.c_uint:
            result_type = self.gen_type(ctypes.c_int, self.shape)

        result:genType = result_type()
        for i in range(len(result._data)):
            result._data[i] = ((not self._data[i]) if self.dtype == ctypes.c_bool else -self._data[i])

        return result

    def _is_homo(self, other:Any)->bool:
        return (
            isinstance(other, genType) and
            self.math_form == other.math_form and
            self.shape == other.shape
        )

    def _op(self, operator:str, other:Union[float, bool, int, genType])->genType:
        second_has_negative:bool = False
        if operator == "**":
            second_has_negative = self.__has_negative(other)

        result_type = self._operator_type(operator, other, reverse=False, second_has_negative=second_has_negative)
        result:genType = result_type()
        other_is_homo:bool = self._is_homo(other)
        operator_func:Callable[[Any,Any], Any] = self._operator_funcs[operator]
        for i in range(len(result._data)):
            result._data[i] = operator_func(self._data[i], other._data[i] if other_is_homo else other)

        return result
    
    def _rop(self, operator:str, other:Union[float, bool, int, genType])->genType:
        second_has_negative:bool = False
        if operator == "**":
            second_has_negative = self.__has_negative(other)

        result_type = self._operator_type(operator, other, reverse=True, second_has_negative=second_has_negative)
        result:genType = result_type()
        operator_func:Callable[[Any,Any], Any] = self._operator_funcs[operator]
        for i in range(len(result._data)):
            result._data[i] = operator_func(other, self._data[i])

        return result
    
    def _iop(self, operator:str, other:Union[float, bool, int, genType])->genType:
        other_is_homo:bool = self._is_homo(other)
        if not other_is_homo and not is_number(other):
            raise TypeError(f"unsupported operand type(s) for {operator}=: '{self.__class__.__name__}' and '{other.__class__.__name__}'")
        
        operator_func:Callable[[Any,Any], Any] = self._operator_funcs[operator]
        for i in range(len(self._data)):
            self._data[i] = operator_func(self._data[i], other._data[i] if other_is_homo else other)

        self._update_data()

        return self
    
    def _compare_op(self, operator:str, other:Union[float, bool, int, genType])->genType:
        btype = self.gen_type(ctypes.c_bool, self.shape)
        result:genType = btype()

        other_is_homo:bool = self._is_homo(other)
        if not other_is_homo and not is_number(other):
            raise TypeError(f"unsupported operand type(s) for {operator}: '{self.__class__.__name__}' and '{other.__class__.__name__}'")
        
        operator_func:Callable[[Any,Any], Any] = self._operator_funcs[operator]
        for i in range(len(self._data)):
            result._data[i] = operator_func(self._data[i], other._data[i] if other_is_homo else other)
        
        return result
    
    def _compare_rop(self, operator:str, other:Union[float, bool, int, genType])->genType:
        btype = self.gen_type(ctypes.c_bool, self.shape)
        result:genType = btype()

        operator_func:Callable[[Any,Any], Any] = self._operator_funcs[operator]
        for i in range(len(result._data)):
            result._data[i] = operator_func(other, self._data[i])
        
        return result
    
    def __add__(self, other:Union[float, bool, int, genType])->genType:
        return self._op("+", other)
    
    def __radd__(self, other:Union[float, bool, int])->genType:
        return self._rop("+", other)
    
    def __iadd__(self, other:Union[float, bool, int, genType])->genType:
        return self._iop("+", other)

    def __sub__(self, other:Union[float, bool, int, genType])->genType:
        return self._op("-", other)
    
    def __rsub__(self, other:Union[float, bool, int])->genType:
        return self._rop("-", other)
    
    def __isub__(self, other:Union[float, bool, int, genType])->genType:
        return self._iop("-", other)

    def __mul__(self, other:Union[float, bool, int, genType])->genType:
        return self._op("*", other)
    
    def __rmul__(self, other:Union[float, bool, int])->genType:
        return self._rop("*", other)
    
    def __imul__(self, other:Union[float, bool, int, genType])->genType:
        return self._iop("*", other)

    def __truediv__(self, other:Union[float, bool, int, genType])->genType:
        return self._op("/", other)
    
    def __rtruediv__(self, other:Union[float, bool, int])->genType:
        return self._rop("/", other)
    
    def __itruediv__(self, other:Union[float, bool, int, genType]):
        return self._iop("/", other)

    def __floordiv__(self, other:Union[float, bool, int, genType])->genType:
        return self._op("//", other)
    
    def __rfloordiv__(self, other:Union[float, bool, int])->genType:
        return self._rop("//", other)
    
    def __ifloordiv__(self, other:Union[float, bool, int, genType]):
        return self._iop("//", other)

    def __mod__(self, other:Union[float, bool, int, genType])->genType:
        return self._op("%", other)
    
    def __rmod__(self, other:Union[float, bool, int])->genType:
        return self._rop("%", other)
    
    def __imod__(self, other:Union[float, bool, int, genType]):
        return self._iop("%", other)

    def __pow__(self, other:Union[float, bool, int, genType])->genType:
        return self._op("**", other)
    
    def __rpow__(self, other:Union[float, bool, int])->genType:
        return self._rop("**", other)
    
    def __ipow__(self, other:Union[float, bool, int, genType]):
        return self._iop("**", other)

    def __eq__(self, other:Union[float, bool, int, genType])->genType:
        return self._compare_op("==", other)
    
    def __req__(self, other:Union[float, bool, int, genType])->genType:
        return self._compare_rop("==", other)
    
    def __ne__(self, other:Union[float, bool, int, genType])->genType:
        return self._compare_op("!=", other)
    
    def __rne__(self, other:Union[float, bool, int, genType])->genType:
        return self._compare_rop("!=", other)
    
    def __gt__(self, other:Union[float, bool, int, genType])->genType:
        return self._compare_op(">", other)
    
    def __rgt__(self, other:Union[float, bool, int, genType])->genType:
        return self._compare_rop(">", other)
    
    def __lt__(self, other:Union[float, bool, int, genType])->genType:
        return self._compare_op("<", other)
    
    def __rlt__(self, other:Union[float, bool, int, genType])->genType:
        return self._compare_rop("<", other)
    
    def __ge__(self, other:Union[float, bool, int, genType])->genType:
        return self._compare_op(">=", other)
    
    def __rge__(self, other:Union[float, bool, int, genType])->genType:
        return self._compare_rop(">=", other)
    
    def __le__(self, other:Union[float, bool, int, genType])->genType:
        return self._compare_op("<=", other)
    
    def __rle__(self, other:Union[float, bool, int, genType])->genType:
        return self._compare_rop("<=", other)