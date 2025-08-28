from typing import Tuple
from .genMat import genMat


class genMat4x3(genMat):

    @property
    def shape(self)->Tuple[int]:
        return (4, 3)