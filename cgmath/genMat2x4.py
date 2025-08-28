from typing import Tuple
from .genMat import genMat


class genMat2x4(genMat):

    @property
    def shape(self)->Tuple[int]:
        return (2, 4)