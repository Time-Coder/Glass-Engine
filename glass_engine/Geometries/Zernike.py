import glm
from functools import partial

from .CylindricalFSurf import CylindricalFSurf
from ..ColorMap import ColorMap
from ..Mesh import Mesh
from glass.utils import checktype
from ..algorithm import Zernike_eval

class Zernike(CylindricalFSurf):

    @checktype
    def __init__(self, n:int, m:int, surf_type:Mesh.SurfType=Mesh.SurfType.Smooth,
                 color_map:ColorMap=None, back_color_map:ColorMap=None,
                 color:(glm.vec3,glm.vec4)=None, back_color:(glm.vec3,glm.vec4)=None,
                 name:str=""):
        CylindricalFSurf.__init__(self, partial(Zernike_eval, n, m), r_range=[0,1],
                      color_map=color_map, back_color_map=back_color_map, surf_type=surf_type,
                      color=color, back_color=back_color,
                      name=name)