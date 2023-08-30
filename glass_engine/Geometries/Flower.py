from ..Mesh import Mesh
from ..ColorMap import ColorMap

from .Surf import Surf

from glass.utils import checktype

import numpy as np
import glm

class Flower(Surf):

    @checktype
    def __init__(self, color_map:ColorMap=None, back_color_map:ColorMap=None,
                 color:(glm.vec3,glm.vec4)=None, back_color:(glm.vec3,glm.vec4)=None,
                 surf_type:Mesh.SurfType=Mesh.SurfType.Smooth, name:str=""):
        x, t = np.meshgrid(np.linspace(0, 1, 25), np.linspace(0, 1, 500)*17*np.pi-2*np.pi)
        p=(np.pi/2)*np.exp(-t/(8*np.pi))
        u=1-(1-np.mod(3.6*t,2*np.pi)/np.pi)**4/2
        y=2*(x**2-x)**2*np.sin(p)
        r=u*(x*np.sin(p)+y*np.cos(p))

        X = r*np.cos(t)
        Y = r*np.sin(t)
        Z = u*(x*np.cos(p)-y*np.sin(p))+0.5
        Surf.__init__(self, X, Y, 0.8*Z, r,
                      color_map=color_map, back_color_map=back_color_map,
                      color=color, back_color=back_color,
                      surf_type=surf_type, name=name)