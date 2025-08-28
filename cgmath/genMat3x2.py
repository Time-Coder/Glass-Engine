from typing import Tuple
from .genMat import genMat


class genMat3x2(genMat):

    @property
    def shape(self)->Tuple[int]:
        return (3, 2)