from typing import Tuple
from .genMat import genMat


class genMat4x4(genMat):

    @property
    def shape(self)->Tuple[int]:
        return (4, 4)
    
genMat4 = genMat4x4