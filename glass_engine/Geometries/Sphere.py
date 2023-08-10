from ..Mesh import Mesh

from glass.utils import checktype
from glass import Vertex

import glm
import math

class Sphere(Mesh):

    @checktype
    def __init__(self, radius:float=1,
                 color:(glm.vec3,glm.vec4)=glm.vec4(0.396, 0.74151, 0.69102, 1), back_color:(glm.vec3,glm.vec4)=None,
                 n_lon_divide:int=100, start_lon:float=0, span_lon:float=360,
                 n_lat_divide:int=50, start_lat:float=-90, span_lat:float=180,
                 name:str="", block=True):
        Mesh.__init__(self, color=color, back_color=back_color, name=name, block=block)
        self.__radius = radius
        self.__start_lon = start_lon
        self.__span_lon = span_lon
        self.__n_lon_divide = n_lon_divide
        self.__start_lat = start_lat
        self.__span_lat = span_lat
        self.__n_lat_divide = n_lat_divide
        self.start_building()

    def build(self):
        self.is_closed = True
        self.self_calculated_normal = True

        vertices = self.vertices
        indices = self.indices
        radius = self.__radius
        start_lon = self.__start_lon/180*math.pi
        span_lon = self.__span_lon/180*math.pi
        n_lon_divide = self.__n_lon_divide
        start_lat = self.__start_lat/180*math.pi
        span_lat = self.__span_lat/180*math.pi
        n_lat_divide = self.__n_lat_divide

        i_vertex = 0
        i_index = 0

        for i in range(n_lon_divide):
            theta = start_lon + span_lon*i/(n_lon_divide - 1)
            s = theta/(2*math.pi)
            cos_theta = math.cos(theta)
            sin_theta = math.sin(theta)

            for j in range(n_lat_divide):
                phi = start_lat + span_lat*j/(n_lat_divide-1)
                t = phi/math.pi + 0.5
                cos_phi = math.cos(phi)
                sin_phi = math.sin(phi)

                vertex = Vertex()

                vertex.tangent = 2*math.pi*radius*cos_phi*glm.vec3(-sin_theta, cos_theta, 0)
                vertex.bitangent = math.pi*radius*glm.vec3(-sin_phi*cos_theta, -sin_phi*sin_theta, cos_phi)
                vertex.normal = glm.vec3(cos_phi*cos_theta, cos_phi*sin_theta, sin_phi)
                vertex.position = radius * vertex.normal
                vertex.tex_coord = glm.vec3(s, t, 0)

                vertices[i_vertex] = vertex
                i_vertex += 1

                if i > 0 and j > 0:
                    triangle = glm.uvec3(0, 0, 0)
                    triangle[0] = i_vertex-1
                    triangle[1] = i_vertex-1-n_lat_divide
                    triangle[2] = i_vertex-1-n_lat_divide-1
                    indices[i_index] = triangle
                    i_index += 1

                    triangle = glm.uvec3(0, 0, 0)
                    triangle[0] = i_vertex-1
                    triangle[1] = i_vertex-1-n_lat_divide-1
                    triangle[2] = i_vertex-1-1
                    indices[i_index] = triangle
                    i_index += 1

                    yield
        
        del vertices[i_vertex:]
        del indices[i_index:]

    @property
    def n_lat_divide(self):
        return self.__n_lat_divide
    
    @n_lat_divide.setter
    @Mesh.param_setter
    def n_lat_divide(self, n:int):
        self.__n_lat_divide = n

    @property
    def n_lon_divide(self):
        return self.__n_lon_divide
    
    @n_lon_divide.setter
    @Mesh.param_setter
    def n_lon_divide(self, n:int):
        self.__n_lon_divide = n

    @property
    def start_lon(self):
        return self.__start_lon
    
    @start_lon.setter
    @Mesh.param_setter
    def start_lon(self, angle:float):
        self.__start_lon = angle

    @property
    def span_lon(self):
        return self.__span_lon
    
    @span_lon.setter
    @Mesh.param_setter
    def span_lon(self, angle:float):
        self.__span_lon = angle

    @property
    def start_lat(self):
        return self.__start_lat
    
    @start_lat.setter
    @Mesh.param_setter
    def start_lat(self, angle:float):
        self.__start_lat = angle

    @property
    def span_lat(self):
        return self.__span_lat

    @span_lat.setter
    @Mesh.param_setter
    def span_lat(self, angle:float):
        self.__span_lat = angle

    @property
    def radius(self):
        return self.__radius
    
    @radius.setter
    @Mesh.param_setter
    def radius(self, radius:float):
        self.__radius = radius
