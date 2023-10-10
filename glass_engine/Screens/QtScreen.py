from ..Manipulators.Manipulator import Manipulator
from ..Renderers.Renderer import Renderer
from ..PostProcessEffects import PostProcessEffects, BloomEffect, ACESToneMapper, FXAAEffect, DOFEffect, SSAOEffect, ExplosureAdaptor
from ..SlideAverageFilter import SlideAverageFilter
from ..VideoRecorder import VideoRecorder, convert_to_image

from glass import ShaderProgram, GLConfig, GlassConfig, FBO, RBO, sampler2DMS, sampler2D, RenderHints, SSBO, UBO, VAO
from glass.utils import extname, di

import time
import glm
import sys
from OpenGL import GL
import numpy as np
import os
import cv2
import warnings

def __new__(cls, *args, **kwargs):
    if cls.qt.QtWidgets.QApplication.instance() is None:
        cls._app = cls.qt.QtWidgets.QApplication(sys.argv)

    instance = cls.__base__.__new__(cls, *args, **kwargs)
    return instance

def __init__(self, camera, parent=None)->None:
    cls = self.__class__
    cls.__base__.__init__(self, parent=parent)

    self.setFocusPolicy(cls.qt.QtCore.Qt.FocusPolicy.StrongFocus)
    self._samples = 1
    self._samples_set_by_user = False

    self._pressed_keys = set()
    self._last_frame_time = 0
    self._is_cursor_hiden = False
    self._hide_cursor_global_pos = glm.vec2(0)
    self._last_cursor_global_pos = cls.qt.QtCore.QPoint(0, 0)
    self._fps = 0
    self._smooth_fps = 0
    self._before_draw_calls = 0
    self._before_draw_points = 0
    self._before_draw_lines = 0
    self._before_draw_meshes = 0
    self._before_draw_patches = 0
    self._draw_calls = 0
    self._draw_points = 0
    self._draw_lines = 0
    self._draw_meshes = 0
    self._draw_patches = 0
    self._paint_times = 0

    self._fps_filter = SlideAverageFilter()
    self._before_PPE_fbo_ss = None
    self._before_PPE_fbo_ms = None
    self._is_gl_init = False
    self._before_PPE_image = None
    self._video_recorders = []
    
    self._camera_id = id(camera)

    self._manipulator = None
    self._renderer = None
    
    self._render_hints = RenderHints()
    self._render_hints.depth_test = True

    self._listen_cursor_timer = self.startTimer(10)

    self._post_process_effects = PostProcessEffects()

    self._post_process_effects["SSAO"] = SSAOEffect()
    self._post_process_effects["bloom"] = BloomEffect()
    self._post_process_effects["DOF"] = DOFEffect()
    self._post_process_effects["explosure_adaptor"] = ExplosureAdaptor()
    self._post_process_effects["tone_mapper"] = ACESToneMapper()
    self._post_process_effects["FXAA"] = FXAAEffect(internal_format=GL.GL_RGBA8)

    self._post_process_effects["SSAO"].enabled = False
    self._post_process_effects["bloom"].enabled = False
    self._post_process_effects["DOF"].enabled = False
    self._post_process_effects["explosure_adaptor"].enabled = False
    self._post_process_effects["tone_mapper"].enabled = False
    self._post_process_effects["FXAA"].enabled = False

def update(self)->None:
    self._before_PPE_image = None
    self.__class__.__base__.update(self)

def _assign_values_to_PPEs(self):
    self._post_process_effects.camera = self.camera
    self._post_process_effects.depth_map = self.renderer._depth_map
    self._post_process_effects.view_normal_map = self.renderer._view_normal_map
    self._post_process_effects.view_pos_map = self._renderer._view_pos_map

def _update(self)->None:
    self.__class__.__base__.update(self)

def sizeHint(self):
    return self.__class__.qt.QtCore.QSize(800, 600)

@property
def camera(self):
    return di(self._camera_id)

@property
def samples(self)->int:
    return self._samples

@samples.setter
def samples(self, samples:int)->None:
    surface_format = self.__class__.qt.QtGui.QSurfaceFormat()
    surface_format.setSamples(samples)
    self.setFormat(surface_format)
    if not self._is_gl_init:
        self._samples = samples
        self._samples_set_by_user = True

def _set_samples(self, samples:int)->None:
    surface_format = self.__class__.qt.QtGui.QSurfaceFormat()
    surface_format.setSamples(samples)
    self.setFormat(surface_format)
    if not self._is_gl_init:
        self._samples = samples

@property
def renderer(self)->Renderer:
    return self._renderer

@renderer.setter
def renderer(self, renderer:Renderer)->None:
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
def manipulator(self)->Manipulator:
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
def render_hints(self)->RenderHints:
    return self._render_hints

@render_hints.setter
def render_hints(self, hint:RenderHints)->None:
    if hint is None:
        hint = RenderHints()

    self._render_hints = hint

def initializeGL(self)->None:
    if GLConfig.major_version < 4:
        raise RuntimeError(f"Current OpenGL version ({GLConfig.version}) is lower than minimum version require (OpenGL 4.3)")

    if GLConfig.minor_version < 3:
        raise RuntimeError(f"Current OpenGL version ({GLConfig.version}) is lower than minimum version require (OpenGL 4.3)")

    if GlassConfig.warning and "GL_ARB_bindless_texture" not in GLConfig.available_extensions:
        warning_message = """
Extension GL_ARB_bindless_texture is not available.
Shadows and dynamic environment mapping will be disabled.
Try to change default graphics card of python.exe to high performance one.
"""
        warnings.warn(warning_message)

    self.makeCurrent()

    if self.camera.scene is None:
        raise RuntimeError(f"{self.camera} is not in any scene, please add it to one scene before show it's screen")

    self._is_gl_init = True

def makeCurrent(self)->None:
    self.__class__.__base__.makeCurrent(self)
    GLConfig.buffered_current_context = GLConfig.current_context
    GLConfig.buffered_viewport = GLConfig.viewport

    SSBO.makeCurrent()
    UBO.makeCurrent()
    VAO.execute_cmd_buffer()

def resizeGL(self, width:int, height:int)->None:
    self.__class__.__base__.resizeGL(self, width, height)
    self._before_PPE_image = None

def _draw_to_before_PPE(self, should_update_scene:bool)->bool:
    if self._before_PPE_image is None or should_update_scene:
        with self._before_PPE_fbo:
            scene = self.camera.scene
            clear_color = scene.fog.apply(scene.background.color, glm.vec3(0), glm.vec3(0,self.camera.far,0))
            with GLConfig.LocalConfig(clear_color=clear_color):
                with self.render_hints:
                    should_update_scene = self.renderer.render() or should_update_scene

        resolved = self._before_PPE_fbo.resolved
        self._before_PPE_image = resolved.color_attachment(0)
        self._post_process_effects.screen_update_time = time.time()

    return should_update_scene

def _mark_draw_calls(self):
    self._before_draw_calls = ShaderProgram.accum_draw_calls()
    self._before_draw_points = ShaderProgram.accum_draw_points()
    self._before_draw_lines = ShaderProgram.accum_draw_lines()
    self._before_draw_meshes = ShaderProgram.accum_draw_meshes()
    self._before_draw_patches = ShaderProgram.accum_draw_patches()

def paintGL(self)->None:
    self.makeCurrent()
    self.frame_started.emit()
    self._mark_draw_calls()

    camera = self.camera
    scene = camera.scene

    should_update_scene = scene.generate_meshes()
    should_update_PPEs = False
    
    if self._video_recorders:
        should_update_scene = self._draw_to_before_PPE(should_update_scene)
        self._assign_values_to_PPEs()
        screen_image = self._post_process_effects.apply(self._before_PPE_image)
        should_update_PPEs = self._post_process_effects.should_update
        screen_image.fbo.draw_to_active(0)

        if self._paint_times > 0:
            view_port = GLConfig.buffered_viewport
            for video_recorder in self._video_recorders:
                video_recorder._start(view_port, self.smooth_fps)
                video_recorder._frame_queue.put((time.time(), screen_image.fbo.data(0)))
    elif self._post_process_effects.has_valid:
        should_update_scene = self._draw_to_before_PPE(should_update_scene)
        self._assign_values_to_PPEs()
        should_update_PPEs = self._post_process_effects.draw_to_active(self._before_PPE_image)
    else:
        clear_color = scene.fog.apply(scene.background.color, glm.vec3(0), glm.vec3(0,self.camera.far,0))
        with GLConfig.LocalConfig(clear_color=clear_color):
            with self.render_hints:
                should_update_scene = self.renderer.render() or should_update_scene

    self._calc_fps()
    self.frame_ended.emit()

    if should_update_scene or should_update_PPEs:
        if should_update_scene:
            self._before_PPE_image = None
            
        self._update()

@property
def _before_PPE_fbo(self)->FBO:
    screen_size = GLConfig.screen_size
    if self.samples > 1:
        if self._before_PPE_fbo_ms is not None:
            self._before_PPE_fbo_ms.resize(screen_size.x, screen_size.y, self.samples)
        else:
            self._before_PPE_fbo_ms = FBO(screen_size.x, screen_size.y, self.samples)
            self._before_PPE_fbo_ms.attach(0, sampler2DMS, GL.GL_RGBA32F)
            self._before_PPE_fbo_ms.attach(GL.GL_DEPTH_ATTACHMENT, RBO)
        return self._before_PPE_fbo_ms
    else:
        if self._before_PPE_fbo_ss is not None:
            self._before_PPE_fbo_ss.resize(screen_size.x, screen_size.y)
        else:
            self._before_PPE_fbo_ss = FBO(screen_size.x, screen_size.y)
            self._before_PPE_fbo_ss.attach(0, sampler2D, GL.GL_RGBA32F)
            self._before_PPE_fbo_ss.attach(GL.GL_DEPTH_ATTACHMENT, RBO)
        return self._before_PPE_fbo_ss
    
def _mouse_parameters(self, mouse_event)->tuple:
    button = mouse_event.button()
    try:
        button_value = button.value
    except:
        button_value = int(button)

    button = Manipulator.MouseButton(button_value)
    try:
        screen_pos = mouse_event.position()
        global_pos = mouse_event.globalPosition()
    except:
        screen_pos = mouse_event.pos()
        global_pos = self.mapToGlobal(screen_pos)

    screen_pos = glm.vec2(screen_pos.x(), screen_pos.y())
    global_pos = glm.vec2(global_pos.x(), global_pos.y())
    return button, screen_pos, global_pos

def _wheel_parameters(self, wheel_event)->tuple:
    angle = glm.vec2(wheel_event.angleDelta().x(), wheel_event.angleDelta().y())
    
    try:
        screen_pos = wheel_event.position()
        global_pos = wheel_event.globalPosition()
    except:
        screen_pos = wheel_event.pos()
        global_pos = self.mapToGlobal(screen_pos)

    screen_pos = glm.vec2(screen_pos.x(), screen_pos.y())
    global_pos = glm.vec2(global_pos.x(), global_pos.y())
    return angle, screen_pos, global_pos

def mousePressEvent(self, mouse_event)->None:
    button, screen_pos, global_pos = self._mouse_parameters(mouse_event)

    self.makeCurrent()

    should_update = False
    if self.manipulator is not None:
        should_update = self.manipulator.on_mouse_pressed(button, screen_pos, global_pos)

    self.mouse_pressed.emit(button, screen_pos, global_pos)

    if should_update:
        self.update()

def mouseReleaseEvent(self, mouse_event)->None:
    button, screen_pos, global_pos = self._mouse_parameters(mouse_event)

    self.makeCurrent()

    should_update = False
    if self.manipulator is not None:
        should_update = self.manipulator.on_mouse_released(button, screen_pos, global_pos)
    
    self.mouse_released.emit(button, screen_pos, global_pos)
    
    if should_update:
        self.update()

def mouseDoubleClickEvent(self, mouse_event)->None:
    button, screen_pos, global_pos = self._mouse_parameters(mouse_event)

    self.makeCurrent()

    should_update = False
    if self.manipulator is not None:
        should_update = self.manipulator.on_mouse_double_clicked(button, screen_pos, global_pos)
    
    self.mouse_double_clicked.emit(button, screen_pos, global_pos)
    
    if should_update:
        self.update()

def _mouseMoveEvent(self, screen_pos:glm.vec2, global_pos:glm.vec2)->bool:
    self.makeCurrent()

    should_update = False
    if self.manipulator is not None:
        should_update = self.manipulator.on_mouse_moved(screen_pos, global_pos)

    self.mouse_moved.emit(screen_pos, global_pos)

    if should_update:
        self.update()

def keyPressEvent(self, key_event)->None:
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

def keyReleaseEvent(self, key_event)->None:
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

def _keyRepeateEvent(self, keys:set)->bool:
    self.makeCurrent()

    should_update = False
    if self.manipulator is not None:
        should_update = self.manipulator.on_key_repeated(keys)

    self.key_repeated.emit(keys)

    if should_update:
        self.update()

def wheelEvent(self, wheel_event)->None:
    angle, screen_pos, global_pos = self._wheel_parameters(wheel_event)

    self.makeCurrent()

    should_update = False
    if self.manipulator is not None:
        should_update = self.manipulator.on_wheel_scrolled(angle, screen_pos, global_pos)
    
    self.wheel_scrolled.emit(angle, screen_pos, global_pos)

    if should_update:
        self.update()

def _calc_fps(self)->None:
    current_time = time.time()
    dt = current_time - self._last_frame_time
    self._last_frame_time = current_time
    if dt < 1:
        self._fps = 1 / dt
        self._smooth_fps = self._fps_filter(self._fps)

    self._draw_calls = ShaderProgram.accum_draw_calls() - self._before_draw_calls
    self._draw_points = ShaderProgram.accum_draw_points() - self._before_draw_points
    self._draw_lines = ShaderProgram.accum_draw_lines() - self._before_draw_lines
    self._draw_meshes = ShaderProgram.accum_draw_meshes() - self._before_draw_meshes
    self._draw_patches = ShaderProgram.accum_draw_patches() - self._before_draw_patches
    self._paint_times += 1

def hide_cursor(self)->None:
    if self._is_cursor_hiden:
        return
    
    self._is_cursor_hiden = True
    cursor_pos = self.__class__.qt.QtGui.QCursor.pos()
    self._hide_cursor_global_pos = glm.vec2(cursor_pos.x(), cursor_pos.y())
    self.setCursor(self.__class__.qt.QtCore.Qt.CursorShape.BlankCursor)
    return self._hide_cursor_global_pos

def show_cursor(self)->None:
    if not self._is_cursor_hiden:
        return
    
    self._is_cursor_hiden = False
    self.unsetCursor()

def show(self)->None:
    if self.__class__._app is not None and \
        not self.__class__._has_exec:
        self.setWindowTitle("Glass Engine")
        self_folder = os.path.dirname(os.path.abspath(__file__))
        self.setWindowIcon(self.__class__.qt.QtGui.QIcon(self_folder + "/../images/glass_engine_logo64.png"))
        
    self.__class__.__base__.show(self)
    if self.__class__._app is not None and \
        not self.__class__._has_exec:
        self.__class__._app.exec()
        self.__class__._has_exec = True

@property
def post_process_effects(self)->PostProcessEffects:
    return self._post_process_effects

@property
def is_cursor_hiden(self)->bool:
    return self._is_cursor_hiden

@property
def fps(self)->float:
    return self._fps

@property
def smooth_fps(self)->float:
    return self._smooth_fps

@property
def draw_calls(self)->int:
    return self._draw_calls

@property
def draw_points(self)->int:
    return self._draw_points

@property
def draw_lines(self)->int:
    return self._draw_lines

@property
def draw_meshes(self)->int:
    return self._draw_meshes

@property
def draw_patches(self)->int:
    return self._draw_patches

def timerEvent(self, timer_event)->None:
    if timer_event.timerId() == self._listen_cursor_timer:
        cursor_global_pos = self.__class__.qt.QtGui.QCursor.pos()
        last_global_pos = self._last_cursor_global_pos
        self._last_cursor_global_pos = cursor_global_pos

        cursor_global_posF = self.__class__.qt.QtCore.QPointF(cursor_global_pos)

        should_update = False
        if self._pressed_keys:
            should_update = self._keyRepeateEvent(self._pressed_keys) or should_update

        if self._is_cursor_hiden:
            try:
                center_global_posF = self.mapToGlobal(self.__class__.qt.QtCore.QPointF(self.width()/2, self.height()))
            except:
                center = self.__class__.qt.QtCore.QPoint(int(self.width()/2), int(self.height()/2))
                center_global_pos = self.mapToGlobal(center)
                center_global_posF = self.__class__.qt.QtCore.QPointF(float(center_global_pos.x()), float(center_global_pos.y()))
            
            offset = cursor_global_posF - center_global_posF
            buffer = 100
            if offset.x() > buffer or offset.x() < -buffer or \
                offset.y() > buffer or offset.y() < -buffer:
                self._hide_cursor_global_pos.x -= offset.x()
                self._hide_cursor_global_pos.y -= offset.y()
                self.__class__.qt.QtGui.QCursor.setPos(center_global_posF.toPoint())
                cursor_global_posF = center_global_posF
        
        if cursor_global_pos != last_global_pos:
            try:
                screen_pos = self.mapFromGlobal(cursor_global_posF)
            except:
                screen_pos = self.mapFromGlobal(self.__class__.qt.QtCore.QPoint(int(cursor_global_posF.x()), int(cursor_global_posF.y())))
            
            screen_pos = glm.vec2(screen_pos.x(), screen_pos.y())
            global_pos = glm.vec2(cursor_global_posF.x(), cursor_global_posF.y())
            should_update = self._mouseMoveEvent(screen_pos, global_pos) or should_update

        if should_update:
            self.update()

def capture(self, save_path:str=None, viewport:tuple=None)->np.ndarray:
    self.makeCurrent()
    with self._before_PPE_fbo:
        scene = self.camera.scene
        clear_color = scene.fog.apply(scene.background.color, glm.vec3(0), glm.vec3(0,self.camera.far,0))
        with GLConfig.LocalConfig(clear_color=clear_color):
            with self.render_hints:
                self.renderer.render()

    image = None
    resolved = self._before_PPE_fbo.resolved
    if self._post_process_effects.has_valid:
        self._before_PPE_image = resolved.color_attachment(0)
        self._post_process_effects.screen_update_time = time.time()
        self._assign_values_to_PPEs()
        result_sampler = self._post_process_effects.apply(self._before_PPE_image)
        image = result_sampler.fbo.data(0)
    else:
        image = resolved.data(0)

    if viewport is None:
        viewport = GLConfig.buffered_viewport
    image = convert_to_image(image, viewport)
    
    if save_path is not None:
        folder_name = os.path.dirname(os.path.abspath(save_path))
        if not os.path.isdir(folder_name):
            os.makedirs(folder_name)

        cv2.imwrite(save_path, image)

    return image

def capture_video(self, save_path:str, viewport:tuple=None, fps:(float,int)=None)->VideoRecorder:
    ext_name = extname(save_path)
    if ext_name not in ["mp4", "avi"]:
        raise ValueError(f"not supported video type: .{ext_name}, only support .mp4 and .avi")
    
    fourcc = None
    if ext_name == "mp4":
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    elif ext_name == "avi":
        fourcc = cv2.VideoWriter_fourcc(*"XVID")

    folder_path = os.path.dirname(os.path.abspath(save_path))
    if not os.path.isdir(folder_path):
        os.makedirs(folder_path)

    if fps is None:
        fps = self.smooth_fps

    if viewport is None:
        self.__class__.__base__.makeCurrent(self)
        try:
            viewport = GLConfig.buffered_viewport
        except:
            viewport = None

    video_recorder = VideoRecorder(self._video_recorders, save_path, fourcc, viewport, fps)
    self._video_recorders.append(video_recorder)

    return video_recorder

def closeEvent(self, close_event)->None:
    while self._video_recorders:
        video_recorder = self._video_recorders.pop()
        video_recorder.stop()

@property
def bloom(self):
    return self._post_process_effects["bloom"]

@bloom.setter
def bloom(self, flag:bool):
    self._post_process_effects["bloom"].enabled = flag

@property
def SSAO(self):
    return self._post_process_effects["SSAO"]

@SSAO.setter
def SSAO(self, flag:bool):
    self._post_process_effects["SSAO"].enabled = flag

@property
def tone_mapper(self):
    return self._post_process_effects["tone_mapper"]

@tone_mapper.setter
def tone_mapper(self, flag:bool):
    self._post_process_effects["tone_mapper"].enabled = flag

@property
def DOF(self):
    return self._post_process_effects["DOF"]

@DOF.setter
def DOF(self, flag:bool):
    self._post_process_effects["DOF"].enabled = flag

@property
def explosure_adaptor(self):
    return self._post_process_effects["explosure_adaptor"]

@explosure_adaptor.setter
def explosure_adaptor(self, flag:bool):
    self._post_process_effects["explosure_adaptor"].enabled = flag

@property
def FXAA(self):
    return self._post_process_effects["FXAA"]

@FXAA.setter
def FXAA(self, flag:bool):
    self._post_process_effects["FXAA"].enabled = flag

def init_QtScreen(cls):
    cls.qt = sys.modules[cls.__base__.__module__.split(".")[0]]
    cls._app = None
    cls._has_exec = False

    cls.__new__ = __new__
    cls.__init__ = __init__
    cls.update = update
    cls._assign_values_to_PPEs = _assign_values_to_PPEs
    cls._update = _update
    cls.sizeHint = sizeHint
    cls.camera = camera
    cls.samples = samples
    cls._set_samples = _set_samples
    cls.renderer = renderer
    cls.manipulator = manipulator
    cls.render_hints = render_hints
    cls.initializeGL = initializeGL
    cls.makeCurrent = makeCurrent
    cls.resizeGL = resizeGL
    cls._draw_to_before_PPE = _draw_to_before_PPE
    cls._mark_draw_calls = _mark_draw_calls
    cls.paintGL = paintGL
    cls._before_PPE_fbo = _before_PPE_fbo
    cls._mouse_parameters = _mouse_parameters
    cls._wheel_parameters = _wheel_parameters
    cls.mousePressEvent = mousePressEvent
    cls.mouseReleaseEvent = mouseReleaseEvent
    cls.mouseDoubleClickEvent = mouseDoubleClickEvent
    cls._mouseMoveEvent = _mouseMoveEvent
    cls.keyPressEvent = keyPressEvent
    cls.keyReleaseEvent = keyReleaseEvent
    cls._keyRepeateEvent = _keyRepeateEvent
    cls.wheelEvent = wheelEvent
    cls._calc_fps = _calc_fps
    cls.hide_cursor = hide_cursor
    cls.show_cursor = show_cursor
    cls.show = show
    cls.post_process_effects = post_process_effects
    cls.is_cursor_hiden = is_cursor_hiden
    cls.fps = fps
    cls.smooth_fps = smooth_fps
    cls.draw_calls = draw_calls
    cls.draw_points = draw_points
    cls.draw_lines = draw_lines
    cls.draw_meshes = draw_meshes
    cls.draw_patches = draw_patches
    cls.timerEvent = timerEvent
    cls.capture = capture
    cls.capture_video = capture_video
    cls.closeEvent = closeEvent
    cls.bloom = bloom
    cls.SSAO = SSAO
    cls.tone_mapper = tone_mapper
    cls.DOF = DOF
    cls.explosure_adaptor = explosure_adaptor
    cls.FXAA = FXAA

    return cls