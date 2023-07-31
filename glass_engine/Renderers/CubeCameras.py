import math
import glm

from glass import UniformBlock

class CubeCamera:

    def __init__(self, face:str):
        self.near = 0.1
        self.far = 100
        self.clip = self.far - self.near
        self.focus = self.near
        self.aperture = 0.01
        self.auto_focus = False
        self.focus_tex_coord = glm.vec2(0.5, 0.5)
        self.focus_change_speed = 0.1
        self.projection_mode = 0

        cos45 = 0.5*math.sqrt(2)
        sin45 = cos45

        self.tan_half_fov = 1
        self.sin_half_fov = sin45
        self.aspect = 1

        self.height = 5
        self.width = 5
        self.CSM_levels = 5

        self.abs_orientation = glm.quat(1, 0, 0, 0)
        if face == "left":
            self.abs_orientation = glm.quat(cos45, 0, 0, sin45)
        elif face == "right":
            self.abs_orientation = glm.quat(cos45, 0, 0, -sin45)
        elif face == "back":
            self.abs_orientation = glm.quat(0, 0, 0, 1)
        elif face == "front":
            self.abs_orientation = glm.quat(1, 0, 0, 0)
        elif face == "top":
            self.abs_orientation = glm.quat(cos45, sin45, 0, 0)
        elif face == "bottom":
            self.abs_orientation = glm.quat(cos45, -sin45, 0, 0)
        self.abs_position = glm.vec3(0, 0, 0)

class CubeCameras(UniformBlock.HostClass):
    def __init__(self):
        UniformBlock.HostClass.__init__(self)
        
        self.cube_cameras = []
        self.cube_cameras.append(CubeCamera("right"))
        self.cube_cameras.append(CubeCamera("left"))
        self.cube_cameras.append(CubeCamera("bottom"))
        self.cube_cameras.append(CubeCamera("top"))
        self.cube_cameras.append(CubeCamera("front"))
        self.cube_cameras.append(CubeCamera("back"))
        
CubeCameras = CubeCameras()