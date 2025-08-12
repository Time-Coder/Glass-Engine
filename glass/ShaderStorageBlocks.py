from .Blocks import Blocks
from .SSBO import SSBO


class ShaderStorageBlocks(Blocks):

    BO = SSBO

    def __init__(self, program):
        Blocks.__init__(self, program)
        self.shader_storage_blocks_info = {}
