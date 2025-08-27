from __future__ import annotations

from typing import Optional, Union, List
from .genVec import genVec


class genVec2(genVec):

    namespaces:List[str] = ['xy', 'rg', 'st']

    def __init__(self, x:Optional[Union[float, bool, int, genVec]]=None, y:Optional[float]=None):
        genVec.__init__(self)

        if x is None and y is None:
            return
        
        if y is None:
            if isinstance(x, (bool, int, float)):
                self._data[0] = self.dtype(x)
                self._data[1] = self.dtype(x)
            elif isinstance(x, genVec):
                self._data[0] = self.dtype(x[0])
                self._data[1] = self.dtype(x[1])
            else:
                raise TypeError(f"invalid argument type(s) for {self.__class__.__name__}()")
            
            return
        
        self._data[0] = self.dtype(x)
        self._data[1] = self.dtype(y)

    def __len__(self)->int:
        return 2