from __future__ import annotations

from .genType import genType
from .genVec import genVec
from .helper import from_import

from typing import Tuple, Any, Union, Dict
import ctypes


class genQuat(genType):

    __gen_quat_map:Dict[type, type] = {}

    def __init__(self, *args):
        genType.__init__(self)
        self._data = (self.dtype * 4)(1, 0, 0, 0)

        if len(args) == 0:
            return

        if len(args) == 1:
            arg = args[0]
            if not isinstance(arg, genQuat):
                raise TypeError(f"invalid argument type(s) for {self.__class__.__name__}()")
            
            self._data[0] = arg._data[0]
            self._data[1] = arg._data[1]
            self._data[2] = arg._data[2]
            self._data[3] = arg._data[3]
            return
        
        if len(args) == 2:
            w = args[0]
            v = args[1]

            if not isinstance(w, (float,int,bool)) or not isinstance(v, genVec):
                raise TypeError(f"invalid argument type(s) for {self.__class__.__name__}()")
            
            self._data[0] = w
            self._data[1] = v._data[0]
            self._data[2] = v._data[1]
            self._data[3] = v._data[2]

        if len(args) == 4:
            self._data[0] = args[0]
            self._data[1] = args[1]
            self._data[2] = args[2]
            self._data[3] = args[3]

        raise ValueError(f"invalid arguments for {self.__class__.__name__}()")
            
    @property
    def quat_type(dtype:type)->type:
        if dtype not in genQuat.__gen_quat_map:
            if dtype == ctypes.c_float:
                genQuat.__gen_quat_map[dtype] = from_import(".quat", "quat")
            elif dtype == ctypes.c_double:
                genQuat.__gen_quat_map[dtype] = from_import(".dquat", "dquat")

        return genQuat.__gen_quat_map[dtype]

    @property
    def shape(self)->Tuple[int]:
        return (4,)
    
    def __len__(self)->int:
        return 4
    
    def __getitem__(self, index:int)->float:
        return self._data[index]
    
    def __setitem__(self, index:int, value:float)->None:
        self._data[index] = value

    def __iter__(self):
        return iter(self._data)
    
    def __contains__(self, value:Any)->bool:
        return (value in self._data)
    
    def _op(self, operator:str, other:Union[float, bool, int, genQuat, genVec])->Union[genQuat, genVec]:
        if operator == "**" or (operator in ["/", "//", "%"] and isinstance(other, genType)):
            raise TypeError(f"unsupported operand type(s) for {operator}: '{self.__class__.__name__}' and '{other.__class__.__name__}'")
        
        if operator == "*" and isinstance(other, genType):
            if not isinstance(other, (genQuat, genVec)):
                raise TypeError(f"unsupported operand type(s) for {operator}: '{self.__class__.__name__}' and '{other.__class__.__name__}'")
            
            if isinstance(other, genVec) and len(other) != 3:
                raise TypeError(f"unsupported operand type(s) for {operator}: '{self.__class__.__name__}' and '{other.__class__.__name__}'")

            result_dtype = self._operator_dtype(self.dtype, operator, other.dtype)
            result_shape = (self.rows, other.cols) if isinstance(other, genMat) else (self.rows,)
            result_type = self.gen_type(result_dtype, result_shape)
            result = result_type()
            if isinstance(result, genMat):
                for i in range(result.rows):
                    for j in range(result.cols):
                        value = 0
                        for k in range(self.cols):
                            value += self[k, i] * other[j, k]

                        result[j, i] = value
            elif isinstance(result, genVec):
                for i in range(len(result)):
                    value = 0
                    for k in range(self.cols):
                        value += self[k, i] * other[k]

                    result._data[i] = value

            return result

        return genType._op(operator, other)

    def _iop(self, operator:str, other:Union[float, bool, int, genMat])->genMat:
        if operator == "**" or (operator in ["/", "//", "%"] and isinstance(other, genType)):
            raise TypeError(f"unsupported operand type(s) for {operator}=: '{self.__class__.__name__}' and '{other.__class__.__name__}'")

        if operator == "*" and isinstance(other, genType):
            if not isinstance(other, genMat):
                raise TypeError(f"unsupported operand type(s) for {operator}=: '{self.__class__.__name__}' and '{other.__class__.__name__}'")
            
            if self.cols != other.rows or other.rows != other.cols:
                raise TypeError(f"unsupported operand type(s) for {operator}=: '{self.__class__.__name__}' and '{other.__class__.__name__}'")

            result:genMat = self * other
            self._data[:] = result._data[:]
            self._update_data()
            return self
            
        return genType._iop(operator, other)