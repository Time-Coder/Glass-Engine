from .Block import Block
from .SSBO import SSBO


class ShaderStorageBlock(Block):

    BO = SSBO

    def __init__(self, program):
        Block.__init__(self, program)
