import glm
import numpy as np

from .SphericalFSurf import SphericalFSurf
from ..ColorMap import ColorMap
from ..Mesh import Mesh
from glass.utils import checktype
from ..algorithm import spherical_harmonics_eval

class SphericalHarmonics(SphericalFSurf):

    @checktype
    def __init__(self, n:int, m:int, surf_type=Mesh.SurfType.Smooth,
                 color_map:ColorMap=None, back_color_map:ColorMap=None,
                 color:(glm.vec3,glm.vec4)=None, back_color:(glm.vec3,glm.vec4)=None,
                 name:str=""):
        
        def SH(lon, lat):
            theta = np.pi/2-lat
            phi = lon
            SH_value = spherical_harmonics_eval(n, m, theta, phi)
            if m > 0:
                return np.sqrt(2) * np.abs(SH_value.real)
            elif m < 0:
                return np.sqrt(2) * np.abs(SH_value.imag)
            else:
                return np.abs(SH_value.real)

        SphericalFSurf.__init__(self, SH, surf_type=surf_type,
                      color_map=color_map, back_color_map=back_color_map,
                      color=color, back_color=back_color,
                      name=name)