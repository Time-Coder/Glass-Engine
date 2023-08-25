from .Manipulator import Manipulator

from glass.RenderHint import RenderHint
from glass.utils import checktype

from OpenGL import GL
import math
import glm
import datetime

class ModelViewManipulator(Manipulator):

    def __init__(self, distance:float=2, azimuth_deg:float=0, elevation_deg:float=0):
        Manipulator.__init__(self)
        
        self.__is_left_pressed = False
        self.__left_press_global_posF = glm.vec2(0, 0)
        self.__left_press_azimuth_deg = 0
        self.__left_press_elevation_deg = 0

        self.__is_right_pressed = False
        self.__right_press_global_posF = glm.vec2(0, 0)
        self.__right_press_offset = glm.vec2(0, 0)

        self.__distance = distance
        self.__azimuth_deg = azimuth_deg
        self.__elevation_deg = elevation_deg
        self.__offset = glm.vec2(0, 0)
        self.__sensitivity = 1

    @property
    def distance(self)->float:
        return self.__distance
    
    @distance.setter
    @checktype
    def distance(self, distance:float):
        self.__distance = distance
        self.__update_camera()
        self.camera.screen.update()

    @property
    def azimuth(self):
        return self.__azimuth_deg
    
    @azimuth.setter
    @checktype
    def azimuth(self, azimuth:float):
        self.__azimuth_deg = azimuth
        self.__update_camera()
        self.camera.screen.update()

    @property
    def elevation(self):
        return self.__elevation_deg
    
    @elevation.setter
    @checktype
    def elevation(self, elevation:float):
        self.__elevation_deg = elevation
        self.__update_camera()
        self.camera.screen.update()

    @property
    def sensitivity(self)->float:
        return self.__sensitivity
    
    @sensitivity.setter
    @checktype
    def sensitivity(self, sensitivity:float):
        self.__sensitivity = sensitivity

    def __update_camera(self):
        azimuth = self.__azimuth_deg/180*math.pi
        elevation = self.__elevation_deg/180*math.pi

        self.camera.position.x = self.__distance*math.cos(elevation)*math.sin(azimuth)
        self.camera.position.y = -self.__distance*math.cos(elevation)*math.cos(azimuth)
        self.camera.position.z = self.__distance*math.sin(elevation)

        if glm.length(self.__offset) > 1E-6:
            right = glm.dvec3(math.cos(azimuth), math.sin(azimuth), 0)
            forward = glm.dvec3(-math.sin(elevation) * math.sin(azimuth), math.sin(elevation) * math.cos(azimuth), math.cos(elevation))
            self.camera.position += (self.__offset.x * right + self.__offset.y * forward)

        self.camera.pitch = -self.__elevation_deg
        self.camera.yaw = self.__azimuth_deg

    def startup(self):
        self.__update_camera()

    def on_mouse_pressed(self, button:Manipulator.MouseButton, screen_pos:glm.vec2, global_pos:glm.vec2):
        if button == Manipulator.MouseButton.LeftButton:
            self.__is_left_pressed = True
            self.__left_press_global_posF = global_pos
            self.__left_press_azimuth_deg = self.__azimuth_deg
            self.__left_press_elevation_deg = self.__elevation_deg
        elif button in Manipulator.MouseButton.RightButton:
            self.__is_right_pressed = True
            self.__right_press_global_posF = global_pos
            self.__right_press_offset = self.__offset

        return False

    def on_mouse_released(self, button:Manipulator.MouseButton, screen_pos:glm.vec2, global_pos:glm.vec2):
        if button == Manipulator.MouseButton.LeftButton:
            self.__is_left_pressed = False
        elif button == Manipulator.MouseButton.RightButton:
            self.__is_right_pressed = False

        return False
    
    def on_mouse_double_clicked(self, button:Manipulator.MouseButton, screen_pos:glm.vec2, global_pos:glm.vec2)->bool:
        self.__offset = glm.vec2(0, 0)
        self.__update_camera()
        return True

    def on_mouse_moved(self, screen_pos:glm.vec2, global_pos:glm.vec2):
        if self.__is_left_pressed:
            d = global_pos - self.__left_press_global_posF
            dx = d.x
            dy = d.y

            d_pitch = dy / self.camera.screen.height() * 200 * self.sensitivity
            d_yaw = -dx / self.camera.screen.width() * 200 * self.sensitivity
            
            self.__azimuth_deg = self.__left_press_azimuth_deg + d_yaw
            self.__elevation_deg = self.__left_press_elevation_deg + d_pitch
            self.__update_camera()

            return True
        
        elif self.__is_right_pressed:
            d = global_pos - self.__right_press_global_posF
            dx = -d.x
            dy = d.y

            offset_delta = glm.vec2()
            offset_delta.x = dx / self.camera.screen.width() * 2 * self.__distance * self.camera.tan_half_fov * self.camera.aspect
            offset_delta.y = dy / self.camera.screen.height() * 2 * self.__distance * self.camera.tan_half_fov
            self.__offset = self.__right_press_offset + offset_delta
            self.__update_camera()

            return True

        return False

    def on_wheel_scrolled(self, angle:glm.vec2, screen_pos:glm.vec2, global_pos:glm.vec2):
        if self.__is_left_pressed or self.__is_right_pressed:
            return False
        
        n = angle.y/120
        if self.camera.projection_mode.value == 0:
            if n > 0:
                self.__distance *= 0.8
            else:
                self.__distance *= 1.2
        else:
            if n > 0:
                self.camera.height *= 0.8
            else:
                self.camera.height *= 1.2

        self.__update_camera()
        return True

    def on_key_pressed(self, key:Manipulator.Key)->bool:
        if key == Manipulator.Key.Key_R:
            polygon_mode = self.camera.screen.renderer.render_hint.polygon_mode
            if polygon_mode in [GL.GL_FILL, RenderHint.inherit]:
                self.camera.screen.renderer.render_hint.polygon_mode = GL.GL_LINE
                self.camera.screen.renderer.render_hintline_width = 1
            elif polygon_mode == GL.GL_LINE:
                self.camera.screen.renderer.render_hint.polygon_mode = GL.GL_POINT
                self.camera.screen.renderer.render_hintpoint_size = 1.5
            elif polygon_mode == GL.GL_POINT:
                self.camera.screen.renderer.render_hint.polygon_mode = GL.GL_FILL
            return True
        elif key == Manipulator.Key.Key_P:
            now = datetime.datetime.now()
            file_name = "capture_" + now.strftime("%Y-%m-%d_%H-%M-%S") + ".png"
            self.camera.screen.capture(file_name)

        return False