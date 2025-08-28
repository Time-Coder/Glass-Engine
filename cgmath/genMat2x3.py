from typing import Tuple
from .genMat import genMat


class genMat2x3(genMat):

    @property
    def shape(self)->Tuple[int]:
        return (2, 3)