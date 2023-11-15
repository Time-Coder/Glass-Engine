from .Manipulator import Manipulator

from glass.RenderHints import RenderHints
from glass.utils import checktype

from OpenGL import GL
import math
import glm
import datetime

class ModelViewManipulator(Manipulator):

    def __init__(self, distance:float=5, azimuth:float=0, elevation:float=0):
        Manipulator.__init__(self)
        
        self.__is_left_pressed = False
        self.__left_press_global_posF = glm.vec2(0, 0)
        self.__left_press_azimuth = 0
        self.__left_press_elevation = 0

        self.__is_right_pressed = False
        self.__right_press_global_posF = glm.vec2(0, 0)
        self.__right_press_offset = glm.vec2(0, 0)

        self.__distance = distance
        self.__azimuth = azimuth
        self.__elevation = elevation
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
        return self.__azimuth
    
    @azimuth.setter
    @checktype
    def azimuth(self, azimuth:float):
        self.__azimuth = azimuth
        self.__update_camera()
        self.camera.screen.update()

    @property
    def elevation(self):
        return self.__elevation
    
    @elevation.setter
    @checktype
    def elevation(self, elevation:float):
        self.__elevation = elevation
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
        azimuth = self.__azimuth/180*math.pi
        elevation = self.__elevation/180*math.pi

        self.camera.position.x = self.__distance*math.cos(elevation)*math.sin(azimuth)
        self.camera.position.y = -self.__distance*math.cos(elevation)*math.cos(azimuth)
        self.camera.position.z = self.__distance*math.sin(elevation)

        if glm.length(self.__offset) > 1E-6:
            right = glm.vec3(math.cos(azimuth), math.sin(azimuth), 0)
            forward = glm.vec3(-math.sin(elevation) * math.sin(azimuth), math.sin(elevation) * math.cos(azimuth), math.cos(elevation))
            self.camera.position += (self.__offset.x * right + self.__offset.y * forward)

        self.camera.pitch = -self.__elevation
        self.camera.yaw = self.__azimuth

    def startup(self):
        self.__update_camera()

    def on_mouse_pressed(self, button:Manipulator.MouseButton, screen_pos:glm.vec2, global_pos:glm.vec2):
        if button == Manipulator.MouseButton.LeftButton:
            self.__is_left_pressed = True
            self.__left_press_global_posF = global_pos
            self.__left_press_azimuth = self.__azimuth
            self.__left_press_elevation = self.__elevation
        elif button == Manipulator.MouseButton.RightButton:
            self.__is_right_pressed = True
            self.__right_press_global_posF = global_pos
            self.__right_press_offset = self.__offset
        elif button == Manipulator.MouseButton.XButton1:
            self.__sensitivity /= pow(2, 1/2)
        elif button == Manipulator.MouseButton.XButton2:
            self.__sensitivity *= pow(2, 1/2)

        return False

    def on_mouse_released(self, button:Manipulator.MouseButton, screen_pos:glm.vec2, global_pos:glm.vec2):
        if button == Manipulator.MouseButton.LeftButton:
            self.__is_left_pressed = False
            if self.__left_press_global_posF == global_pos:
                x = screen_pos.x
                y = screen_pos.y
                width = self.camera.screen.width()
                height = self.camera.screen.height()
                s = x/(width-1)
                t = 1 - y/(height-1)
                self.camera.lens.focus_tex_coord = glm.vec2(s, t)
                return True
        elif button == Manipulator.MouseButton.RightButton:
            self.__is_right_pressed = False

        return False
    
    def on_mouse_double_clicked(self, button:Manipulator.MouseButton, screen_pos:glm.vec2, global_pos:glm.vec2)->bool:
        if button == Manipulator.MouseButton.LeftButton:
            self.__offset = glm.vec2(0, 0)
            self.__update_camera()
            return True
        
        return False

    def on_mouse_moved(self, screen_pos:glm.vec2, global_pos:glm.vec2):
        if self.__is_left_pressed:
            d = global_pos - self.__left_press_global_posF
            dx = d.x
            dy = d.y

            d_pitch = dy / self.camera.screen.height() * 200 * self.sensitivity
            d_yaw = -dx / self.camera.screen.width() * 200 * self.sensitivity
            
            self.__azimuth = self.__left_press_azimuth + d_yaw
            self.__elevation = self.__left_press_elevation + d_pitch
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
        scale = pow(2, n/6)
        if self.camera.projection_mode.value == 0:
            self.camera.fov /= scale
        else:
            self.camera.height /= scale

        self.__update_camera()
        return True

    def on_key_pressed(self, key:Manipulator.Key)->bool:
        if key == Manipulator.Key.Key_R:
            polygon_mode = self.camera.screen.render_hints.polygon_mode
            if polygon_mode in [GL.GL_FILL, RenderHints.inherit]:
                self.camera.screen.render_hints.polygon_mode = GL.GL_LINE
                self.camera.screen.render_hints.line_width = 1
            elif polygon_mode == GL.GL_LINE:
                self.camera.screen.render_hints.polygon_mode = GL.GL_POINT
                self.camera.screen.render_hints.point_size = 1.5
            elif polygon_mode == GL.GL_POINT:
                self.camera.screen.render_hints.polygon_mode = GL.GL_FILL
            return True
        elif key == Manipulator.Key.Key_P:
            now = datetime.datetime.now()
            file_name = "capture_" + now.strftime("%Y-%m-%d_%H-%M-%S") + ".png"
            self.camera.screen.capture(file_name)
        elif key == Manipulator.Key.Key_O:
            self.camera.screen.SSAO.enabled = (not self.camera.screen.SSAO.enabled)
            return True
        elif key == Manipulator.Key.Key_M:
            self.camera.screen.DOF.enabled = (not self.camera.screen.DOF.enabled)
            return True
        
    def on_key_repeated(self, keys)->bool:
        should_update = False
        if Manipulator.Key.Key_W in keys and \
           Manipulator.Key.Key_S not in keys:
            self.__distance /= pow(2, 1/self.camera.screen.smooth_fps)
            self.__update_camera()
            should_update = True
        if Manipulator.Key.Key_S in keys and \
             Manipulator.Key.Key_W not in keys:
            self.__distance *= pow(2, 1/self.camera.screen.smooth_fps)
            self.__update_camera()
            should_update = True
        if Manipulator.Key.Key_A in keys and \
             Manipulator.Key.Key_D not in keys:
            self.__offset.x -= 0.5/self.camera.screen.smooth_fps * self.__distance * self.camera.tan_half_fov
            self.__update_camera()
            should_update = True
        if Manipulator.Key.Key_D in keys and \
             Manipulator.Key.Key_A not in keys:
            self.__offset.x += 0.5/self.camera.screen.smooth_fps * self.__distance * self.camera.tan_half_fov
            self.__update_camera()
            should_update = True
        if Manipulator.Key.Key_E in keys and \
             Manipulator.Key.Key_C not in keys:
            self.__offset.y += 0.5/self.camera.screen.smooth_fps * self.__distance * self.camera.tan_half_fov
            self.__update_camera()
            should_update = True
        if Manipulator.Key.Key_C in keys and \
             Manipulator.Key.Key_E not in keys:
            self.__offset.y -= 0.5/self.camera.screen.smooth_fps * self.__distance * self.camera.tan_half_fov
            self.__update_camera()
            should_update = True
        if Manipulator.Key.Key_F in keys:
            screen = self.camera.screen
            print("fps:", screen.fps, "draw calls:", screen.draw_calls)
            should_update = True

        return should_update