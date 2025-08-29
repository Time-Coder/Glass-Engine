from .Cylinder import Cylinder
from .Cone import Cone
from ..SceneNode import SceneNode

from typing import Union

import cgmath as cgm


class CoordSys(SceneNode):

    def __init__(
        self,
        x_length: float = 1,
        y_length: Union[float, None] = None,
        z_length: Union[float, None] = None,
        alpha: float = 1,
        name: str = "",
    ):
        SceneNode.__init__(self, name=name)

        if y_length is None:
            y_length = x_length

        if z_length is None:
            z_length = x_length

        x_axis = CoordSys.create_axis(x_length, cgm.vec4(1, 0, 0, alpha))
        x_axis.roll = 90
        self.add_child(x_axis)

        y_axis = CoordSys.create_axis(y_length, cgm.vec4(0, 1, 0, alpha))
        y_axis.pitch = -90
        self.add_child(y_axis)

        z_axis = CoordSys.create_axis(z_length, cgm.vec4(0, 0, 1, alpha))
        self.add_child(z_axis)

    @staticmethod
    def create_axis(length: float, color: cgm.vec4):
        axis = Cylinder(0.015, length, color=color)
        arrow = Cone(0.04, 0.15, color=color)
        arrow.position.z = length
        axis.add_child(arrow)

        return axis
