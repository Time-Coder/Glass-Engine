from typing import Optional, Union, List
from .genVec import genVec
import ctypes


class genVec3(genVec):

    namespaces:List[str] = ['xyz', 'rgb', 'stp']

    def __init__(self, x:Optional[Union[float, bool, int, genVec]]=None, y:Optional[float]=None, z:Optional[float]=None):
        genVec.__init__(self)

        if x is None and y is None and z is None:
            return
        
        if y is None and z is None:
            if isinstance(x, (bool, int, float)):
                self._data[0] = self.dtype(x)
                self._data[1] = self.dtype(x)
                self._data[2] = self.dtype(x)
            elif isinstance(x, genVec) and x.size >= 3:
                self._data[0] = self.dtype(x[0])
                self._data[1] = self.dtype(x[1])
                self._data[2] = self.dtype(x[2])
            else:
                raise TypeError(f"invalid argument type(s) for {self.__class__.__name__}()")
            
            return
        
        if z is None:
            if isinstance(x, (bool, int, float)) and isinstance(y, genVec) and y.size == 2:
                self._data[0] = self.dtype(x)
                self._data[1] = self.dtype(y[0])
                self._data[2] = self.dtype(y[1])
            elif isinstance(x, genVec) and x.size == 2 and isinstance(y, (bool, int, float)):
                self._data[0] = self.dtype(x[0])
                self._data[1] = self.dtype(x[1])
                self._data[2] = self.dtype(y)
            else:
                raise TypeError(f"invalid argument type(s) for {self.__class__.__name__}()")
            
            return

        self._data[0] = self.dtype(x)
        self._data[1] = self.dtype(y)
        self._data[2] = self.dtype(z)

    def __len__(self)->int:
        return 3