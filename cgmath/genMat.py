from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Set, List, Dict, Tuple, Union, Any
import ctypes

from .genVec import genVec


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

class genMat(ABC):

    def __init__(self):
        self._data = (self.dtype * (self.rows * self.cols))()

    @property
    @abstractmethod
    def dtype(self)->type:
        pass
    
    @property
    @abstractmethod
    def rows(self)->int:
        pass

    @property
    @abstractmethod
    def cols(self)->int:
        pass

    @property
    def shape(self)->Tuple[int]:
        return (self.rows, self.cols)

    def value_ptr(self):
        return self._data
    
    def __getitem__(self, index:Union[int,Tuple[int]])->Union[int,bool,float,genVec]:
        if isinstance(index, int):
            result_type = genVec._vec_type(self.dtype, self.rows)
            return result_type(*self._data[self.rows*index : self.rows*(index + 1)])
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
        if isinstance(value, (float,int,bool)):
            return value in self._data
        elif isinstance(value, genVec) and len(value) == self.rows:
            for i in range(self.cols):
                if self[i] == value:
                    return True
                
        return False

    def __repr__(self)->str:
        value_strs = []
        for i in range(len(self)):
            value_strs.append(str(self[i]))

        return f"{self.__class__.__name__}({', '.join(value_strs)})"