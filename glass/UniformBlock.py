from .Block import Block
from .UBO import UBO


class UniformBlock(Block):

    BO = UBO

    def __init__(self, shader_program):
        Block.__init__(self, shader_program)
