from __future__ import annotations

from .genType import genType, MathForm
from .genVec import genVec
from .genVec3 import genVec3
from .helper import is_number

from typing import Tuple, Any, Union
import math


class genQuat(genType):

    def __init__(self, *args):
        genType.__init__(self)
        self._data[0] = 1

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

            if not is_number(w) or not isinstance(v, genVec):
                raise TypeError(f"invalid argument type(s) for {self.__class__.__name__}()")
            
            self._data[0] = w
            self._data[1] = v._data[0]
            self._data[2] = v._data[1]
            self._data[3] = v._data[2]
            return

        if len(args) == 4:
            self._data[0] = args[0]
            self._data[1] = args[1]
            self._data[2] = args[2]
            self._data[3] = args[3]
            return

        raise ValueError(f"invalid arguments for {self.__class__.__name__}()")
            
    @property
    def math_form(self)->MathForm:
        return MathForm.Quat

    @property
    def w(self)->float:
        return self._data[0]
    
    @w.setter
    def w(self, w:float)->None:
        self._data[0] = w
        self._update_data()

    @property
    def x(self)->float:
        return self._data[1]
    
    @x.setter
    def x(self, x:float)->None:
        self._data[1] = x
        self._update_data()

    @property
    def y(self)->float:
        return self._data[2]
    
    @y.setter
    def y(self, y:float)->None:
        self._data[2] = y
        self._update_data()

    @property
    def z(self)->float:
        return self._data[3]
    
    @z.setter
    def z(self, z:float)->None:
        self._data[3] = z
        self._update_data()

    @property
    def xyz(self)->genVec3:
        vec_type = genVec.vec_type(self.dtype, 3)
        return vec_type(self._data[1], self._data[2], self._data[3])
    
    @xyz.setter
    def xyz(self, xyz:genVec3)->None:
        if not isinstance(xyz, genVec3):
            raise TypeError(f'must be genVec3, not {type(xyz)}')

        self._data[1] = xyz._data[0]
        self._data[2] = xyz._data[1]
        self._data[3] = xyz._data[2]
        self._update_data()

    @staticmethod
    def quat_type(dtype:type)->type:
        return genType.gen_type(MathForm.Quat, dtype, (4,))

    @property
    def shape(self)->Tuple[int]:
        return (4,)
    
    def __len__(self)->int:
        return 4
    
    def __getitem__(self, index:int)->float:
        return self._data[index]
    
    def __setitem__(self, index:Union[slice,int], value:Union[genQuat,float])->None:
        self._data[index] = value
        self._update_data()

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

            result_dtype = self._bin_op_dtype(operator, self.dtype, other.dtype, False)
            quat_type = self.quat_type(result_dtype)
            if isinstance(other, genQuat):
                result:genQuat = quat_type()
                result.w = self.w * other.w - self.x * other.x - self.y * other.y - self.z * other.z
                result.x = self.w * other.x + self.x * other.w + self.y * other.z - self.z * other.y
                result.y = self.w * other.y + self.y * other.w + self.z * other.x - self.x * other.z
                result.z = self.w * other.z + self.z * other.w + self.x * other.y - self.y * other.x
                return result
            else: # if isinstance(other, genVec):
                vec_quat:genQuat = quat_type(0, other)
                temp_quat:genQuat = self * vec_quat * quat_type(self.w, -self.xyz) / math.sqrt(self.w**2 + self.x**2 + self.y**2 + self.z**2)
                return temp_quat.xyz
        
        if isinstance(other, genType) and not isinstance(other, genQuat):
            raise TypeError(f"unsupported operand type(s) for {operator}: '{self.__class__.__name__}' and '{other.__class__.__name__}'")

        return genType._op(self, operator, other)

    def _iop(self, operator:str, other:Union[float, bool, int, genQuat])->genQuat:
        if operator == "**" or (operator in ["/", "//", "%"] and isinstance(other, genType)):
            raise TypeError(f"unsupported operand type(s) for {operator}=: '{self.__class__.__name__}' and '{other.__class__.__name__}'")

        if operator == "*" and isinstance(other, genType):
            if not isinstance(other, genQuat):
                raise TypeError(f"unsupported operand type(s) for {operator}: '{self.__class__.__name__}' and '{other.__class__.__name__}'")
            
            w = self.w * other.w - self.x * other.x - self.y * other.y - self.z * other.z
            x = self.w * other.x + self.x * other.w + self.y * other.z - self.z * other.y
            y = self.w * other.y + self.y * other.w + self.z * other.x - self.x * other.z
            z = self.w * other.z + self.z * other.w + self.x * other.y - self.y * other.x
            self.w = w
            self.x = x
            self.y = y
            self.z = z

            return self
        
        if isinstance(other, genType) and not isinstance(other, genQuat):
            raise TypeError(f"unsupported operand type(s) for {operator}=: '{self.__class__.__name__}' and '{other.__class__.__name__}'")

        return genType._iop(self, operator, other)
