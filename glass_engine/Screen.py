from .Manipulators.Manipulator import Manipulator
from .Renderers.Renderer import Renderer
from .Frame import Frame

from glass import GLConfig, FBO, RBO, sampler2DMS, sampler2D, RenderHint, SSBO, UBO
from glass.utils import checktype, extname, di

from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6.QtGui import QMouseEvent, QKeyEvent, QCursor, QWheelEvent, QSurfaceFormat, QPainter, QPen, QColor
from PyQt6.QtCore import Qt, QPointF, QPoint, QTimerEvent, pyqtSignal, QSize
from PyQt6.QtWidgets import QApplication

import queue
import time
import glm
import sys
from OpenGL import GL
import numpy as np
import os
import cv2
import threading
import math

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

def convert_to_image(data, viewport):
    if viewport[0] != 0 or \
       viewport[1] != 0 or \
       viewport[2] != data.shape[1] or \
       viewport[3] != data.shape[0]:
        width_pad = max(viewport[0] + viewport[2] - data.shape[1], 0)
        height_pad = max(viewport[1] + viewport[3] - data.shape[0], 0)
        if len(data.shape) == 2:
            if width_pad > 0 or height_pad > 0:
                data = np.pad(data, ((height_pad,0), (0,width_pad)))
            data = data[viewport[1]:viewport[1]+viewport[3], viewport[0]:viewport[0]+viewport[2]]
        else:
            if width_pad > 0 or height_pad > 0:
                data = np.pad(data, ((height_pad,0), (0,width_pad), (0, 0)))
            data = data[viewport[1]:viewport[1]+viewport[3], viewport[0]:viewport[0]+viewport[2], :]

    image = data
    if "float" in str(data.dtype):
        image = np.clip(255*data, 0, 255)

    image = image.astype(np.uint8)
    image = cv2.flip(image, 0)

    channels = (1 if len(image.shape) < 3 else image.shape[2])
    if channels == 3:
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    elif channels == 4:
        image = cv2.cvtColor(image, cv2.COLOR_RGBA2BGR)

    return image

class VideoWriter:
    def __init__(self, screen_video_writers, file_name:str, fourcc, viewport:tuple, fps:float):
        self._screen_video_writers = screen_video_writers

        self._cv_video_writer = cv2.VideoWriter(file_name, fourcc, fps, (viewport[2], viewport[3]))
        self._viewport = viewport
        self._last_frame = None
        self._frame_queue = queue.Queue()
        self._start_time = time.time()
        self._stop_time = float("inf")
        self._dt = 1/fps
        self._writing_thread = threading.Thread(target=self._writing_loop, daemon=True)
        self._writing_thread.start()

    def __del__(self):
        self.stop()

    def stop(self):
        if math.isinf(self._stop_time):
            self._stop_time = time.time()
            self._frame_queue.put(None)

    def _writing_loop(self):
        t = self._start_time
        while t < self._stop_time:
            frame = self._frame_queue.get()
            if frame is None:
                if self._last_frame is None:
                    break

                while t < self._stop_time:
                    self._cv_video_writer.write(self._last_frame[1])
                    t += self._dt

                break
            image = convert_to_image(frame[1], self._viewport)

            if self._last_frame is None:
                self._last_frame = (frame[0], image)

            while t <= min(self._stop_time, frame[0]):
                self._cv_video_writer.write(self._last_frame[1])
                t += self._dt

            self._last_frame = (frame[0], image)

        self._cv_video_writer.release()
        try:
            self._screen_video_writers.remove(self)
        except:
            pass

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
        self._samples_set_by_user = False
    
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
        self._before_filter_image = None
        self._video_writers = []
        self._background_color = glm.vec4(0, 0, 0, 0)
        
        self._camera_id = id(camera)

        self._manipulator = None
        self._renderer = None
        
        self.__render_hint = RenderHint()
        self._listen_cursor_timer = self.startTimer(10)

    @property
    def background_color(self):
        return self._background_color
        
    @background_color.setter
    @checktype
    def background_color(self, color:(glm.vec4,glm.vec3)):
        if isinstance(color, glm.vec3):
            color = glm.vec4(color, 1)

        self._background_color = color

    def update(self):
        self._before_filter_image = None
        QOpenGLWidget.update(self)

    def _update(self):
        QOpenGLWidget.update(self)

    def sizeHint(self):
        return QSize(800, 600)

    @property
    def camera(self):
        return di(self._camera_id)

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
            self._samples_set_by_user = True

    @property
    def renderer(self):
        return self._renderer
    
    @renderer.setter
    def renderer(self, renderer:Renderer):
        if self._renderer is renderer:
            return
        
        if renderer is None:
            self._renderer._camera_id = id(None)
            self._renderer = None
            return

        if renderer._camera_id != id(None):
            renderer.camera.screen.renderer = None

        self._renderer = renderer
        renderer._camera_id = self._camera_id
        should_update = renderer.startup()
        if should_update:
            self.update()

    @property
    def manipulator(self):
        return self._manipulator
    
    @manipulator.setter
    def manipulator(self, manipulator:Manipulator):
        if self._manipulator is manipulator:
            return
        
        if manipulator is None:
            self._manipulator._camera_id = id(None)
            self._manipulator = None
            return

        if manipulator._camera_id != id(None):
            manipulator.camera.screen.manipulator = None

        self._manipulator = manipulator
        manipulator._camera_id = self._camera_id
        should_update = manipulator.startup()
        if should_update:
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

        self._is_gl_init = True

    def makeCurrent(self):
        QOpenGLWidget.makeCurrent(self)

        GLConfig.buffered_current_context = GLConfig.current_context
        SSBO.makeCurrent()
        UBO.makeCurrent()

    def resizeGL(self, width, height):
        QOpenGLWidget.resizeGL(self, width, height)
        self._before_filter_image = None

    def _draw_to_before_filter_image(self, should_update_scene):
        if self._before_filter_image is None or should_update_scene:
            with self._before_filter_fbo:
                clear_color = self.camera.scene.fog.apply(self.background_color, glm.vec3(0,0,0), glm.vec3(0,self.camera.far,0))
                with GLConfig.LocalConfig(clear_color=clear_color):
                    with self.renderer.render_hint:
                        should_update_scene = self.renderer.render() or should_update_scene

            self._before_filter_image = self._before_filter_fbo.resolved.color_attachment(0)
            self.renderer.filters.screen_update_time = time.time()

        return should_update_scene

    def paintGL(self):
        self.makeCurrent()
        self.frame_started.emit()

        should_update_scene = self.camera.scene.generate_meshes()
        should_update_filter = False
        
        if self._video_writers:
            should_update_scene = self._draw_to_before_filter_image(should_update_scene)
            screen_image = self.renderer.filters(self._before_filter_image)
            should_update_filter = self.renderer.filters.should_update
            Frame.draw(screen_image)
            for video_writer in self._video_writers:
                video_writer._frame_queue.put((time.time(), screen_image.fbo.data(0)))
        elif self.renderer.filters.has_valid:
            should_update_scene = self._draw_to_before_filter_image(should_update_scene)
            should_update_filter = self.renderer.filters.draw(self._before_filter_image)
        else:
            clear_color = self.camera.scene.fog.apply(self.background_color, glm.vec3(0,0,0), glm.vec3(0,self.camera.far,0))
            with GLConfig.LocalConfig(clear_color=clear_color):
                with self.renderer.render_hint:
                    should_update_scene = self.renderer.render() or should_update_scene

        self.__calc_fps()
        self.frame_ended.emit()

        if should_update_scene or should_update_filter:
            if should_update_scene:
                self._before_filter_image = None
                
            self._update()

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
            self.update()

    def mouseReleaseEvent(self, mouse_event: QMouseEvent)->None:
        button, screen_pos, global_pos = Screen.__mouse_parameters(mouse_event)

        self.makeCurrent()

        should_update = False
        if self.manipulator is not None:
            should_update = self.manipulator.on_mouse_released(button, screen_pos, global_pos)
        
        self.mouse_released.emit(button, screen_pos, global_pos)
        
        if should_update:
            self.update()

    def mouseDoubleClickEvent(self, mouse_event:QMouseEvent)->None:
        button, screen_pos, global_pos = Screen.__mouse_parameters(mouse_event)

        self.makeCurrent()

        should_update = False
        if self.manipulator is not None:
            should_update = self.manipulator.on_mouse_double_clicked(button, screen_pos, global_pos)
        
        self.mouse_double_clicked.emit(button, screen_pos, global_pos)
        
        if should_update:
            self.update()

    def __mouseMoveEvent(self, screen_pos:glm.vec2, global_pos:glm.vec2)->bool:
        self.makeCurrent()

        should_update = False
        if self.manipulator is not None:
            should_update = self.manipulator.on_mouse_moved(screen_pos, global_pos)

        self.mouse_moved.emit(screen_pos, global_pos)

        if should_update:
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
            self.update()

    def __keyRepeateEvent(self, keys:set[Manipulator.Key])->bool:
        self.makeCurrent()

        should_update = False
        if self.manipulator is not None:
            should_update = self.manipulator.on_key_repeated(keys)

        self.key_repeated.emit(keys)

        if should_update:
            self.update()

    def wheelEvent(self, wheel_event:QWheelEvent)->None:
        angle, screen_pos, global_pos = Screen.__wheel_parameters(wheel_event)

        self.makeCurrent()

        should_update = False
        if self.manipulator is not None:
            should_update = self.manipulator.on_wheel_scrolled(angle, screen_pos, global_pos)
        
        self.wheel_scrolled.emit(angle, screen_pos, global_pos)

        if should_update:
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
                self.update()

    @checktype
    def capture(self, save_path:str=None, viewport:tuple=None)->np.ndarray:
        self.makeCurrent()
        with self._before_filter_fbo:
            clear_color = self.camera.scene.fog.apply(self.background_color, glm.vec3(0,0,0), glm.vec3(0,self.camera.far,0))
            with GLConfig.LocalConfig(clear_color=clear_color):
                with self.renderer.render_hint:
                    self.renderer.render()

        image = None
        if self.renderer.filters.has_valid:
            self._before_filter_image = self._before_filter_fbo.resolved.color_attachment(0)
            self.renderer.filters.screen_update_time = time.time()
            result_sampler = self.renderer.filters(self._before_filter_image)
            image = result_sampler.fbo.data(0)
        else:
            image = self._before_filter_fbo.resolved.data(0)

        if viewport is None:
            viewport = GLConfig.viewport
        image = convert_to_image(image, viewport)
        
        if save_path is not None:
            folder_name = os.path.dirname(os.path.abspath(save_path))
            if not os.path.isdir(folder_name):
                os.makedirs(folder_name)

            cv2.imwrite(save_path, image)

        return image

    def capture_video(self, save_path:str, viewport:tuple=None, fps:float=None)->VideoWriter:
        ext_name = extname(save_path)
        if ext_name not in ["mp4", "avi"]:
            raise ValueError(f"not supported video type: .{ext_name}, only support .mp4 and .avi")
        
        fourcc = None
        if ext_name == "mp4":
            fourcc = cv2.VideoWriter_fourcc(*"MP4V")
        elif ext_name == "avi":
            fourcc = cv2.VideoWriter_fourcc(*"XVID")

        folder_path = os.path.dirname(os.path.abspath(save_path))
        if not os.path.isdir(folder_path):
            os.makedirs(folder_path)

        if fps is None:
            fps = self.smooth_fps

        if viewport is None:
            QOpenGLWidget.makeCurrent(self)
            viewport = GLConfig.viewport

        video_writer = VideoWriter(self._video_writers, save_path, fourcc, viewport, fps)
        self._video_writers.append(video_writer)

        return video_writer

    def closeEvent(self, close_event)->None:
        while self._video_writers:
            video_writer = self._video_writers.pop()
            video_writer.stop()
