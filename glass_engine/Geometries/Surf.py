from ..Mesh import Mesh
from ..ColorMap import ColorMap

from glass.utils import checktype
from glass import AttrList

import glm
import numpy as np
import copy

class Surf(Mesh):
    @checktype
    def __init__(self, X:np.ndarray, Y:np.ndarray, Z:np.ndarray,
                 C:np.ndarray=None, back_C:np.ndarray=None,
                 color_map:ColorMap=None, back_color_map:ColorMap=None, 
                 color:(glm.vec3,glm.vec4)=None, back_color:(glm.vec3,glm.vec4)=None,
                 surf_type:Mesh.SurfType=Mesh.SurfType.Smooth, name=""):
        Mesh.__init__(self, name=name, surf_type=surf_type)
        self._XData = X
        self._YData = Y
        self._ZData = Z
        self._CData = C if C is not None else Z

        self._back_CData_user_set = (back_C is not None)
        self._back_CData = back_C if self._back_CData_user_set else self._CData

        Surf._set_colors(self, color, back_color, color_map, back_color_map)
        self.start_building()

    @staticmethod
    def _set_colors(obj, color, back_color, color_map, back_color_map):
        obj._use_color_map = (color is None)
        if color_map is None:
            color_map = ColorMap.parula()

        if color is not None:
            obj.color = color

        if back_color is None:
            back_color = color

        obj._color_map = color_map
        obj._back_color_map_user_set = (back_color_map is not None)
        obj._back_use_color_map = (back_color is None or back_color_map is not None)
        if back_color_map is None:
            back_color_map = copy.deepcopy(color_map)

        if back_color is not None:
            obj.back_color = back_color

        obj._back_color_map = back_color_map

    @staticmethod
    def _build(obj, X, Y, Z, C, back_C):
        obj.should_add_color = False
        rows = X.shape[0]
        cols = X.shape[1]
        color_map = obj._color_map
        back_color_map = obj._back_color_map
        use_color_map = obj._use_color_map
        back_use_color_map = obj._back_use_color_map
        color = obj._color
        back_color = obj._back_color

        xx = X.flatten()
        yy = Y.flatten()
        zz = Z.flatten()
        pos = np.vstack((xx, yy, zz))
        pos = pos.transpose().astype(np.float32)
        it_vertex = np.arange(0, len(xx), dtype=np.uint32)
        jj = it_vertex % cols
        ii = it_vertex // cols
        tt = 1 - ii/(rows - 1)
        ss = jj/(cols - 1)
        tex_coords = np.vstack((ss, tt, np.zeros_like(ss))).transpose().astype(np.float32)
        colors = None
        if use_color_map:
            if len(C.shape) == 2 or C.shape[2] == 1:
                if not color_map.range_user_set:
                    color_map.range = (C.min(), C.max())
                colors = color_map(C).flatten().reshape(len(xx), 4)
            else:
                if C.shape[2] == 4:
                    colors = C.flatten().reshape(len(xx), 4)
                else:
                    colors = np.insert(C, 3, np.ones(C.shape[:2], dtype=np.float32), axis=2).flatten().reshape(len(xx), 4)
        else:
            colors = np.tile([color.r, color.g, color.b, color.a], len(xx)).reshape(len(xx), 4)
        colors = colors.astype(np.float32)

        back_colors = None
        if back_use_color_map:
            if len(back_C.shape) == 2 or back_C.shape[2] == 1:
                if not back_color_map.range_user_set:
                    back_color_map.range = (back_C.min(), back_C.max())
                back_colors = back_color_map(back_C).flatten().reshape(len(xx), 4)
            else:
                if back_C.shape[2] == 4:
                    back_colors = back_C.flatten().reshape(len(xx), 4)
                else:
                    back_colors = np.insert(back_C, 3, np.ones(back_C.shape[:2], dtype=np.float32), axis=2).flatten().reshape(len(xx), 4)
        else:
            back_colors = np.tile([back_color.r, back_color.g, back_color.b, back_color.a], len(xx)).reshape(len(xx), 4)
        back_colors = back_colors.astype(np.float32)

        obj.vertices.reset(
            position=AttrList.fromarray(pos, glm.vec3),
            tangent=AttrList.fromarray(np.zeros_like(pos), glm.vec3),
            bitangent=AttrList.fromarray(np.zeros_like(pos), glm.vec3),
            normal=AttrList.fromarray(np.zeros_like(pos), glm.vec3),
            tex_coord=AttrList.fromarray(tex_coords, glm.vec3),
            color=AttrList.fromarray(colors, glm.vec4),
            back_color=AttrList.fromarray(back_colors, glm.vec4)
        )

        it_vertex = it_vertex[(ii != 0) & (jj != 0)]
        indices0 = it_vertex
        indices1 = it_vertex - 1
        indices2 = it_vertex - 1 - cols
        indices3 = it_vertex
        indices4 = it_vertex - 1 - cols
        indices5 = it_vertex - cols
        indices_mat = np.vstack((indices0, indices1, indices2, indices3, indices4, indices5))
        indices_mat = indices_mat.transpose().reshape(-1, 3)
        obj.indices.reset(indices_mat, dtype=glm.uvec3)

    def build(self):
        X = self._XData
        Y = self._YData
        Z = self._ZData
        C = self._CData if self._CData is not None else Z
        back_C = self._back_CData if self._back_CData is not None else C
        Surf._build(self, X, Y, Z, C, back_C)

    @property
    def XData(self):
        return self._XData
    
    @XData.setter
    @Mesh.param_setter
    def XData(self, X:np.ndarray):
        self._XData = X
    
    @property
    def YData(self):
        return self._YData
    
    @YData.setter
    @Mesh.param_setter
    def YData(self, Y:np.ndarray):
        self._YData = Y
    
    @property
    def ZData(self):
        return self._ZData
    
    @ZData.setter
    @Mesh.param_setter
    def ZData(self, Z:np.ndarray):
        self._ZData = Z
    
    @property
    def CData(self):
        return self._CData
    
    @CData.setter
    @Mesh.param_setter
    def CData(self, C:np.ndarray):
        self._CData = C
        self._use_color_map = True
        if not self._back_CData_user_set:
            self._back_CData = C
            self._back_use_color_map = True

    @property
    def back_CData(self):
        return self._back_CData
    
    @back_CData.setter
    @Mesh.param_setter
    def back_CData(self, C:np.ndarray):
        self._back_CData = C
        self._back_CData_user_set = True
        self._back_use_color_map = True
    
    @property
    def color_map(self):
        return self._color_map
    
    @color_map.setter
    @Mesh.param_setter
    def color_map(self, color_map:ColorMap):
        self._color_map = color_map
        self._use_color_map = True
        if not self._back_color_map_user_set:
            self._back_color_map = color_map
            self._back_use_color_map = True

    @property
    def back_color_map(self):
        return self._back_color_map
    
    @back_color_map.setter
    @Mesh.param_setter
    def back_color_map(self, color_map:ColorMap):
        self._back_color_map = color_map
        self._back_use_color_map = True
        self._back_color_map_user_set = True
