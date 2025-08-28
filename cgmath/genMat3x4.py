from typing import Tuple
from .genMat import genMat


class genMat3x4(genMat):

    @property
    def shape(self)->Tuple[int]:
        return (3, 4)