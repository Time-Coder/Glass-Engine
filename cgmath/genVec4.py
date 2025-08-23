from typing import Optional, Union, List
from .genVec import genVec


class genVec4(genVec):

    namespaces:List[str] = ['xyzw', 'rgba', 'stpq']
    size:int = 4

    def __init__(self, x:Optional[Union[float, bool, int, genVec]]=None, y:Optional[Union[float, bool, int, genVec]]=None, z:Optional[float]=None, w:Optional[float]=None):
        genVec.__init__(self)

        if x is None and y is None and z is None and w is None:
            return
        
        if y is None and z is None and w is None:
            if isinstance(x, (bool, int, float)):
                self._data[0] = self.dtype(x)
                self._data[1] = self.dtype(x)
                self._data[2] = self.dtype(x)
                self._data[3] = self.dtype(x)
            elif isinstance(x, genVec) and x.size >= 3:
                self._data[0] = self.dtype(x[0])
                self._data[1] = self.dtype(x[1])
                self._data[2] = self.dtype(x[2])
                self._data[3] = self.dtype(x[3])
            else:
                raise TypeError(f"invalid argument type(s) for {self.__class__.__name__}()")
            
            return
        
        if z is None and w is None:
            if isinstance(x, (bool, int, float)) and isinstance(y, genVec) and y.size == 3:
                self._data[0] = self.dtype(x)
                self._data[1] = self.dtype(y[0])
                self._data[2] = self.dtype(y[1])
                self._data[3] = self.dtype(y[2])
            elif isinstance(x, genVec) and x.size == 3 and isinstance(y, (bool, int, float)):
                self._data[0] = self.dtype(x[0])
                self._data[1] = self.dtype(x[1])
                self._data[2] = self.dtype(x[2])
                self._data[3] = self.dtype(y)
            elif isinstance(x, genVec) and x.size == 2 and isinstance(y, genVec) and y.size == 2:
                self._data[0] = self.dtype(x[0])
                self._data[1] = self.dtype(x[1])
                self._data[2] = self.dtype(y[0])
                self._data[3] = self.dtype(y[1])
            else:
                raise TypeError(f"invalid argument type(s) for {self.__class__.__name__}()")
            
            return
        
        if w is None:
            if isinstance(x, (bool, int, float)) and isinstance(y, (bool, int, float)) and isinstance(z, genVec) and z.size == 2:
                self._data[0] = self.dtype(x)
                self._data[1] = self.dtype(y)
                self._data[2] = self.dtype(z[0])
                self._data[3] = self.dtype(z[1])
            elif isinstance(x, (bool, int, float)) and isinstance(y, genVec) and y.size == 2 and isinstance(z, (bool, int, float)):
                self._data[0] = self.dtype(x)
                self._data[1] = self.dtype(y[0])
                self._data[2] = self.dtype(y[1])
                self._data[3] = self.dtype(z)
            elif isinstance(x, genVec) and x.size == 2 and isinstance(y, (bool, int, float)) and isinstance(z, (bool, int, float)):
                self._data[0] = self.dtype(x[0])
                self._data[1] = self.dtype(x[1])
                self._data[2] = self.dtype(y)
                self._data[3] = self.dtype(z)
            else:
                raise TypeError(f"invalid argument type(s) for {self.__class__.__name__}()")
            
            return

        self._data[0] = self.dtype(x)
        self._data[1] = self.dtype(y)
        self._data[2] = self.dtype(z)
        self._data[3] = self.dtype(w)
