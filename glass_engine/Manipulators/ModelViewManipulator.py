from .Manipulator import Manipulator

from glass.RenderHints import RenderHints
from glass.utils import checktype

from OpenGL import GL
import math
import glm
import datetime


class ModelViewManipulator(Manipulator):

    def __init__(self, distance: float = 5, azimuth: float = 0, elevation: float = 0):
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
        self.drag_sensitivity: float = 1
        self.scroll_sensitivity: float = 1

    @property
    def distance(self) -> float:
        return self.__distance

    @distance.setter
    @checktype
    def distance(self, distance: float):
        self.__distance = distance
        self.__update_camera()
        self.camera.screen.update()

    @property
    def azimuth(self):
        return self.__azimuth

    @azimuth.setter
    @checktype
    def azimuth(self, azimuth: float):
        self.__azimuth = azimuth
        self.__update_camera()
        self.camera.screen.update()

    @property
    def elevation(self):
        return self.__elevation

    @elevation.setter
    @checktype
    def elevation(self, elevation: float):
        self.__elevation = elevation
        self.__update_camera()
        self.camera.screen.update()

    def __update_camera(self):
        azimuth = self.__azimuth / 180 * math.pi
        elevation = self.__elevation / 180 * math.pi

        self.camera.position.x = (
            self.__distance * math.cos(elevation) * math.sin(azimuth)
        )
        self.camera.position.y = (
            -self.__distance * math.cos(elevation) * math.cos(azimuth)
        )
        self.camera.position.z = self.__distance * math.sin(elevation)

        if glm.length(self.__offset) > 1e-6:
            right = glm.vec3(math.cos(azimuth), math.sin(azimuth), 0)
            forward = glm.vec3(
                -math.sin(elevation) * math.sin(azimuth),
                math.sin(elevation) * math.cos(azimuth),
                math.cos(elevation),
            )
            self.camera.position += self.__offset.x * right + self.__offset.y * forward

        self.camera.pitch = -self.__elevation
        self.camera.yaw = self.__azimuth

    def startup(self):
        self.__update_camera()

    def on_mouse_pressed(
        self,
        button: Manipulator.MouseButton,
        screen_pos: glm.vec2,
        global_pos: glm.vec2,
    ):
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
            self.drag_sensitivity /= pow(2, 1 / 2)
        elif button == Manipulator.MouseButton.XButton2:
            self.drag_sensitivity *= pow(2, 1 / 2)

    def on_mouse_released(
        self,
        button: Manipulator.MouseButton,
        screen_pos: glm.vec2,
        global_pos: glm.vec2,
    ):
        if button == Manipulator.MouseButton.LeftButton:
            self.__is_left_pressed = False
            if self.__left_press_global_posF == global_pos:
                x = screen_pos.x
                y = screen_pos.y
                width = self.camera.screen.width()
                height = self.camera.screen.height()
                s = x / (width - 1)
                t = 1 - y / (height - 1)
                self.camera.lens.focus_tex_coord = glm.vec2(s, t)
        elif button == Manipulator.MouseButton.RightButton:
            self.__is_right_pressed = False

    def on_mouse_double_clicked(
        self,
        button: Manipulator.MouseButton,
        screen_pos: glm.vec2,
        global_pos: glm.vec2,
    ) -> None:
        if button == Manipulator.MouseButton.LeftButton:
            self.__offset = glm.vec2(0, 0)
            self.camera.fov = 45
            self.__update_camera()

    def on_mouse_moved(self, screen_pos: glm.vec2, global_pos: glm.vec2)->None:
        if self.__is_left_pressed:
            d = global_pos - self.__left_press_global_posF
            dx = d.x
            dy = d.y

            d_pitch = dy / self.camera.screen.height() * 200 * self.drag_sensitivity
            d_yaw = -dx / self.camera.screen.width() * 200 * self.drag_sensitivity

            self.__azimuth = self.__left_press_azimuth + d_yaw
            self.__elevation = self.__left_press_elevation + d_pitch
            self.__update_camera()

        elif self.__is_right_pressed:
            d = global_pos - self.__right_press_global_posF
            dx = -d.x
            dy = d.y

            offset_delta = glm.vec2()
            offset_delta.x = (
                dx
                / self.camera.screen.width()
                * 2
                * self.__distance
                * self.camera.tan_half_fov
                * self.camera.aspect
            )
            offset_delta.y = (
                dy
                / self.camera.screen.height()
                * 2
                * self.__distance
                * self.camera.tan_half_fov
            )
            self.__offset = self.__right_press_offset + offset_delta
            self.__update_camera()

    def on_wheel_scrolled(
        self, angle: glm.vec2, screen_pos: glm.vec2, global_pos: glm.vec2
    ):
        n = self.scroll_sensitivity * angle.y / 120
        scale = pow(2, n / 6)
        if self.camera.projection_mode.value == 0:
            self.camera.fov /= scale
        else:
            self.camera.height /= scale

    def on_key_pressed(self, key: Manipulator.Key) -> None:
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
        elif key == Manipulator.Key.Key_P:
            now = datetime.datetime.now()
            file_name = "capture_" + now.strftime("%Y-%m-%d_%H-%M-%S") + ".png"
            self.camera.screen.capture(file_name)
        elif key == Manipulator.Key.Key_O:
            self.camera.screen.SSAO.enabled = not self.camera.screen.SSAO.enabled
        elif key == Manipulator.Key.Key_M:
            self.camera.screen.DOF.enabled = not self.camera.screen.DOF.enabled

    def on_key_repeated(self, keys) -> None:
        if Manipulator.Key.Key_W in keys and Manipulator.Key.Key_S not in keys:
            self.__distance /= pow(2, 1 / self.camera.screen.smooth_fps)
            self.__update_camera()
        if Manipulator.Key.Key_S in keys and Manipulator.Key.Key_W not in keys:
            self.__distance *= pow(2, 1 / self.camera.screen.smooth_fps)
            self.__update_camera()
        if Manipulator.Key.Key_A in keys and Manipulator.Key.Key_D not in keys:
            self.__offset.x -= (
                0.5
                / self.camera.screen.smooth_fps
                * self.__distance
                * self.camera.tan_half_fov
            )
            self.__update_camera()
        if Manipulator.Key.Key_D in keys and Manipulator.Key.Key_A not in keys:
            self.__offset.x += (
                0.5
                / self.camera.screen.smooth_fps
                * self.__distance
                * self.camera.tan_half_fov
            )
            self.__update_camera()
        if Manipulator.Key.Key_E in keys and Manipulator.Key.Key_C not in keys:
            self.__offset.y += (
                0.5
                / self.camera.screen.smooth_fps
                * self.__distance
                * self.camera.tan_half_fov
            )
            self.__update_camera()
        if Manipulator.Key.Key_C in keys and Manipulator.Key.Key_E not in keys:
            self.__offset.y -= (
                0.5
                / self.camera.screen.smooth_fps
                * self.__distance
                * self.camera.tan_half_fov
            )
            self.__update_camera()
        if Manipulator.Key.Key_F in keys:
            screen = self.camera.screen
            screen.update()
            print("fps:", screen.fps, "draw calls:", screen.draw_calls)

