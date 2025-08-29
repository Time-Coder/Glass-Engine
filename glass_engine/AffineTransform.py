import cgmath as cgm
from glass import Instance


class AffineTransform(Instance):
    def __init__(self):
        Instance.__init__(self)

        self["affine_transform_row0"] = cgm.vec4(1, 0, 0, 0)
        self["affine_transform_row1"] = cgm.vec4(0, 1, 0, 0)
        self["affine_transform_row2"] = cgm.vec4(0, 0, 1, 0)
        self["env_map_handle"] = 0
        self["visible"] = 1

    def apply(self, pos):
        transform_mat = cgm.mat4(
            self["affine_transform_row0"],
            self["affine_transform_row1"],
            self["affine_transform_row2"],
            cgm.vec4(0, 0, 0, 1),
        )
        transform_mat = cgm.transpose(transform_mat)
        result = transform_mat * cgm.vec4(*pos, 1)
        return result.xyz
