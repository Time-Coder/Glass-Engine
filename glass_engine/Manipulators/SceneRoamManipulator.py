from .Manipulator import Manipulator
from glass.RenderHints import RenderHints

import glm
from OpenGL import GL
import copy
import datetime

class SceneRoamManipulator(Manipulator):

    def __init__(self):
        Manipulator.__init__(self)
        
        self._is_right_pressed = False
        self._right_press_global_pos = glm.vec2(0, 0)
        self._right_press_yaw = 0
        self._right_press_pitch = 0

        self._is_left_pressed = False
        self._left_press_global_pos = glm.vec2(0, 0)
        self._left_press_yaw = 0
        self._left_press_pitch = 0

        self._hide_cursor_global_pos = glm.vec2(0, 0)
        self._hide_cursor_yaw = 0
        self._hide_cursor_pitch = 0
        self._video_writer = None
        self._moving_speed = 1

    def on_mouse_pressed(self, button:Manipulator.MouseButton, screen_pos:glm.vec2, global_pos:glm.vec2):
        if button == Manipulator.MouseButton.XButton1:
            self._moving_speed /= pow(2, 1/2)
        elif button == Manipulator.MouseButton.XButton2:
            self._moving_speed *= pow(2, 1/2)
        
        if not self.camera.screen.is_cursor_hiden:
            if button == Manipulator.MouseButton.RightButton:
                self._is_right_pressed = True
                self._right_press_global_pos = global_pos
                self._right_press_yaw = self.camera.yaw
                self._right_press_pitch = self.camera.pitch
            elif button == Manipulator.MouseButton.LeftButton:
                self._is_left_pressed = True
                self._left_press_global_pos = global_pos
                self._left_press_yaw = self.camera.yaw
                self._left_press_pitch = self.camera.pitch
                self._left_press_camera_pos = copy.deepcopy(self.camera.position)

        return False

    def on_mouse_released(self, button:Manipulator.MouseButton, screen_pos:glm.vec2, global_pos:glm.vec2):
        if button == Manipulator.MouseButton.RightButton:
            self._is_right_pressed = False
        elif button == Manipulator.MouseButton.LeftButton:
            self._is_left_pressed = False
            if self._left_press_global_pos == global_pos:
                x = screen_pos.x
                y = screen_pos.y
                width = self.camera.screen.width()
                height = self.camera.screen.height()
                s = x/(width-1)
                t = 1 - y/(height-1)
                self.camera.lens.focus_tex_coord = glm.vec2(s, t)
                return True

        return False

    def on_mouse_moved(self, screen_pos:glm.vec2, global_pos:glm.vec2):
        if self.camera.screen.is_cursor_hiden:
            d = global_pos - self._hide_cursor_global_pos
            dx = d.x
            dy = d.y

            d_pitch = dy / self.camera.screen.height() * self.camera.fov_y
            d_yaw = dx / self.camera.screen.width() * self.camera.fov_x

            self.camera.yaw = self._hide_cursor_yaw - d_yaw
            self.camera.pitch = self._hide_cursor_pitch - d_pitch
            return True
        elif self._is_right_pressed:
            d = global_pos - self._right_press_global_pos
            dx = d.x
            dy = d.y

            d_pitch = dy / self.camera.screen.height() * self.camera.fov_y
            d_yaw = dx / self.camera.screen.width() * self.camera.fov_x
            
            self.camera.yaw = self._right_press_yaw + d_yaw
            self.camera.pitch = self._right_press_pitch + d_pitch
            return True
        elif self._is_left_pressed:
            d = global_pos - self._left_press_global_pos
            dx = d.x/100
            dy = d.y/100

            self.camera.position = self._left_press_camera_pos + self.camera.orientation * glm.vec3(-dx, 0, dy)
            return True
        
        return False

    def on_wheel_scrolled(self, angle:glm.vec2, screen_pos:glm.vec2, global_pos:glm.vec2):
        n = angle.y/120
        scale = pow(2, n/6)
        if self.camera.projection_mode.value == 0:
            self.camera.fov /= scale
        else:
            self.camera.height /= scale

        return True

    def on_key_pressed(self, key:Manipulator.Key)->bool:
        if key in [Manipulator.Key.Key_Enter, Manipulator.Key.Key_Return]:
            self._hide_cursor_global_pos = self.camera.screen.hide_cursor()
            self._hide_cursor_yaw = self.camera.yaw
            self._hide_cursor_pitch = self.camera.pitch
        elif key == Manipulator.Key.Key_Escape:
            self.camera.screen.show_cursor()
        elif key == Manipulator.Key.Key_R:
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
        elif key == Manipulator.Key.Key_O:
            self.camera.screen.SSAO.enabled = (not self.camera.screen.SSAO.enabled)
            return True
        elif key == Manipulator.Key.Key_M:
            self.camera.screen.DOF.enabled = (not self.camera.screen.DOF.enabled)
            return True
        elif key == Manipulator.Key.Key_P:
            now = datetime.datetime.now()
            file_name = "capture_" + now.strftime("%Y-%m-%d_%H-%M-%S") + ".png"
            self.camera.screen.capture(file_name)
        elif key == Manipulator.Key.Key_V:
            if self._video_writer is None:
                now = datetime.datetime.now()
                file_name = "capture_" + now.strftime("%Y-%m-%d_%H-%M-%S") + ".avi"
                self._video_writer = self.camera.screen.capture_video(file_name)
            else:
                self._video_writer.stop()
                self._video_writer = None
        
        return False

    def on_key_repeated(self, keys:set)->bool:
        if self._is_left_pressed:
            return

        d = self._moving_speed / 60
        fps = self.camera.screen.smooth_fps
        if fps > 0:
            d = self._moving_speed / fps
        if abs(d) < 1E-6:
            return False
        
        should_update = False
        if Manipulator.Key.Key_W in keys and \
           Manipulator.Key.Key_S not in keys: # 前进
            self.camera.position += self.camera.orientation * glm.vec3(0, d, 0)
            should_update = True
        if Manipulator.Key.Key_S in keys and \
            Manipulator.Key.Key_W not in keys: # 后退
            self.camera.position += self.camera.orientation * glm.vec3(0, -d, 0)
            should_update = True
        if Manipulator.Key.Key_A in keys and \
            Manipulator.Key.Key_D not in keys: # 向左
            self.camera.position += self.camera.orientation * glm.vec3(-d, 0, 0)
            should_update = True
        if Manipulator.Key.Key_D in keys and \
            Manipulator.Key.Key_A not in keys: # 向右
            self.camera.position += self.camera.orientation * glm.vec3(d, 0, 0)
            should_update = True
        if Manipulator.Key.Key_E in keys and \
            Manipulator.Key.Key_C not in keys: # 向上
            self.camera.position += self.camera.orientation * glm.vec3(0, 0, d)
            should_update = True
        if Manipulator.Key.Key_C in keys and \
            Manipulator.Key.Key_E not in keys: # 向下
            self.camera.position += self.camera.orientation * glm.vec3(0, 0, -d)
            should_update = True
        if Manipulator.Key.Key_F in keys:
            screen = self.camera.screen
            print("fps:", screen.fps, "draw calls:", screen.draw_calls)
            should_update = True

        return should_update