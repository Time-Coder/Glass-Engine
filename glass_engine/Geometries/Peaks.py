from ..Mesh import Mesh
from ..ColorMap import ColorMap

from .Surf import Surf

from glass.utils import checktype

import numpy as np
import glm

class Peaks(Surf):

    @checktype
    def __init__(self, x_range=[-3,3], y_range=[-3,3],
                 color_map:ColorMap=None, back_color_map:ColorMap=None,
                 color:(glm.vec3,glm.vec4)=None, back_color:(glm.vec3,glm.vec4)=None,
                 surf_type:Mesh.SurfType=Mesh.SurfType.Smooth,
                 name:str="", block:bool=True):
        X = np.linspace(x_range[0], x_range[1]) if len(x_range) == 2 else x_range
        Y = np.linspace(y_range[0], y_range[1]) if len(y_range) == 2 else y_range
        X, Y = np.meshgrid(X, Y)
        Z = 3*(1-X)**2 * np.exp(-(X**2) - (Y+1)**2) \
            - 10*(X/5 - X**3 - Y**5)*np.exp(-X**2-Y**2) \
            - 1/3*np.exp(-(X+1)**2 - Y**2)
        Surf.__init__(self, X, Y, Z/3,
                      color_map=color_map, back_color_map=back_color_map,
                      color=color, back_color=back_color,
                      surf_type=surf_type, name=name, block=block)