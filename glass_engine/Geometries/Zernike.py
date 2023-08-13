import glm
from functools import partial

from .CylindricalFSurf import CylindricalFSurf
from ..ColorMap import ColorMap
from glass.utils import checktype
from ..algorithm import Zernike_eval

class Zernike(CylindricalFSurf):

    @checktype
    def __init__(self, n:int, m:int,
                 color_map:ColorMap=None, back_color_map:ColorMap=None,
                 color:(glm.vec3,glm.vec4)=None, back_color:(glm.vec3,glm.vec4)=None,
                 name:str="", block:bool=True):
        CylindricalFSurf.__init__(self, partial(Zernike_eval, n, m), r_range=[0,1],
                      color_map=color_map, back_color_map=back_color_map,
                      color=color, back_color=back_color,
                      name=name, block=block)