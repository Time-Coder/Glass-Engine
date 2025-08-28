from __future__ import annotations

from typing import Optional, Union, Tuple
from .genMat import genMat
from .genType import genType
from .genVec import genVec


class genMat2x2(genMat):

    def __init__(self,
        m00:Optional[Union[float, bool, int, genType]]=None,
        m01:Optional[Union[float, bool, int, genVec]]=None,
        
        m10:Optional[Union[float, bool, int, genVec]]=None,
        m11:Optional[float]=None,
    ):
        genMat.__init__(self)

        if m00 is None and m01 is None and m10 is None and m11 is None:
            return

        if (
            isinstance(m00, (float,int,bool)) and
            isinstance(m01, (float,int,bool)) and
            isinstance(m10, (float,int,bool)) and
            isinstance(m11, (float,int,bool))
        ):
            self._data[0] = m00
            self._data[1] = m01
            self._data[2] = m10
            self._data[3] = m11
            return
        
        if (
            isinstance(m00, genMat) and
            m01 is None and m10 is None and m11 is None
        ):
            for i in range(self.rows):
                for j in range(self.cols):
                    self[j, i] = m00[j, i]

            return
        
        if (
            isinstance(m00, (float,bool,int)) and
            m01 is None and m10 is None and m11 is None
        ):
            self._data[0] = m00
            self._data[1] = m00
            self._data[2] = m00
            self._data[3] = m00
        
        if (
            isinstance(m00, genVec) and len(m00) == 2 and
            isinstance(m01, genVec) and len(m01) == 2 and
            m10 is None and m11 is None
        ):
            self._data[0] = m00._data[0]
            self._data[1] = m00._data[1]
            self._data[2] = m01._data[0]
            self._data[3] = m01._data[1]
            return
        
        if (
            isinstance(m00, genVec) and len(m00) == 2 and 
            isinstance(m01, (float, bool, int)) and
            isinstance(m10, (float, bool, int)) and
            m11 is None
        ):
            self._data[0] = m00._data[0]
            self._data[1] = m00._data[1]
            self._data[2] = m01
            self._data[3] = m10
            return

        if (
            isinstance(m00, (float, bool, int)) and
            isinstance(m01, (float, bool, int)) and
            isinstance(m10, genVec) and len(m10) == 2 and 
            m11 is None
        ):
            self._data[0] = m00
            self._data[1] = m01
            self._data[2] = m10._data[0]
            self._data[3] = m10._data[1]
            return

        raise TypeError(f"invalid argument type(s) for {self.__class__.__name__}()")

    @property
    def shape(self)->Tuple[int]:
        return (2, 2)