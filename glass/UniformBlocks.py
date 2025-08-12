from .Blocks import Blocks
from .UBO import UBO


class UniformBlocks(Blocks):

    BO = UBO

    def __init__(self, shader_program):
        Blocks.__init__(self, shader_program)
