from .SceneNode import SceneNode
from .Manipulators.SceneRoamManipulator import SceneRoamManipulator
from .Renderers.ForwardRenderer import ForwardRenderer
from .VideoRecorder import VideoRecorder

from glass.utils import checktype

import glm
import math
from enum import Enum
import numpy as np
import sys

Screen = {}
def import_Screen(gui_system:str)->None:
    if gui_system not in Screen:
        cmd = f'from .Screens.{gui_system}Screen import {gui_system}Screen'
        exec(cmd)

        Screen[gui_system] = eval(f"{gui_system}Screen")

class Camera(SceneNode):

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
    def __init__(self, gui_system="", projection_mode:ProjectionMode=ProjectionMode.Perspective, name:str=""):
        SceneNode.__init__(self, name, unique_path=True)
        self.__projection_mode:Camera.ProjectionMode = projection_mode
        self.__gui_system:str = ""

        self.__fov_deg:float = 45
        self.__fov_rad:float = math.pi/4
        half_fov = self.__fov_rad/2
        self.__tan_half_fov:float = math.tan(half_fov)
        self.__sin_half_fov:float = math.sin(half_fov)
        self.__far:float = 100
        self.__near:float = 0.1
        self.__clip:float = self.__far - self.__near
        self.__height:float = 40*2*self.__near*self.__tan_half_fov
        self.__CSM_levels:int = 5
        self.__lens:Camera.Lens = Camera.Lens()

        self._set_screen(gui_system)

    def _set_screen(self, gui_system)->None:
        if not isinstance(gui_system, str):
            gui_system = gui_system.__name__

        if not gui_system:
            for module_name in sys.modules:
                if module_name.startswith("PyQt6"):
                    gui_system = "PyQt6"
                    break

                if module_name.startswith("PyQt5"):
                    gui_system = "PyQt5"
                    break

                if module_name.startswith("PySide6"):
                    gui_system = "PySide6"
                    break

                if module_name.startswith("PySide2"):
                    gui_system = "PySide2"
                    break

        if gui_system:
            self.__gui_system = gui_system.lower().replace("pyside", "PySide").replace("pyqt", "PyQt")
            import_Screen(self.__gui_system)

        if not self.__gui_system:
            try:
                import_Screen("PyQt6")
                self.__gui_system = "PyQt6"
            except:
                self.__gui_system = ""

        if not self.__gui_system:
            try:
                import_Screen("PyQt5")
                self.__gui_system = "PyQt5"
            except:
                self.__gui_system = ""

        if not self.__gui_system:
            try:
                import_Screen("PySide6")
                self.__gui_system = "PySide6"
            except:
                self.__gui_system = ""

        if not self.__gui_system:
            try:
                import_Screen("PySide2")
                self.__gui_system = "PySide2"
            except:
                self.__gui_system = ""

        if not self.__gui_system:
            raise RuntimeError("all GUI systems failed to init")

        self.__screen = Screen[self.__gui_system](self)
        self.__screen.manipulator = SceneRoamManipulator()
        self.__screen.renderer = ForwardRenderer()

    @property
    def lens(self)->Lens:
        return self.__lens

    @property
    def gui_system(self)->str:
        return self.__gui_system
    
    @lens.setter
    def lens(self, lens:Lens)->None:
        self.__lens = lens

    @property
    def projection_mode(self)->ProjectionMode:
        return self.__projection_mode
    
    @projection_mode.setter
    def projection_mode(self, projection_mode:ProjectionMode)->None:
        self.__projection_mode = projection_mode

    @property
    def tan_half_fov(self)->float:
        return self.__tan_half_fov
    
    @property
    def sin_half_fov(self)->float:
        return self.__sin_half_fov

    @property
    def aspect(self)->float:
        return self.__screen.width() / self.__screen.height()
    
    @property
    def fov_x(self)->float:
        return 2*math.atan(self.aspect*self.__tan_half_fov)/math.pi*180
    
    @property
    def fov_y(self)->float:
        return self.__fov_deg
    
    @property
    def fov(self)->float:
        return self.__fov_deg
    
    @fov.setter
    def fov(self, fov_deg:float)->None:
        self.__fov_deg = fov_deg
        self.__fov_rad = fov_deg/180*math.pi
        half_fov = self.__fov_rad/2
        self.__tan_half_fov = math.tan(half_fov)
        self.__sin_half_fov = math.sin(half_fov)
        self.__height = 40*2*self.__near*self.__tan_half_fov

    @property
    def near(self)->float:
        return self.__near
    
    @near.setter
    def near(self, near:float)->None:
        self.__near = near
        self.__clip = self.__far - self.__near
        self.__height = 40*2*self.__near*self.__tan_half_fov
    
    @property
    def far(self)->float:
        return self.__far
    
    @far.setter
    def far(self, far:float)->None:
        self.__far = far
        self.__clip = self.__far - self.__near

    @property
    def clip(self)->float:
        return self.__clip

    @property
    def height(self)->float:
        return self.__height

    @height.setter
    def height(self, height:float)->None:
        self.__height = height

        self.__tan_half_fov = self.__height / (40*2*self.__near)
        half_fov = math.atan(self.__tan_half_fov)
        self.__fov_rad = 2*half_fov
        self.__fov_deg = self.__fov_rad/math.pi*180
        self.__sin_half_fov = math.sin(half_fov)

    @property
    def width(self)->float:
        return self.__height * self.aspect
    
    @width.setter
    def width(self, width:float)->None:
        self.__height = width / self.screen.width() * self.screen.height()

    @property
    def screen(self):
        return self.__screen

    @property
    def CSM_levels(self)->int:
        return self.__CSM_levels
    
    @CSM_levels.setter
    def CSM_levels(self, levels:int):
        self.__CSM_levels = levels

    def take_photo(self, save_path:str=None, viewport:tuple=None)->np.ndarray:
        return self.screen.capture(save_path, viewport)
    
    def record_video(self, save_path:str, viewport:tuple=None, fps:(float,int)=None)->VideoRecorder:
        return self.screen.capture_video(save_path, viewport, fps)

    def project(self, world_coord:glm.vec3)->glm.vec4:
        return self.view_to_NDC(self.world_to_view(world_coord))
    
    def project3(self, world_coord:glm.vec3)->glm.vec3:
        NDC = self.project(world_coord)
        return NDC.xyz / NDC.w

    def world_to_view(self, world_coord:glm.vec3)->glm.vec3:
        return glm.inverse(self.abs_orientation) * (world_coord - self.abs_position)

    def view_to_world(self, view_coord:glm.vec3)->glm.vec3:
        return self.abs_orientation * view_coord + self.abs_position

    def world_dir_to_view(self, world_dir:glm.vec3)->glm.vec3:
        return glm.inverse(self.abs_orientation) * world_dir

    def view_dir_to_world(self, view_dir:glm.vec3)->glm.vec3:
        return self.abs_orientation * view_dir
    
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
    
    def screen_to_view_dir(self, screen_pos:glm.vec2)->glm.vec3:
        xNDC = 2*screen_pos.x / self.screen.width() - 1
        yNDC = 1 - 2*screen_pos.y / self.screen.height()

        view_dir = glm.vec3()
        view_dir.x = xNDC * self.aspect * self.tan_half_fov
        view_dir.y = 1
        view_dir.z = yNDC * self.tan_half_fov
        return glm.normalize(view_dir)
    
    def screen_to_world_dir(self, screen_pos:glm.vec2)->glm.vec3:
        return self.view_dir_to_world(self.screen_to_view_dir(screen_pos))
    