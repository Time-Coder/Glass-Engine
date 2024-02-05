from .Mesh import Mesh
from .Camera import Camera
from .GlassEngineConfig import GlassEngineConfig

from glass.utils import checktype
from glass import Vertex, sampler2D, ShaderProgram

import glm
import math
import numpy as np
from OpenGL import GL
import os


class SkyDome(Mesh):

    @checktype
    def __init__(self, n_lon_divide: int = 100, n_lat_divide: int = 50, name: str = ""):
        Mesh.__init__(self, name=name, block=True)
        self.__n_lon_divide = n_lon_divide
        self.__n_lat_divide = n_lat_divide
        self.__skydome_map = None
        self.__program = None

        self.render_hints.depth_func = "<="
        self.render_hints.cull_face = GL.GL_FRONT
        self.should_add_color = False
        self.start_building()

    def build(self):
        self.is_closed = True
        self.self_calculated_normal = True
        self.x_min, self.x_max = -1, 1
        self.y_min, self.y_max = -1, 1
        self.z_min, self.z_max = -1, 1

        vertices = self.vertices
        indices = self.indices
        n_lon_divide = self.__n_lon_divide
        n_lat_divide = self.__n_lat_divide

        i_vertex = 0
        i_index = 0

        for i in range(n_lon_divide):
            theta = math.pi * (2 * i / (n_lon_divide - 1) - 0.5)
            s = 1 - i / (n_lon_divide - 1)
            cos_theta = math.cos(theta)
            sin_theta = math.sin(theta)

            for j in range(n_lat_divide):
                phi = math.pi * (j / (n_lat_divide - 1) - 0.5)
                t = j / (n_lat_divide - 1)
                cos_phi = math.cos(phi)
                sin_phi = math.sin(phi)

                vertex = Vertex()

                vertex.position = glm.vec3(
                    cos_phi * cos_theta, cos_phi * sin_theta, sin_phi
                )
                vertex.tex_coord = glm.vec2(s, t)

                vertices[i_vertex] = vertex
                i_vertex += 1

                if i > 0 and j > 0:
                    triangle = glm.uvec3(0, 0, 0)
                    triangle[0] = i_vertex - 1
                    triangle[1] = i_vertex - 1 - n_lat_divide
                    triangle[2] = i_vertex - 1 - n_lat_divide - 1
                    indices[i_index] = triangle
                    i_index += 1

                    triangle = glm.uvec3(0, 0, 0)
                    triangle[0] = i_vertex - 1
                    triangle[1] = i_vertex - 1 - n_lat_divide - 1
                    triangle[2] = i_vertex - 1 - 1
                    indices[i_index] = triangle
                    i_index += 1

        del vertices[i_vertex:]
        del indices[i_index:]

    @property
    def n_lat_divide(self):
        return self.__n_lat_divide

    @n_lat_divide.setter
    @Mesh.param_setter
    def n_lat(self, n_lat_divide: int):
        self.__n_lat_divide = n_lat_divide

    @property
    def n_lon_divide(self):
        return self.__n_lon_divide

    @n_lon_divide.setter
    @Mesh.param_setter
    def n_lon(self, n_lon_divide: int):
        self.__n_lon_divide = n_lon_divide

    @property
    def skydome_map(self):
        return self.__skydome_map

    @skydome_map.setter
    @checktype
    def skydome_map(self, skydome_map: (sampler2D, np.ndarray, str)):
        if isinstance(skydome_map, (np.ndarray, str)):
            if self.__skydome_map is None:
                self.__skydome_map = sampler2D()
            self.__skydome_map.image = skydome_map
        else:
            self.__skydome_map = skydome_map

    @property
    def is_completed(self):
        return self.__skydome_map is not None and self.__skydome_map.is_completed

    def __getitem__(self, name: str):
        return self.__skydome_map[name]

    def __setitem__(self, name: str, value):
        self.__skydome_map[name] = value

    @property
    def program(self):
        if self.__program is None:
            self_folder = os.path.dirname(os.path.abspath(__file__))
            program = ShaderProgram()
            GlassEngineConfig.define_for_program(program)
            program.compile(self_folder + "/glsl/Pipelines/skydome/skydome.vs")
            program.compile(self_folder + "/glsl/Pipelines/skydome/skydome.fs")
            self.__program = program

        return self.__program

    def draw(self, camera: Camera):
        scene = camera.scene
        self.program["camera"] = camera
        self.program["skydome_map"] = self.skydome_map
        self.program["sky_distance"] = scene.background.distance

        if GlassEngineConfig["USE_FOG"]:
            self.program["fog"] = scene.fog

        Mesh.draw(self, self.program)
