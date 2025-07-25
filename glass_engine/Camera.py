from __future__ import annotations
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
import importlib
from typing import Union
from functools import wraps

Screen = {}


def import_Screen(gui_system: str) -> None:
    if gui_system not in Screen:
        module_name = f"glass_engine.Screens.{gui_system}Screen"
        module = importlib.import_module(module_name)

        Screen[gui_system] = getattr(module, f"{gui_system}Screen")


class Camera(SceneNode):

    class ProjectionMode(Enum):
        Perspective = 0
        Orthographic = 1

    class Lens:

        def __init__(self, camera):
            self.camera = camera
            self.__focus: float = 0.09
            self.__aperture: float = 0.05
            self.__auto_focus: bool = True
            self.__focus_tex_coord: glm.vec2 = glm.vec2(0.5, 0.5)
            self.__focus_change_time: float = 2
            self.__exposure: float = 1
            self.__auto_exposure: bool = True
            self.__local_exposure: bool = False
            self.__exposure_adapt_time: float = 2

        def param_setter(func):

            @wraps(func)
            def wrapper(*args, **kwargs):
                self = args[0]
                value = args[1]

                equal = False
                try:
                    lvalue = getattr(self, func.__name__)
                    if type(lvalue) != type(value):
                        equal = False
                    else:
                        equal = bool(getattr(self, func.__name__) == value)
                except:
                    equal = False

                if equal:
                    return

                safe_func = checktype(func)
                return_value = safe_func(*args, **kwargs)
                self.camera.screen.update()

                return return_value

            return wrapper

        @property
        def clear_distance(self):
            return 1 / (1 / self.focus - 1 / self.camera.near)

        @clear_distance.setter
        @param_setter
        def clear_distance(self, distance: float):
            self.focus = 1 / (1 / self.camera.near + 1 / distance)

        @property
        def focus(self)->float:
            return self.__focus
        
        @focus.setter
        @param_setter
        def focus(self, focus: float):
            self.__focus = focus

        @property
        def aperture(self)->float:
            return self.__aperture
        
        @aperture.setter
        @param_setter
        def aperture(self, aperture: float):
            self.__aperture = aperture

        @property
        def auto_focus(self)->bool:
            return self.__auto_focus
        
        @auto_focus.setter
        @param_setter
        def auto_focus(self, auto_focus: bool):
            self.__auto_focus = auto_focus

        @property
        def focus_tex_coord(self):
            return self.__focus_tex_coord
        
        @focus_tex_coord.setter
        @param_setter
        def focus_tex_coord(self, focus_tex_coord: glm.vec2):
            self.__focus_tex_coord = focus_tex_coord

        @property
        def focus_change_time(self):
            return self.__focus_change_time
        
        @focus_change_time.setter
        @param_setter
        def focus_change_time(self, focus_change_time: float):
            self.__focus_change_time = focus_change_time

        @property
        def exposure(self):
            return self.__exposure
        
        @exposure.setter
        @param_setter
        def exposure(self, exposure: float):
            self.__exposure = exposure

        @property
        def auto_exposure(self):
            return self.__auto_exposure
        
        @auto_exposure.setter
        @param_setter
        def auto_exposure(self, auto_exposure: bool):
            self.__auto_exposure = auto_exposure

        @property
        def local_exposure(self)->bool:
            return self.__local_exposure
        
        @local_exposure.setter
        @param_setter
        def local_exposure(self, local_exposure: bool):
            self.__local_exposure = local_exposure

        @property
        def exposure_adapt_time(self):
            return self.__exposure_adapt_time
        
        @exposure_adapt_time.setter
        @param_setter
        def exposure_adapt_time(self, exposure_adapt_time: float):
            self.__exposure_adapt_time = exposure_adapt_time

    @checktype
    def __init__(
        self,
        gui_system="",
        projection_mode: Camera.ProjectionMode = ProjectionMode.Perspective,
        name: str = "",
    ):
        SceneNode.__init__(self, name, unique_path=True)
        self.__projection_mode: Camera.ProjectionMode = projection_mode
        self.__gui_system: str = ""

        self.__max_fov: float = 120
        self.__min_fov: float = 5
        self.__fov_deg: float = 45
        self.__fov_rad: float = math.pi / 4
        half_fov = self.__fov_rad / 2
        self.__tan_half_fov: float = math.tan(half_fov)
        self.__sin_half_fov: float = math.sin(half_fov)
        self.__far: float = 100
        self.__near: float = 0.1
        self.__clip: float = self.__far - self.__near
        self.__height: float = 40 * 2 * self.__near * self.__tan_half_fov
        self.__max_height: float = (
            40 * 2 * self.__near * math.tan(self.__max_fov / 2 / 180 * math.pi)
        )
        self.__min_height: float = (
            40 * 2 * self.__near * math.tan(self.__min_fov / 2 / 180 * math.pi)
        )
        self.__CSM_levels: int = 5
        self.__aspect_ratio: float = 1
        self.__lens: Camera.Lens = Camera.Lens(self)

        self._set_screen(gui_system)

    def _set_screen(self, gui_system) -> None:
        all_gui_systems = ["PySide6", "PyQt6", "PySide2", "PyQt5"]

        if not isinstance(gui_system, str):
            gui_system = gui_system.__name__

        if not gui_system:
            for module_name in sys.modules:
                for gui_sys in all_gui_systems:
                    if module_name.startswith(gui_sys):
                        gui_system = gui_sys
                        break

        if not gui_system:
            for gui_sys in all_gui_systems:
                try:
                    exec(f"from {gui_sys}.QtWidgets import QWidget")
                    gui_system = gui_sys
                    break
                except:
                    pass

        if gui_system:
            self.__gui_system = (
                gui_system.lower().replace("pyside", "PySide").replace("pyqt", "PyQt")
            )
            import_Screen(self.__gui_system)

        if not self.__gui_system:
            for gui_sys in all_gui_systems:
                try:
                    import_Screen(gui_sys)
                    self.__gui_system = gui_sys
                    break
                except:
                    self.__gui_system = ""

        if not self.__gui_system:
            raise RuntimeError("all GUI systems failed to init")

        self.__screen = Screen[self.__gui_system](self)
        self.__screen.manipulator = SceneRoamManipulator()
        self.__screen.renderer = ForwardRenderer()

    def param_setter(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            self = args[0]
            value = args[1]

            equal = False
            try:
                lvalue = getattr(self, func.__name__)
                if type(lvalue) != type(value):
                    equal = False
                else:
                    equal = bool(getattr(self, func.__name__) == value)
            except:
                equal = False

            if equal:
                return

            safe_func = checktype(func)
            return_value = safe_func(*args, **kwargs)
            self.screen.update()

            return return_value

        return wrapper

    @property
    def aspect_ratio(self)->float:
        return self.__aspect_ratio
    
    @aspect_ratio.setter
    @param_setter
    def aspect_ratio(self, aspect_ratio: float) -> None:
        self.__aspect_ratio = aspect_ratio

    @property
    def lens(self) -> Lens:
        return self.__lens

    @property
    def gui_system(self) -> str:
        return self.__gui_system

    @lens.setter
    @param_setter
    def lens(self, lens: Lens) -> None:
        self.__lens = lens

    @property
    def projection_mode(self) -> ProjectionMode:
        return self.__projection_mode

    @projection_mode.setter
    @param_setter
    def projection_mode(self, projection_mode: ProjectionMode) -> None:
        self.__projection_mode = projection_mode

    @property
    def tan_half_fov(self) -> float:
        return self.__tan_half_fov

    @property
    def sin_half_fov(self) -> float:
        return self.__sin_half_fov

    @property
    def aspect(self) -> float:
        return self.__screen.width() / self.__screen.height() / self.aspect_ratio

    @property
    def fov(self) -> float:
        return self.__fov_deg

    @fov.setter
    @param_setter
    def fov(self, fov_deg: float) -> None:
        if fov_deg < self.min_fov:
            fov_deg = self.min_fov

        if fov_deg > self.max_fov:
            fov_deg = self.max_fov

        if fov_deg == self.__fov_deg:
            return

        self.__fov_deg = fov_deg
        self.__fov_rad = fov_deg / 180 * math.pi
        half_fov = self.__fov_rad / 2
        self.__tan_half_fov = math.tan(half_fov)
        self.__sin_half_fov = math.sin(half_fov)
        self.__height = 40 * 2 * self.__near * self.__tan_half_fov

    @property
    def max_fov(self):
        return self.__max_fov

    @max_fov.setter
    @param_setter
    def max_fov(self, max_fov):
        if self.__max_fov == max_fov:
            return

        if max_fov < self.min_fov:
            self.__min_fov = max_fov
            self.__min_height = (
                40 * 2 * self.__near * math.tan(self.__min_fov / 2 / 180 * math.pi)
            )

        self.__max_fov = max_fov
        self.__max_height = (
            40 * 2 * self.__near * math.tan(self.__max_fov / 2 / 180 * math.pi)
        )

        if self.fov > max_fov:
            self.fov = max_fov

    @property
    def min_fov(self):
        return self.__min_fov

    @min_fov.setter
    @param_setter
    def min_fov(self, min_fov):
        if self.__min_fov == min_fov:
            return

        if min_fov > self.max_fov:
            self.__max_fov = min_fov
            self.__max_height = (
                40 * 2 * self.__near * math.tan(self.__max_fov / 2 / 180 * math.pi)
            )

        self.__min_fov = min_fov
        self.__min_height = (
            40 * 2 * self.__near * math.tan(self.__min_fov / 2 / 180 * math.pi)
        )

        if self.fov < min_fov:
            self.fov = min_fov

    @property
    def max_height(self):
        return self.__max_height

    @max_height.setter
    @param_setter
    def max_height(self, max_height):
        if self.__max_height == max_height:
            return

        if max_height < self.min_height:
            self.__min_height = max_height
            self.__min_fov = (
                math.atan(self.__min_height / 80 / self.__near) / math.pi * 180 * 2
            )

        self.__max_height = max_height
        self.__max_fov = (
            math.atan(self.__max_height / 80 / self.__near) / math.pi * 180 * 2
        )

        if self.fov > self.__max_fov:
            self.fov = self.__max_fov

    @property
    def min_height(self):
        return self.__min_height

    @min_height.setter
    @param_setter
    def min_height(self, min_height: float):
        if self.__min_height == min_height:
            return

        if min_height > self.max_height:
            self.__max_height = min_height
            self.__max_fov = (
                math.atan(self.__max_height / 80 / self.__near) / math.pi * 180 * 2
            )

        self.__min_height = min_height
        self.__min_fov = (
            math.atan(self.__min_height / 80 / self.__near) / math.pi * 180 * 2
        )

        if self.fov < self.__min_fov:
            self.fov = self.__min_fov

    @property
    def fov_x(self) -> float:
        return 2 * math.atan(self.aspect * self.__tan_half_fov) / math.pi * 180

    @fov_x.setter
    @param_setter
    def fov_x(self, fov_x):
        self.fov = (
            2
            * math.atan(math.tan(fov_x / 180 * math.pi / 2) / self.aspect)
            / math.pi
            * 180
        )

    @property
    def fov_y(self) -> float:
        return self.fov

    @fov_y.setter
    @param_setter
    def fov_y(self, fov_y: float):
        self.fov = fov_y

    @property
    def near(self) -> float:
        return self.__near

    @near.setter
    @param_setter
    def near(self, near: float) -> None:
        self.__near = near
        self.__clip = self.__far - self.__near
        self.__height = 40 * 2 * self.__near * self.__tan_half_fov
        self.__min_height = (
            40 * 2 * self.__near * math.tan(self.__min_fov / 180 * math.pi / 2)
        )
        self.__max_height = (
            40 * 2 * self.__near * math.tan(self.__max_fov / 180 * math.pi / 2)
        )

    @property
    def far(self) -> float:
        return self.__far

    @far.setter
    @param_setter
    def far(self, far: float) -> None:
        self.__far = far
        self.__clip = self.__far - self.__near

    @property
    def clip(self) -> float:
        return self.__clip

    @property
    def height(self) -> float:
        return self.__height

    @height.setter
    @param_setter
    def height(self, height: float) -> None:
        if height > self.max_height:
            height = self.max_height

        if height < self.min_height:
            height = self.min_height

        self.__height = height

        self.__tan_half_fov = self.__height / (40 * 2 * self.__near)
        half_fov = math.atan(self.__tan_half_fov)
        self.__fov_rad = 2 * half_fov
        self.__fov_deg = self.__fov_rad / math.pi * 180
        self.__sin_half_fov = math.sin(half_fov)

    @property
    def width(self) -> float:
        return self.__height * self.aspect

    @width.setter
    @param_setter
    def width(self, width: float) -> None:
        self.height = width / self.aspect

    @property
    def screen(self):
        return self.__screen

    @property
    def CSM_levels(self) -> int:
        return self.__CSM_levels

    @CSM_levels.setter
    @param_setter
    def CSM_levels(self, levels: int):
        self.__CSM_levels = levels

    def take_photo(self, save_path: str = None, viewport: tuple = None) -> np.ndarray:
        return self.screen.capture(save_path, viewport)

    def record_video(
        self, save_path: str, viewport: tuple = None, fps: Union[float, int] = None
    ) -> VideoRecorder:
        return self.screen.capture_video(save_path, viewport, fps)

    def project(self, world_coord: glm.vec3) -> glm.vec4:
        return self.view_to_NDC(self.world_to_view(world_coord))

    def project3(self, world_coord: glm.vec3) -> glm.vec3:
        NDC = self.project(world_coord)
        return NDC.xyz / NDC.w

    def world_to_view(self, world_coord: glm.vec3) -> glm.vec3:
        return glm.inverse(self.abs_orientation) * (world_coord - self.abs_position)

    def view_to_world(self, view_coord: glm.vec3) -> glm.vec3:
        return self.abs_orientation * view_coord + self.abs_position

    def world_dir_to_view(self, world_dir: glm.vec3) -> glm.vec3:
        return glm.inverse(self.abs_orientation) * world_dir

    def view_dir_to_world(self, view_dir: glm.vec3) -> glm.vec3:
        return self.abs_orientation * view_dir

    def view_to_NDC(self, view_coord: glm.vec3) -> glm.vec4:
        NDC_coord = glm.vec4()
        if self.projection_mode == Camera.ProjectionMode.Perspective:
            NDC_coord.x = view_coord.x / (self.aspect * self.tan_half_fov)
            NDC_coord.y = view_coord.z / self.tan_half_fov
            NDC_coord.z = (
                2 * self.far * (view_coord.y - self.near) / self.clip - view_coord.y
            )
            NDC_coord.w = view_coord.y
        else:
            NDC_coord.x = 2 * view_coord.x / self.width
            NDC_coord.y = 2 * view_coord.z / self.height
            NDC_coord.z = 2 * (view_coord.y - self.near) / self.clip - 1
            NDC_coord.w = 1

        return NDC_coord

    def screen_to_view_dir(self, screen_pos: glm.vec2) -> glm.vec3:
        xNDC = 2 * screen_pos.x / self.screen.width() - 1
        yNDC = 1 - 2 * screen_pos.y / self.screen.height()

        view_dir = glm.vec3()
        view_dir.x = xNDC * self.aspect * self.tan_half_fov
        view_dir.y = 1
        view_dir.z = yNDC * self.tan_half_fov
        return glm.normalize(view_dir)

    def screen_to_world_dir(self, screen_pos: glm.vec2) -> glm.vec3:
        return self.view_dir_to_world(self.screen_to_view_dir(screen_pos))
