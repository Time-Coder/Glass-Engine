from .SinglePathNode import SinglePathNode
from .Screen import Screen
from .Manipulators.SceneRoamManipulator import SceneRoamManipulator
from .Renderers.ForwardRenderer import ForwardRenderer

from glass.utils import checktype

import glm
import math
from enum import Enum

class Camera(SinglePathNode):

    class ProjectionMode(Enum):
        Perspective = 0
        Orthographic = 1

    class Lens:

        def __init__(self):
            self.focus:float = 0.09
            self.aperture:float = 0.05
            self.auto_focus:bool = True
            self.focus_tex_coord:glm.vec2 = glm.vec2(0.5, 0.5)
            self.focus_change_time:float = 2

            self.explosure:float = 1
            self.auto_explosure:bool = True
            self.local_explosure:bool = False
            self.explosure_adapt_time:float = 2

        @property
        def clear_distance(self):
            return 1/(1/self.focus - 1/self.near)
        
        @clear_distance.setter
        def clear_distance(self, distance:float):
            self.focus = 1/(1/self.near + 1/distance)

    @checktype
    def __init__(self, projection_mode:ProjectionMode=ProjectionMode.Perspective, name:str=""):
        SinglePathNode.__init__(self, name)
        self.__projection_type = projection_mode

        self.__fov_deg = 45
        self.__fov_rad = math.pi/4
        half_fov = self.__fov_rad/2
        self.__tan_half_fov = math.tan(half_fov)
        self.__sin_half_fov = math.sin(half_fov)
        self.__far = 100
        self.__near = 0.1
        self.__clip = self.__far - self.__near
        self.__height = 40*2*self.__near*self.__tan_half_fov
        self.__CSM_levels = 5

        self.__lens = Camera.Lens()

        self.__screen = Screen(self)
        self.__screen.manipulator = SceneRoamManipulator()
        self.__screen.renderer = ForwardRenderer()

    @property
    def lens(self):
        return self.__lens

    @property
    def projection_mode(self):
        return self.__projection_type
    
    @projection_mode.setter
    @checktype
    def projection_mode(self, projection_mode:ProjectionMode):
        self.__projection_type = projection_mode

    @property
    def tan_half_fov(self):
        return self.__tan_half_fov
    
    @property
    def sin_half_fov(self):
        return self.__sin_half_fov

    @property
    def aspect(self):
        return self.__screen.width() / self.__screen.height()
    
    @property
    def fov_x(self):
        return 2*math.atan(self.aspect*self.__tan_half_fov)/math.pi*180
    
    @property
    def fov_y(self):
        return self.__fov_deg
    
    @property
    def fov(self):
        return self.__fov_deg
    
    @fov.setter
    @checktype
    def fov(self, angle_deg:float):
        self.__fov_deg = angle_deg
        self.__fov_rad = angle_deg/180*math.pi
        half_fov = self.__fov_rad/2
        self.__tan_half_fov = math.tan(half_fov)
        self.__sin_half_fov = math.sin(half_fov)
        self.__height = 40*2*self.__near*self.__tan_half_fov

    @property
    def fov_rad(self):
        return self.__fov_rad
    
    @fov_rad.setter
    @checktype
    def fov_rad(self, angle_rad:float):
        self.__fov_deg = angle_rad/math.pi*180
        self.__fov_rad = angle_rad
        half_fov = self.__fov_rad/2
        self.__tan_half_fov = math.tan(half_fov)
        self.__sin_half_fov = math.sin(half_fov)
        self.__height = 40*2*self.__near*self.__tan_half_fov

    @property
    def near(self):
        return self.__near
    
    @near.setter
    @checktype
    def near(self, near:float):
        self.__near = near
        self.__clip = self.__far - self.__near
        self.__height = 40*2*self.__near*self.__tan_half_fov
    
    @property
    def far(self):
        return self.__far
    
    @far.setter
    @checktype
    def far(self, far:float):
        self.__far = far
        self.__clip = self.__far - self.__near

    @property
    def clip(self):
        return self.__clip
    
    @clip.setter
    @checktype
    def clip(self, clip:float):
        self.__clip = clip
        self.__far = self.__near + clip

    @property
    def height(self):
        return self.__height

    @height.setter
    @checktype
    def height(self, height:float):
        self.__height = height

        self.__tan_half_fov = self.__height / (40*2*self.__near)
        half_fov = math.atan(self.__tan_half_fov)
        self.__fov_rad = 2*half_fov
        self.__fov_deg = self.__fov_rad/math.pi*180
        self.__sin_half_fov = math.sin(half_fov)

    @property
    def width(self):
        return self.__height * self.aspect
    
    @width.setter
    @checktype
    def width(self, width:float):
        self.__height = width / self.screen.width() * self.screen.height()

    @property
    def screen(self):
        return self.__screen

    @property
    def CSM_levels(self):
        return self.__CSM_levels
    
    @CSM_levels.setter
    @checktype
    def CSM_levels(self, levels:int):
        self.__CSM_levels = levels

    @property
    def near_height(self):
        return 2 * self.near * self.tan_half_fov
    
    @property
    def near_width(self):
        return self.aspect * self.near_height

    @checktype
    def project(self, world_coord:glm.vec3)->glm.vec4:
        return self.view_to_NDC(self.world_to_view(world_coord))
    
    @checktype
    def project3(self, world_coord:glm.vec3)->glm.vec3:
        NDC = self.project(world_coord)
        return NDC.xyz / NDC.w

    @checktype
    def world_to_view(self, world_coord:glm.vec3)->glm.vec3:
        return glm.inverse(self.abs_orientation) * (world_coord - self.abs_position)

    @checktype
    def view_to_world(self, view_coord:glm.vec3)->glm.vec3:
        return self.abs_orientation * view_coord + self.abs_position

    @checktype
    def world_dir_to_view(self, world_dir:glm.vec3)->glm.vec3:
        return glm.inverse(self.abs_orientation) * world_dir

    @checktype
    def view_dir_to_world(self, view_dir:glm.vec3)->glm.vec3:
        return self.abs_orientation * view_dir
    
    @checktype
    def view_to_NDC(self, view_coord:glm.vec3)->glm.vec4:
        NDC_coord = glm.vec4()
        if self.projection_mode == Camera.ProjectionMode.Perspective:
            NDC_coord.x = view_coord.x / (self.aspect * self.tan_half_fov)
            NDC_coord.y = view_coord.z / self.tan_half_fov
            NDC_coord.z = 2*self.far*(view_coord.y-self.near)/self.clip-view_coord.y
            NDC_coord.w = view_coord.y
        else:
            NDC_coord.x = 2*view_coord.x / self.width
            NDC_coord.y = 2*view_coord.z / self.height
            NDC_coord.z = 2*(view_coord.y-self.near)/self.clip-1
            NDC_coord.w = 1
        
        return NDC_coord
    
    @checktype
    def screen_to_view_dir(self, screen_pos:glm.vec2)->glm.vec3:
        xNDC = 2*screen_pos.x / self.screen.width() - 1
        yNDC = 1 - 2*screen_pos.y / self.screen.height()

        view_dir = glm.vec3()
        view_dir.x = xNDC * self.aspect * self.tan_half_fov
        view_dir.y = 1
        view_dir.z = yNDC * self.tan_half_fov
        return glm.normalize(view_dir)
    
    @checktype
    def screen_to_world_dir(self, screen_pos:glm.vec2)->glm.vec3:
        return self.view_dir_to_world(self.screen_to_view_dir(screen_pos))
    