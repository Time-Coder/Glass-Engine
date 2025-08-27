from __future__ import annotations

from typing import Optional, Union, Tuple
from .genMat import genMat
from .genType import genType


class genMat2x2(genMat):

    def __init__(self,
        m00:Optional[Union[float, bool, int, genType]]=None,
        m01:Optional[float]=None,
        
        m10:Optional[float]=None,
        m11:Optional[float]=None,
    ):
        genMat.__init__(self)

    @property
    def shape(self)->Tuple[int]:
        return (2, 2)