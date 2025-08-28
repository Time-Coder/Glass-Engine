from typing import Tuple
from .genMat import genMat


class genMat4x2(genMat):

    @property
    def shape(self)->Tuple[int]:
        return (4, 2)