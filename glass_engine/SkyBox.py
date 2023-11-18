from .Mesh import Mesh
from .Camera import Camera
from .GlassEngineConfig import GlassEngineConfig

from glass.utils import checktype
from glass import Vertex, samplerCube, ShaderProgram

import glm
from OpenGL import GL
import os

class SkyBox(Mesh):

    @checktype
    def __init__(self, name:str=""):
        Mesh.__init__(self, name=name, block=True)
        self.render_hints.depth_func = "<="
        self.render_hints.cull_face = GL.GL_FRONT
        self.__skybox_map = None
        self.__program = None
        self.should_add_color = False
        self.start_building()

    @property
    def skybox_map(self):
        return self.__skybox_map
    
    @skybox_map.setter
    @checktype
    def skybox_map(self, skybox_map:samplerCube):
        self.__skybox_map = skybox_map
    
    @property
    def is_completed(self):
        return (self.__skybox_map is not None and self.__skybox_map.is_completed)
    
    def __getattr__(self, key):
        if key not in ["right", "left", "top", "bottom", "back", "front", "up", "down"]:
            return super().__getattr__(key)

        if self.skybox_map is None:
            self.skybox_map = samplerCube()

        return self.skybox_map[key]

    def __setattr__(self, key, value):
        if key not in ["right", "left", "top", "bottom", "back", "front", "up", "down"]:
            return super().__setattr__(key, value)

        if self.skybox_map is None:
            self.skybox_map = samplerCube()

        self.skybox_map[key] = value

    def build(self):
        self.self_calculated_normal = True
        self.is_closed = True
        self.x_min, self.x_max = -1, 1
        self.y_min, self.y_max = -1, 1
        self.z_min, self.z_max = -1, 1

        vertices = self.vertices
        indices = self.indices

        # 左面
        vertices[0] = Vertex(position=glm.vec3(-1,  1, -1))
        vertices[1] = Vertex(position=glm.vec3(-1, -1, -1))
        vertices[2] = Vertex(position=glm.vec3(-1, -1,  1))
        vertices[3] = Vertex(position=glm.vec3(-1,  1,  1))

        # 右面
        vertices[4] = Vertex(position=glm.vec3(1, -1, -1))
        vertices[5] = Vertex(position=glm.vec3(1,  1, -1))
        vertices[6] = Vertex(position=glm.vec3(1,  1,  1))
        vertices[7] = Vertex(position=glm.vec3(1, -1,  1))

        # 后面
        vertices[8] = Vertex(position=glm.vec3(-1, -1, -1))
        vertices[9] = Vertex(position=glm.vec3( 1, -1, -1))
        vertices[10] = Vertex(position=glm.vec3( 1, -1,  1))
        vertices[11] = Vertex(position=glm.vec3(-1, -1,  1))

        # 前面
        vertices[12] = Vertex(position=glm.vec3( 1, 1, -1))
        vertices[13] = Vertex(position=glm.vec3(-1, 1, -1))
        vertices[14] = Vertex(position=glm.vec3(-1, 1,  1))
        vertices[15] = Vertex(position=glm.vec3( 1, 1,  1))

        # 下面
        vertices[16] = Vertex(position=glm.vec3(-1,  1, -1))
        vertices[17] = Vertex(position=glm.vec3( 1,  1, -1))
        vertices[18] = Vertex(position=glm.vec3( 1, -1, -1))
        vertices[19] = Vertex(position=glm.vec3(-1, -1, -1))

        # 上面
        vertices[20] = Vertex(position=glm.vec3(-1, -1, 1))
        vertices[21] = Vertex(position=glm.vec3( 1, -1, 1))
        vertices[22] = Vertex(position=glm.vec3( 1,  1, 1))
        vertices[23] = Vertex(position=glm.vec3(-1,  1, 1))

        # 左面
        indices[0] = glm.uvec3(0, 1, 2)
        indices[1] = glm.uvec3(0, 2, 3)

        # 右面
        indices[2] = 4+glm.uvec3(0, 1, 2)
        indices[3] = 4+glm.uvec3(0, 2, 3)

        # 后面
        indices[4] = 8+glm.uvec3(0, 1, 2)
        indices[5] = 8+glm.uvec3(0, 2, 3)

        # 前面
        indices[6] = 12+glm.uvec3(0, 1, 2)
        indices[7] = 12+glm.uvec3(0, 2, 3)
        
        # 下面
        indices[8] = 16+glm.uvec3(0, 1, 2)
        indices[9] = 16+glm.uvec3(0, 2, 3)

        # 上面
        indices[10] = 20+glm.uvec3(0, 1, 2)
        indices[11] = 20+glm.uvec3(0, 2, 3)

    @property
    def program(self):
        if self.__program is None:
            self.__program = ShaderProgram()
            self_folder = os.path.dirname(os.path.abspath(__file__))
            self.__program.compile(self_folder + "/glsl/Pipelines/skybox/skybox.vs")
            self.__program.compile(self_folder + "/glsl/Pipelines/skybox/skybox.fs")

        return self.__program
    
    def draw(self, camera:Camera):
        scene = camera.scene
        self.program["camera"] = camera
        self.program["skybox_map"] = self.skybox_map
        self.program["sky_distance"] = scene.background.distance
        if GlassEngineConfig["USE_FOG"]:
            self.program["fog"] = scene.fog
            
        Mesh.draw(self, self.program)