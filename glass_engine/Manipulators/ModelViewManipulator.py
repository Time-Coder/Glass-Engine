from .Manipulator import Manipulator
from glass.RenderHint import RenderHint

from OpenGL import GL
import math
import glm

class ModelViewManipulator(Manipulator):

    def __init__(self):
        self.__is_left_pressed = False
        self.__left_press_global_posF = glm.vec2(0, 0)
        self.__left_press_theta = 0
        self.__left_press_phi = 0

        self.__r = 0
        self.__center = glm.vec3(0, 0, 0)
        self.__theta = 0
        self.__phi = 0

    def on_mouse_pressed(self, button:Manipulator.MouseButton, screen_pos:glm.vec2, global_pos:glm.vec2):
        if button == Manipulator.MouseButton.LeftButton:
            if self.__r == 0:
                camera_pos = self.camera.abs_position
                d = self.camera.abs_orientation * glm.vec3(0, 1, 0)
                self.__r = 2
                if abs(d.z) > 1E-6:
                    self.__r = -camera_pos.z / d.z

                self.__center = camera_pos + self.__r * d

                self.__theta = self.camera.yaw
                self.__phi = -self.camera.pitch

            self.__is_left_pressed = True
            self.__left_press_global_posF = global_pos
            self.__left_press_theta = self.__theta
            self.__left_press_phi = self.__phi

        return False

    def on_mouse_released(self, button:Manipulator.MouseButton, screen_pos:glm.vec2, global_pos:glm.vec2):
        if button == Manipulator.MouseButton.LeftButton:
            self.__is_left_pressed = False

        return False

    def on_mouse_moved(self, screen_pos:glm.vec2, global_pos:glm.vec2):
        if self.__is_left_pressed:
            d = global_pos - self.__left_press_global_posF
            dx = d.x
            dy = d.y

            d_pitch = dy / self.camera.screen.height() * 200
            d_yaw = dx / self.camera.screen.width() * 200
            
            self.__theta = self.__left_press_theta - d_yaw
            self.__phi = self.__left_press_phi + d_pitch
            theta = self.__theta/180*math.pi
            phi = self.__phi/180*math.pi
            self.camera.yaw = self.__theta
            self.camera.pitch = -self.__phi
            self.camera.position.y = self.__center.y-self.__r*math.cos(phi)*math.cos(theta)
            self.camera.position.x = self.__center.x+self.__r*math.cos(phi)*math.sin(theta)
            self.camera.position.z = self.__center.z+self.__r*math.sin(phi)

            return True

        return False

    def on_wheel_scrolled(self, angle:glm.vec2, screen_pos:glm.vec2, global_pos:glm.vec2):
        if self.__r == 0:
            camera_pos = self.camera.abs_position
            d = self.camera.abs_orientation * glm.vec3(0, 1, 0)
            self.__r = 2
            if abs(d.z) > 1E-6:
                self.__r = -camera_pos.z / d.z

            self.__center = camera_pos + self.__r * d

            self.__theta = self.camera.yaw
            self.__phi = -self.camera.pitch

        n = angle.y/120
        if n > 0:
            self.__r *= 0.8
        else:
            self.__r *= 1.2
        
        theta = self.__theta/180*math.pi
        phi = self.__phi/180*math.pi
        self.camera.position.y = -self.__r*math.cos(phi)*math.cos(theta)
        self.camera.position.x = self.__r*math.cos(phi)*math.sin(theta)
        self.camera.position.z = self.__r*math.sin(phi)

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

        return False