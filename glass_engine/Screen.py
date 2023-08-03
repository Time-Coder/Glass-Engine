from .Manipulators.Manipulator import Manipulator
from .Manipulators.SceneRoamManipulator import SceneRoamManipulator
from .Renderers.Renderer import Renderer
from .Renderers.ForwardRenderer import ForwardRenderer
from .Filters import Filters, SingleShaderFilter
from .Frame import Frame

from glass import GLConfig, FBO, RBO, sampler2DMS, sampler2D, RenderHint, SSBO, UBO
from glass.utils import checktype

from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6.QtGui import QMouseEvent, QKeyEvent, QCursor, QWheelEvent, QSurfaceFormat, QFont, QColor, QPen
from PyQt6.QtCore import Qt, QPointF, QPoint, QTimerEvent, pyqtSignal, QSize
from PyQt6.QtWidgets import QApplication

import time
import glm
import sys
from OpenGL import GL

class SlideAverageFilter:

    @checktype
    def __init__(self, window_width:int=10):
        self._current_sum = 0
        self._window_width = window_width
        self._data_list = []

    def __call__(self, new_value):
        if len(self._data_list) >= self._window_width:
            old_value = self._data_list.pop(0)
            self._current_sum -= old_value

        self._data_list.append(new_value)
        self._current_sum += new_value

        return self._current_sum / len(self._data_list)
    
    @property
    def window_width(self):
        return self._window_width
    
    @window_width.setter
    @checktype
    def window_width(self, window_width:int):
        self._window_width = window_width

class Screen(QOpenGLWidget):

    mouse_pressed = pyqtSignal(Manipulator.MouseButton, glm.vec2, glm.vec2)
    mouse_released = pyqtSignal(Manipulator.MouseButton, glm.vec2, glm.vec2)
    mouse_double_clicked = pyqtSignal(Manipulator.MouseButton, glm.vec2, glm.vec2)
    mouse_moved = pyqtSignal(glm.vec2, glm.vec2)
    wheel_scrolled = pyqtSignal(glm.vec2, glm.vec2, glm.vec2)
    key_pressed = pyqtSignal(Manipulator.Key)
    key_released = pyqtSignal(Manipulator.Key)
    key_repeated = pyqtSignal(set)
    frame_started = pyqtSignal()
    frame_ended = pyqtSignal()

    __app = None
    __has_exec = False

    def __new__(cls, *args, **kwargs):
        if QApplication.instance() is None:
            Screen.__app = QApplication(sys.argv)

        instance = QOpenGLWidget.__new__(cls, *args, **kwargs)
        return instance

    def __init__(self, camera, parent=None):
        QOpenGLWidget.__init__(self, parent)

        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self._samples = 1
    
        self._pressed_keys = set()
        self._last_frame_time = 0
        self._is_cursor_hiden = False
        self._hide_cursor_global_posF = QPointF(0, 0)
        self._last_cursor_global_pos = QPoint(0, 0)
        self._fps = 0
        self._smooth_fps = 0
        self._fps_filter = SlideAverageFilter()
        self.__before_filter_fbo = None
        self.__before_filter_fbo_ms = None
        self._is_gl_init = False
        self._screen_image = None
        
        self.camera = camera
        self._manipulator = None
        self.manipulator = SceneRoamManipulator()
        self._renderer = ForwardRenderer()
        
        self.__render_hint = RenderHint()
        self._listen_cursor_timer = self.startTimer(10)

    def sizeHint(self):
        return QSize(800, 600)

    @property
    def samples(self):
        return self._samples
    
    @samples.setter
    def samples(self, samples:int):
        surface_format = QSurfaceFormat()
        surface_format.setSamples(samples)
        self.setFormat(surface_format)
        if not self._is_gl_init:
            self._samples = samples

    @property
    def renderer(self):
        return self._renderer
    
    @renderer.setter
    def renderer(self, renderer:Renderer):
        if self._renderer is renderer:
            return
        
        should_update = False
        self._renderer = renderer
        if self._is_gl_init and renderer is not None:
            self.makeCurrent()
            should_update = self._renderer.startup(self.camera, self.camera.scene)

        if should_update:
            self._screen_image = None
            self.update()

    @property
    def render_hint(self):
        return self.__render_hint
    
    @render_hint.setter
    @checktype
    def render_hint(self, hint:RenderHint):
        if hint is None:
            hint = RenderHint()

        self.__render_hint = hint

    def initializeGL(self):
        self.makeCurrent()

        if self.camera.scene is None:
            raise RuntimeError(f"{self.camera} is not in any scene, please add it to one scene before show it's screen")
        
        if not self._is_gl_init and self.renderer is not None:
            self.renderer.startup(self.camera, self.camera.scene)

        self._is_gl_init = True

    def makeCurrent(self):
        QOpenGLWidget.makeCurrent(self)

        GLConfig.buffered_current_context = GLConfig.current_context
        SSBO.makeCurrent()
        UBO.makeCurrent()

    def paintGL(self):
        self.makeCurrent()

        self.frame_started.emit()

        should_update_scene = self.camera.scene.generate_meshes()
        should_update_filter = False

        with self.render_hint:
            GLConfig.clear_buffers()
            if not self.renderer.filters.has_valid:
                with self.renderer.render_hint:
                    should_update_scene = self.renderer.render(self.camera, self.camera.scene) or should_update_scene
            else:
                if self._screen_image is None or should_update_scene:
                    with self._before_filter_fbo:
                        with self.renderer.render_hint:
                            should_update_scene = self.renderer.render(self.camera, self.camera.scene) or should_update_scene

                    self._screen_image = self._before_filter_fbo.resolved.color_attachment(0)
                    self.renderer.filters.screen_update_time = time.time()

                should_update_filter = self.renderer.filters.draw(self._screen_image)

        self.__calc_fps()
        self.frame_ended.emit()

        if should_update_scene or should_update_filter:
            if should_update_scene:
                self._screen_image = None
                
            self.update()

    @property
    def _before_filter_fbo(self):
        screen_size = GLConfig.screen_size
        if self.samples > 1:
            if self.__before_filter_fbo_ms is not None:
                self.__before_filter_fbo_ms.resize(screen_size.x, screen_size.y, self.samples)
            else:
                self.__before_filter_fbo_ms = FBO(screen_size.x, screen_size.y, self.samples)
                self.__before_filter_fbo_ms.attach(0, sampler2DMS, GL.GL_RGBA32F)
                self.__before_filter_fbo_ms.attach(GL.GL_DEPTH_STENCIL_ATTACHMENT, RBO, GL.GL_DEPTH_STENCIL)
            return self.__before_filter_fbo_ms
        else:
            if self.__before_filter_fbo is not None:
                self.__before_filter_fbo.resize(screen_size.x, screen_size.y)
            else:
                self.__before_filter_fbo = FBO(screen_size.x, screen_size.y)
                self.__before_filter_fbo.attach(0, sampler2D, GL.GL_RGBA32F)
                self.__before_filter_fbo.attach(GL.GL_DEPTH_STENCIL_ATTACHMENT, RBO, GL.GL_DEPTH_STENCIL)
            return self.__before_filter_fbo
        
    @staticmethod
    def __mouse_parameters(mouse_event:QMouseEvent):
        button = Manipulator.MouseButton(mouse_event.button().value)
        screen_pos = mouse_event.position()
        screen_pos = glm.vec2(screen_pos.x(), screen_pos.y())
        global_pos = mouse_event.globalPosition()
        global_pos = glm.vec2(global_pos.x(), global_pos.y())
        return button, screen_pos, global_pos
    
    @staticmethod
    def __wheel_parameters(wheel_event:QWheelEvent):
        angle = glm.vec2(wheel_event.angleDelta().x(), wheel_event.angleDelta().y())
        screen_pos = wheel_event.position()
        screen_pos = glm.vec2(screen_pos.x(), screen_pos.y())
        global_pos = wheel_event.globalPosition()
        global_pos = glm.vec2(global_pos.x(), global_pos.y())
        return angle, screen_pos, global_pos

    def mousePressEvent(self, mouse_event:QMouseEvent)->None:
        button, screen_pos, global_pos = Screen.__mouse_parameters(mouse_event)

        self.makeCurrent()

        should_update = False
        if self.manipulator is not None:
            should_update = self.manipulator.on_mouse_pressed(button, screen_pos, global_pos)

        self.mouse_pressed.emit(button, screen_pos, global_pos)

        if should_update:
            self._screen_image = None
            self.update()

    def mouseReleaseEvent(self, mouse_event: QMouseEvent)->None:
        button, screen_pos, global_pos = Screen.__mouse_parameters(mouse_event)

        self.makeCurrent()

        should_update = False
        if self.manipulator is not None:
            should_update = self.manipulator.on_mouse_released(button, screen_pos, global_pos)
        
        self.mouse_released.emit(button, screen_pos, global_pos)
        
        if should_update:
            self._screen_image = None
            self.update()

    def mouseDoubleClickEvent(self, mouse_event:QMouseEvent)->None:
        button, screen_pos, global_pos = Screen.__mouse_parameters(mouse_event)

        self.makeCurrent()

        should_update = False
        if self.manipulator is not None:
            should_update = self.manipulator.on_mouse_double_clicked(button, screen_pos, global_pos)
        
        self.mouse_double_clicked.emit(button, screen_pos, global_pos)
        
        if should_update:
            self._screen_image = None
            self.update()

    def __mouseMoveEvent(self, screen_pos:glm.vec2, global_pos:glm.vec2)->bool:
        self.makeCurrent()

        should_update = False
        if self.manipulator is not None:
            should_update = self.manipulator.on_mouse_moved(screen_pos, global_pos)

        self.mouse_moved.emit(screen_pos, global_pos)

        if should_update:
            self._screen_image = None
            self.update()

    def keyPressEvent(self, key_event:QKeyEvent)->None:
        key = Manipulator.Key(key_event.key())
        if key not in self._pressed_keys:
            self._pressed_keys.add(key)
        
        self.makeCurrent()

        should_update = False
        if self.manipulator is not None:
            should_update = self.manipulator.on_key_pressed(key)

        self.key_pressed.emit(key)

        if should_update:
            self._screen_image = None
            self.update()

    def keyReleaseEvent(self, key_event: QKeyEvent)->None:
        key = Manipulator.Key(key_event.key())
        if key in self._pressed_keys:
            self._pressed_keys.remove(key)

        self.makeCurrent()

        should_update = False
        if self.manipulator is not None:
            should_update = self.manipulator.on_key_released(key)

        self.key_released.emit(key)

        if should_update:
            self._screen_image = None
            self.update()

    def __keyRepeateEvent(self, keys:set[Manipulator.Key])->bool:
        self.makeCurrent()

        should_update = False
        if self.manipulator is not None:
            should_update = self.manipulator.on_key_repeated(keys)

        self.key_repeated.emit(keys)

        if should_update:
            self._screen_image = None
            self.update()

    def wheelEvent(self, wheel_event:QWheelEvent)->None:
        angle, screen_pos, global_pos = Screen.__wheel_parameters(wheel_event)

        self.makeCurrent()

        should_update = False
        if self.manipulator is not None:
            should_update = self.manipulator.on_wheel_scrolled(angle, screen_pos, global_pos)
        
        self.wheel_scrolled.emit(angle, screen_pos, global_pos)

        if should_update:
            self._screen_image = None
            self.update()
    
    def __calc_fps(self):
        current_time = time.time()
        dt = current_time - self._last_frame_time
        self._last_frame_time = current_time
        if dt < 1:
            self._fps = 1 / dt
            self._smooth_fps = self._fps_filter(self._fps)

    def hide_cursor(self):
        if self._is_cursor_hiden:
            return
        
        self._is_cursor_hiden = True
        self._hide_cursor_global_posF = QPointF(QCursor.pos())
        self.setCursor(Qt.CursorShape.BlankCursor)
        return self._hide_cursor_global_posF

    def show_cursor(self):
        if not self._is_cursor_hiden:
            return
        
        self._is_cursor_hiden = False
        self.unsetCursor()

    def show(self):
        QOpenGLWidget.show(self)
        if Screen.__app is not None and \
           not Screen.__has_exec:
            Screen.__app.exec()
            Screen.__has_exec = True

    @property
    def is_cursor_hiden(self):
        return self._is_cursor_hiden

    @property
    def fps(self):
        return self._fps
    
    @property
    def smooth_fps(self):
        return self._smooth_fps

    @property
    def manipulator(self):
        return self._manipulator
    
    @manipulator.setter
    def manipulator(self, manipulator:Manipulator):
        if self._manipulator is manipulator:
            return
        
        if manipulator is None:
            self._manipulator._camera = None
            self._manipulator = None
            return

        if manipulator.camera is not None:
            manipulator.camera.screen.manipulator = None

        self._manipulator = manipulator
        manipulator._camera = self.camera
        should_update = manipulator.on_start()
        if should_update:
            self._screen_image = None
            self.update()

    def timerEvent(self, timer_event: QTimerEvent)->None:
        if timer_event.timerId() == self._listen_cursor_timer:
            cursor_global_pos = QCursor.pos()
            last_global_pos = self._last_cursor_global_pos
            self._last_cursor_global_pos = cursor_global_pos

            cursor_global_posF = QPointF(cursor_global_pos)

            should_update = sampler2D.should_update()
            if self._pressed_keys:
                should_update = self.__keyRepeateEvent(self._pressed_keys) or should_update

            if self._is_cursor_hiden:
                center_global_posF = self.mapToGlobal(QPointF(self.width()/2, self.height()/2))
                offset = cursor_global_posF - center_global_posF
                buffer = 100
                if offset.x() > buffer or offset.x() < -buffer or \
                    offset.y() > buffer or offset.y() < -buffer:
                    self._hide_cursor_global_posF.x = self._hide_cursor_global_posF.x() - offset.x()
                    self._hide_cursor_global_posF.y = self._hide_cursor_global_posF.y() - offset.y()
                    QCursor.setPos(center_global_posF.toPoint())
                    cursor_global_posF = center_global_posF
            
            if cursor_global_pos != last_global_pos:
                screen_pos = self.mapFromGlobal(cursor_global_posF)
                screen_pos = glm.vec2(screen_pos.x(), screen_pos.y())
                global_pos = glm.vec2(cursor_global_posF.x(), cursor_global_posF.y())
                should_update = self.__mouseMoveEvent(screen_pos, global_pos) or should_update

            if should_update:
                self._screen_image = None
                self.update()
            
