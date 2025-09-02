from __future__ import annotations

from typing import Tuple, Union, Any
from .genVec import genVec
from .genType import genType, MathForm
from .helper import is_number


class genMatIterator:

    def __init__(self, mat:genMat):
        self.__mat:genMat = mat
        self.__current_index:int = 0

    def __next__(self)->genVec:
        if self.__current_index >= self.__mat.cols:
            raise StopIteration()

        result = self.__mat[self.__current_index]
        self.__current_index += 1
        return result

class genMat(genType):

    def __init__(self, *args):
        genType.__init__(self)
        n:int = min(self.rows, self.cols)
        for i in range(n):
            self[i, i] = 1

        i: int = 0
        n_data: int = len(self._data)
        n_args: int = len(args)

        if n_args == 0:
            return
        
        if n_args == 1:
            arg = args[0]
            if is_number(arg):
                for i in range(n):
                    self[i, i] = arg
                return
            
            if isinstance(arg, genMat):
                for i in range(self.rows):
                    for j in range(self.cols):
                        self[j, i] = arg[j, i]
                return
        
        for i_arg, arg in enumerate(args):
            if is_number(arg):
                self._data[i] = arg

                i += 1
                if i == n_data:
                    if n_args != 1 and i_arg != n_args - 1:
                        raise ValueError(f"invalid arguments for {self.__class__.__name__}()")
                    
                    return

            elif isinstance(arg, genVec):
                sub_n_arg: int = len(arg._data)
                for sub_i_arg, value in enumerate(arg._data):
                    self._data[i] = value

                    i += 1
                    if i == n_data:
                        if n_args != 1 and (i_arg != n_args - 1 or sub_i_arg != sub_n_arg - 1):
                            raise ValueError(f"invalid arguments for {self.__class__.__name__}()")
                        
                        return
            
            else:
                raise TypeError(f"invalid argument type(s) for {self.__class__.__name__}()")
            
        raise ValueError(f"invalid arguments for {self.__class__.__name__}()")

    @property
    def math_form(self)->MathForm:
        return MathForm.Mat

    @property
    def rows(self)->int:
        return self.shape[1]
    
    @property
    def cols(self)->int:
        return self.shape[0]
    
    @staticmethod
    def mat_type(dtype:type, shape:Tuple[int]):
        return genType.gen_type(MathForm.Mat, dtype, shape)
    
    def __getitem__(self, index:Union[int,Tuple[int]])->Union[int,bool,float,genVec]:
        if isinstance(index, int):
            result_type = genVec.vec_type(self.dtype, self.rows)
            result:genVec = result_type(*self._data[self.rows * index : self.rows * (index + 1)])
            result._mat_start_index = self.rows * index
            result._related_mat = self
            return result
        elif isinstance(index, tuple):
            return self._data[index[0]*self.rows + index[1]]
    
    def __setitem__(self, index:Union[int,Tuple[int]], value:Union[float,int,bool,genVec])->None:
        if isinstance(index, int):
            for i in range(self.rows):
                self._data[self.rows*index + i] = value[i]
        elif isinstance(index, tuple):
            self._data[index[0]*self.rows + index[1]] = value

    def __iter__(self)->genMatIterator:
        return genMatIterator(self)
    
    def __contains__(self, value:Any)->bool:
        if is_number(value):
            return value in self._data
        elif isinstance(value, genVec) and len(value) == self.rows:
            for i in range(self.cols):
                if self[i] == value:
                    return True
                
        return False

    def _op(self, operator:str, other:Union[float, bool, int, genMat, genVec])->Union[genMat, genVec]:
        if operator == "**" or (operator in ["/", "//", "%"] and isinstance(other, genType)):
            raise TypeError(f"unsupported operand type(s) for {operator}: '{self.__class__.__name__}' and '{other.__class__.__name__}'")
        
        if operator == "*" and isinstance(other, genType):
            if not isinstance(other, (genMat, genVec)) or self.cols != (other.rows if isinstance(other, genMat) else len(other)):
                raise TypeError(f"unsupported operand type(s) for {operator}: '{self.__class__.__name__}' and '{other.__class__.__name__}'")
            
            result_dtype = self._bin_op_dtype(operator, self.dtype, other.dtype, False)
            result_shape = (self.rows, other.cols) if isinstance(other, genMat) else (self.rows,)
            result_type = self.gen_type(other.math_form, result_dtype, result_shape)
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

        return genType._op(self, operator, other)

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
            
        return genType._iop(self, operator, other)