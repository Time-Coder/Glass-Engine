import OpenGL
from OpenGL import GL
from OpenGL.platform import PLATFORM
import glm
import numpy as np
import inspect
from typing import Union, Tuple
import functools

from .GLInfo import GLInfo
from .helper import glGetEnum, glGetEnumi


def record_old_value(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if _MetaGLConfig._active_local_env is not None:
            cls = args[0]
            new_value = args[1]
            old_value = getattr(cls, func.__name__)

            if old_value == new_value:
                return

            _MetaGLConfig._active_local_env.add_old_value(
                func.__name__, old_value
            )

        return func(*args, **kwargs)

    return wrapper


class StencilFunc:

    def __init__(
        self,
        func: Union[GLInfo.stencil_funcs, GLInfo.stencil_func_strs] = None,
        ref: int = None,
        mask: int = None,
    ):
        if func is None:
            func = glGetEnum(GL.GL_STENCIL_FUNC)

        if ref is None:
            ref = glGetEnum(GL.GL_STENCIL_REF)

        if mask is None:
            mask = glGetEnum(GL.GL_STENCIL_VALUE_MASK)

        if isinstance(func, str):
            func = GLInfo.stencil_func_map[func]

        self.__func = func
        self.__ref = ref
        self.__mask = mask

    def apply(self):
        if _MetaGLConfig._active_local_env is not None:
            _MetaGLConfig._active_local_env.add_recover_func(
                GL.glStencilFunc,
                glGetEnum(GL.GL_STENCIL_FUNC),
                glGetEnum(GL.GL_STENCIL_REF),
                glGetEnum(GL.GL_STENCIL_VALUE_MASK)
            )

        GL.glStencilFunc(self.__func, self.__ref, self.__mask)

    def update(self):
        self.__ref = glGetEnum(GL.GL_STENCIL_REF)
        self.__mask = glGetEnum(GL.GL_STENCIL_VALUE_MASK)
        self.__func = glGetEnum(GL.GL_STENCIL_FUNC)

    @property
    def func(self):
        return self.__func

    @property
    def ref(self):
        return self.__ref

    @property
    def mask(self):
        return self.__mask

    def __and__(self, mask: int):
        self.__mask = mask

    def __lt__(self, ref):
        GL.glStencilFunc(GL.GL_LESS, (~ref) | self.__mask, self.__mask)
        self.__func = "<"
        self.__ref = ref

    def __le__(self, ref):
        GL.glStencilFunc(GL.GL_LEQUAL, (~ref) | self.__mask, self.__mask)
        self.__func = "<="
        self.__ref = ref

    def __eq__(self, ref):
        if ref.__class__ == int:
            GL.glStencilFunc(GL.GL_EQUAL, (~ref) | self.__mask, self.__mask)
            self.__func = "=="
            self.__ref = ref
        elif isinstance(ref, self.__class__):
            return (
                self.__func == ref.__func
                and self.__ref == ref.__ref
                and self.__mask == ref.__mask
            )
        elif isinstance(ref, tuple):
            return (
                self.__func == ref[0] and self.__ref == ref[1] and self.__mask == ref[2]
            )
        else:
            return False

    def __gt__(self, ref):
        GL.glStencilFunc(GL.GL_GREATER, (~ref) | self.__mask, self.__mask)
        self.__func = ">"
        self.__ref = ref

    def __ge__(self, ref):
        GL.glStencilFunc(GL.GL_GEQUAL, (~ref) | self.__mask, self.__mask)
        self.__func = ">="
        self.__ref = ref

    def __ne__(self, ref):
        if ref.__class__ == int:
            GL.glStencilFunc(GL.GL_NOTEQUAL, (~ref) | self.__mask, self.__mask)
            self.__func = "!="
            self.__ref = ref
        elif isinstance(ref, self.__class__):
            return (
                self.__func != ref.__func
                or self.__ref != ref.__ref
                or self.__mask != ref.__mask
            )
        else:
            return True


class _MetaGLConfig(type):

    class BlendSrcRGBi:
        def __getitem__(self, index: int):
            return glGetEnumi(GL.GL_BLEND_SRC_RGB, index)

        def __setitem__(self, index: int, value: GLInfo.blend_funcs):
            dst = glGetEnumi(GL.GL_BLEND_DST_RGB, index)
            if _MetaGLConfig._active_local_env is not None:
                _MetaGLConfig._active_local_env.add_recover_func(
                    GL.glBlendFunci,
                    index, glGetEnumi(GL.GL_BLEND_SRC_RGB, index), dst
                )

            GL.glBlendFunci(index, value, dst)

    BlendSrcRGBi = BlendSrcRGBi()

    class BlendDstRGBi:
        def __getitem__(self, index: int):
            return glGetEnumi(GL.GL_BLEND_DST_RGB, index)

        def __setitem__(self, index: int, value: GLInfo.blend_funcs):
            src = glGetEnumi(GL.GL_BLEND_SRC_RGB, index)
            if _MetaGLConfig._active_local_env is not None:
                _MetaGLConfig._active_local_env.add_recover_func(
                    GL.glBlendFunci,
                    index, src, glGetEnumi(GL.GL_BLEND_DST_RGB, index)
                )

            GL.glBlendFunci(index, src, value)

    BlendDstRGBi = BlendDstRGBi()

    class BlendSrcAlphai:
        def __getitem__(self, index: int):
            return glGetEnumi(GL.GL_BLEND_SRC_ALPHA, index)

        def __setitem__(self, index: int, value: GLInfo.blend_funcs):
            dst = glGetEnumi(GL.GL_BLEND_DST_ALPHA, index)
            if _MetaGLConfig._active_local_env is not None:
                _MetaGLConfig._active_local_env.add_recover_func(
                    GL.glBlendFunci,
                    index, glGetEnumi(GL.GL_BLEND_SRC_ALPHA, index), dst
                )

            GL.glBlendFunci(index, value, dst)

    BlendSrcAlphai = BlendSrcAlphai()

    class BlendDstAlphai:
        def __getitem__(self, index: int):
            return glGetEnumi(GL.GL_BLEND_DST_ALPHA, index)

        def __setitem__(self, index: int, value: GLInfo.blend_funcs):
            src = glGetEnumi(GL.GL_BLEND_SRC_ALPHA, index)
            if _MetaGLConfig._active_local_env is not None:
                _MetaGLConfig._active_local_env.add_recover_func(
                    GL.glBlendFunci,
                    index, src, glGetEnumi(GL.GL_BLEND_DST_ALPHA, index)
                )

            GL.glBlendFunci(index, src, value)

    BlendDstAlphai = BlendDstAlphai()

    __debug = True

    __max_texture_units = None
    __max_image_units = None
    __max_compute_work_group_count = None
    __max_compute_work_group_size = None
    __max_compute_work_group_invocations = None
    __max_uniform_buffer_bindings = None
    __max_shader_storage_buffer_bindings = None
    __max_color_attachments = None
    __max_draw_buffers = None
    __screen_size = {}
    __buffered_current_context = None
    __buffered_viewport = {}
    __gl_version = None
    __gl_major_version = None
    __gl_minor_version = None
    __gl_renderer = None
    __available_texture_units = None
    __available_image_units = None
    __available_extensions = None
    __depth_bits = None
    _active_local_env = None
    _all_setters = None

    @property
    def debug(cls):
        return _MetaGLConfig.__debug

    @debug.setter
    @record_old_value
    def debug(cls, flag: bool):
        _MetaGLConfig.__debug = flag
        OpenGL.ERROR_CHECKING = flag

    @property
    def stencil_test(cls):
        return bool(GL.glIsEnabled(GL.GL_STENCIL_TEST))

    @stencil_test.setter
    @record_old_value
    def stencil_test(cls, flag: bool):
        if flag:
            GL.glEnable(GL.GL_STENCIL_TEST)
        else:
            GL.glDisable(GL.GL_STENCIL_TEST)

    @property
    def stencil_mask(cls):
        return glGetEnum(GL.GL_STENCIL_VALUE_MASK)

    @stencil_mask.setter
    @record_old_value
    def stencil_mask(cls, mask: int):
        GL.glStencilMask(mask)

    @property
    def stencil_func(cls):
        return StencilFunc()

    @stencil_func.setter
    def stencil_func(cls, func):
        if isinstance(func, StencilFunc):
            func.apply()
            return
        
        if _MetaGLConfig._active_local_env is not None:
            _MetaGLConfig._active_local_env.add_old_value(
                "stencil_func", GLConfig.stencil_func
            )

        if func in [True, "always", GL.GL_ALWAYS]:
            GL.glStencilFunc(GL.GL_ALWAYS, 1, 0xFF)
        elif func in [False, None, "never", GL.GL_NEVER]:
            GL.glStencilFunc(GL.GL_NEVER, 1, 0xFF)
        else:
            f = func[0]
            if isinstance(f, str):
                f = GLInfo.stencil_func_map[f]
            GL.glStencilFunc(f, func[1], func[2])

    @property
    def stencil_fail(cls):
        return glGetEnum(GL.GL_STENCIL_FAIL)

    @stencil_fail.setter
    @record_old_value
    def stencil_fail(cls, operation: GLInfo.operations):
        GL.glStencilOp(
            operation, cls.stencil_pass_depth_fail, cls.stencil_pass_depth_pass
        )

    @property
    def stencil_pass_depth_fail(cls):
        return glGetEnum(GL.GL_STENCIL_PASS_DEPTH_FAIL)

    @stencil_pass_depth_fail.setter
    @record_old_value
    def stencil_pass_depth_fail(cls, operation: GLInfo.operations):
        GL.glStencilOp(cls.stencil_fail, operation, cls.stencil_pass_depth_pass)

    @property
    def stencil_pass_depth_pass(cls):
        return glGetEnum(GL.GL_STENCIL_PASS_DEPTH_PASS)

    @stencil_pass_depth_pass.setter
    @record_old_value
    def stencil_pass_depth_pass(cls, operation: GLInfo.operations):
        GL.glStencilOp(cls.stencil_fail, cls.stencil_pass_depth_fail, operation)

    @property
    def stencil_op(cls):
        return (
            cls.stencil_fail,
            cls.stencil_pass_depth_fail,
            cls.stencil_pass_depth_pass,
        )

    @stencil_op.setter
    @record_old_value
    def stencil_op(cls, stencil_op):
        GL.glStencilOp(*stencil_op)

    @property
    def depth_test(cls):
        return bool(GL.glIsEnabled(GL.GL_DEPTH_TEST))

    @depth_test.setter
    @record_old_value
    def depth_test(cls, flag: bool):
        if flag:
            GL.glEnable(GL.GL_DEPTH_TEST)
        else:
            GL.glDisable(GL.GL_DEPTH_TEST)

    @property
    def depth_mask(cls):
        result = GL.glGetBooleanv(GL.GL_DEPTH_WRITEMASK)
        return bool(result)

    @depth_mask.setter
    @record_old_value
    def depth_mask(cls, flag: bool):
        if flag:
            GL.glDepthMask(GL.GL_TRUE)
        else:
            GL.glDepthMask(GL.GL_FALSE)

    @property
    def depth_write(cls):
        result = GL.glGetBooleanv(GL.GL_DEPTH_WRITEMASK)
        return bool(result)

    @depth_write.setter
    @record_old_value
    def depth_write(cls, flag: bool):
        if flag:
            GL.glDepthMask(GL.GL_TRUE)
        else:
            GL.glDepthMask(GL.GL_FALSE)

    @property
    def depth_func(cls):
        depth_func = glGetEnum(GL.GL_DEPTH_FUNC)
        return GLInfo.depth_func_map[depth_func]

    @depth_func.setter
    @record_old_value
    def depth_func(cls, depth_func: Union[GLInfo.depth_funcs, GLInfo.depth_func_strs]):
        if isinstance(depth_func, str):
            depth_func = GLInfo.depth_func_map[depth_func]

        GL.glDepthFunc(depth_func)

    @property
    def blend(cls):
        return bool(GL.glIsEnabled(GL.GL_BLEND))

    @blend.setter
    @record_old_value
    def blend(cls, flag: bool):
        if flag:
            GL.glEnable(GL.GL_BLEND)
        else:
            GL.glDisable(GL.GL_BLEND)

    @property
    def blend_equation(cls):
        blend_equation = glGetEnum(GL.GL_BLEND_EQUATION)
        return GLInfo.blend_equation_map[blend_equation]

    @blend_equation.setter
    @record_old_value
    def blend_equation(cls, blend_equation: Union[GLInfo.blend_equations, GLInfo.blend_equation_strs]):
        if isinstance(blend_equation, str):
            blend_equation = GLInfo.blend_equation_map[blend_equation]

        GL.glBlendEquation(blend_equation)

    @property
    def blend_func(cls):
        return cls.blend_src_rgb, cls.blend_dest_rgb

    @blend_func.setter
    @record_old_value
    def blend_func(cls, args: tuple):
        GL.glBlendFunc(*args)

    @property
    def blend_src_rgbi(cls):
        return _MetaGLConfig.BlendSrcRGBi

    @property
    def blend_dest_rgbi(cls):
        return _MetaGLConfig.BlendDstRGBi

    @property
    def blend_src_alphai(cls):
        return _MetaGLConfig.BlendSrcAlphai

    @property
    def blend_dest_alphai(cls):
        return _MetaGLConfig.BlendDstAlphai

    @property
    def blend_src_rgb(cls):
        return glGetEnum(GL.GL_BLEND_SRC_RGB)

    @blend_src_rgb.setter
    @record_old_value
    def blend_src_rgb(cls, value: GLInfo.blend_funcs):
        GL.glBlendFunc(value, cls.blend_dest_rgb)

    @property
    def blend_dest_rgb(cls):
        return glGetEnum(GL.GL_BLEND_DST_RGB)

    @blend_dest_rgb.setter
    @record_old_value
    def blend_dest_rgb(cls, value: GLInfo.blend_funcs):
        GL.glBlendFunc(cls.blend_src_rgb, value)

    @property
    def blend_src_alpha(cls):
        return glGetEnum(GL.GL_BLEND_SRC_ALPHA)

    @blend_src_alpha.setter
    @record_old_value
    def blend_src_alpha(cls, value: GLInfo.blend_funcs):
        GL.glBlendFuncSeparate(
            cls.blend_src_rgb, cls.blend_dest_rgb, value, cls.blend_dest_alpha
        )

    @property
    def blend_dest_alpha(cls):
        return glGetEnum(GL.GL_BLEND_DST_ALPHA)

    @blend_dest_alpha.setter
    @record_old_value
    def blend_dest_alpha(cls, value: GLInfo.blend_funcs):
        GL.glBlendFuncSeparate(
            cls.blend_src_rgb, cls.blend_dest_rgb, cls.blend_src_alpha, value
        )

    @property
    def cull_face(cls):
        if not GL.glIsEnabled(GL.GL_CULL_FACE):
            return None

        return glGetEnum(GL.GL_CULL_FACE_MODE)

    @cull_face.setter
    @record_old_value
    def cull_face(cls, face: GLInfo.cull_face_types):
        if face is None:
            GL.glDisable(GL.GL_CULL_FACE)
        else:
            GL.glEnable(GL.GL_CULL_FACE)
            GL.glCullFace(face)

    @property
    def clear_color(cls):
        color_array = np.array([0.0] * 4, dtype=np.float32)
        GL.glGetFloatv(GL.GL_COLOR_CLEAR_VALUE, color_array)
        return glm.vec4(color_array[0], color_array[1], color_array[2], color_array[3])

    @clear_color.setter
    @record_old_value
    def clear_color(cls, color: Union[Tuple[float], glm.vec3, glm.vec4, float]):
        if isinstance(color, float):
            GL.glClearColor(color, color, color, color)
        elif len(color) == 3:
            GL.glClearColor(color[0], color[1], color[2], 1)
        elif len(color) == 4:
            GL.glClearColor(color[0], color[1], color[2], color[3])
        else:
            raise ValueError(color)

    @property
    def polygon_mode(cls):
        return glGetEnum(GL.GL_POLYGON_MODE)

    @polygon_mode.setter
    @record_old_value
    def polygon_mode(cls, mode: GLInfo.polygon_modes):
        GL.glPolygonMode(GL.GL_FRONT_AND_BACK, mode)

    @property
    def line_width(cls):
        return GL.glGetFloatv(GL.GL_LINE_WIDTH)

    @line_width.setter
    @record_old_value
    def line_width(cls, line_width: float):
        GL.glLineWidth(line_width)

    @property
    def point_size(cls):
        return GL.glGetFloatv(GL.GL_POINT_SIZE)

    @point_size.setter
    @record_old_value
    def point_size(cls, point_size: float):
        GL.glPointSize(point_size)

    @property
    def viewport(cls):
        current_viewport = GL.glGetIntegerv(GL.GL_VIEWPORT)
        return (
            int(current_viewport[0]),
            int(current_viewport[1]),
            int(current_viewport[2]),
            int(current_viewport[3]),
        )

    @viewport.setter
    @record_old_value
    def viewport(cls, viewport: tuple):
        GL.glViewport(*viewport)

    @property
    def buffered_viewport(cls):
        current_context = cls.buffered_current_context
        if current_context not in _MetaGLConfig.__buffered_viewport:
            return cls.viewport

        return _MetaGLConfig.__buffered_viewport[current_context]

    @buffered_viewport.setter
    @record_old_value
    def buffered_viewport(cls, viewport):
        current_context = cls.buffered_current_context
        _MetaGLConfig.__buffered_viewport[current_context] = viewport

    @property
    def screen_size(cls) -> glm.ivec2:
        current_context = cls.buffered_current_context
        if current_context not in _MetaGLConfig.__screen_size:
            _MetaGLConfig.__screen_size[current_context] = glm.ivec2()

        viewport = cls.viewport
        _MetaGLConfig.__screen_size[current_context].x = viewport[2]
        _MetaGLConfig.__screen_size[current_context].y = viewport[3]
        return _MetaGLConfig.__screen_size[current_context]

    @property
    def active_texture_unit(cls):
        return int(GL.glGetIntegerv(GL.GL_ACTIVE_TEXTURE) - GL.GL_TEXTURE0)

    @active_texture_unit.setter
    @record_old_value
    def active_texture_unit(cls, unit):
        if unit >= cls.max_texture_units:
            raise ValueError(
                f"try to active texture unit {unit}, which is over hardware available texture units range 0~{cls.max_texture_units-1}"
            )

        GL.glActiveTexture(GL.GL_TEXTURE0 + unit)

    # Read only:
    @property
    def depth_bits(self):
        if _MetaGLConfig.__depth_bits is None:
            _MetaGLConfig.__depth_bits = int(GL.glGetIntegerv(GL.GL_DEPTH_BITS))

        return _MetaGLConfig.__depth_bits

    @property
    def max_color_attachments(cls):
        if _MetaGLConfig.__max_color_attachments is None:
            try:
                _MetaGLConfig.__max_color_attachments = GL.glGetIntegerv(
                    GL.GL_MAX_COLOR_ATTACHMENTS
                )
            except:
                return 8

        return _MetaGLConfig.__max_color_attachments

    @property
    def max_draw_buffers(cls):
        if _MetaGLConfig.__max_draw_buffers is None:
            try:
                _MetaGLConfig.__max_draw_buffers = GL.glGetIntegerv(
                    GL.GL_MAX_DRAW_BUFFERS
                )
            except:
                return 8

        return _MetaGLConfig.__max_draw_buffers

    @property
    def max_texture_units(cls):
        if _MetaGLConfig.__max_texture_units is None:
            _MetaGLConfig.__max_texture_units = GL.glGetIntegerv(
                GL.GL_MAX_TEXTURE_IMAGE_UNITS
            )
        return _MetaGLConfig.__max_texture_units

    @property
    def max_image_units(cls):
        if _MetaGLConfig.__max_image_units is None:
            _MetaGLConfig.__max_image_units = GL.glGetIntegerv(GL.GL_MAX_IMAGE_UNITS)
        return _MetaGLConfig.__max_image_units

    @property
    def max_compute_work_group_count(cls):
        if _MetaGLConfig.__max_compute_work_group_count is None:
            max_x = GL.glGetIntegeri_v(GL.GL_MAX_COMPUTE_WORK_GROUP_COUNT, 0)[0]
            max_y = GL.glGetIntegeri_v(GL.GL_MAX_COMPUTE_WORK_GROUP_COUNT, 1)[0]
            max_z = GL.glGetIntegeri_v(GL.GL_MAX_COMPUTE_WORK_GROUP_COUNT, 2)[0]
            _MetaGLConfig.__max_compute_work_group_count = (max_x, max_y, max_z)

        return _MetaGLConfig.__max_compute_work_group_count

    @property
    def max_compute_work_group_size(cls):
        if _MetaGLConfig.__max_compute_work_group_size is None:
            max_x = GL.glGetIntegeri_v(GL.GL_MAX_COMPUTE_WORK_GROUP_SIZE, 0)[0]
            max_y = GL.glGetIntegeri_v(GL.GL_MAX_COMPUTE_WORK_GROUP_SIZE, 1)[0]
            max_z = GL.glGetIntegeri_v(GL.GL_MAX_COMPUTE_WORK_GROUP_SIZE, 2)[0]
            _MetaGLConfig.__max_compute_work_group_size = (max_x, max_y, max_z)
        return _MetaGLConfig.__max_compute_work_group_size

    @property
    def max_compute_work_group_invocations(cls):
        if _MetaGLConfig.__max_compute_work_group_invocations is None:
            _MetaGLConfig.__max_compute_work_group_invocations = GL.glGetIntegerv(
                GL.GL_MAX_COMPUTE_WORK_GROUP_INVOCATIONS
            )
        return _MetaGLConfig.__max_compute_work_group_invocations

    @property
    def max_uniform_buffer_bindings(cls):
        if _MetaGLConfig.__max_uniform_buffer_bindings is None:
            _MetaGLConfig.__max_uniform_buffer_bindings = int(
                GL.glGetIntegerv(GL.GL_MAX_UNIFORM_BUFFER_BINDINGS)
            )
        return _MetaGLConfig.__max_uniform_buffer_bindings

    @property
    def max_shader_storage_buffer_bindings(cls):
        if _MetaGLConfig.__max_shader_storage_buffer_bindings is None:
            _MetaGLConfig.__max_shader_storage_buffer_bindings = int(
                GL.glGetIntegerv(GL.GL_MAX_SHADER_STORAGE_BUFFER_BINDINGS)
            )
        return _MetaGLConfig.__max_shader_storage_buffer_bindings

    @property
    def current_context(cls):
        try:
            context = PLATFORM.GetCurrentContext()
            return context if isinstance(context, int) else context.address
        except:
            return 0

    @property
    def buffered_current_context(cls):
        if _MetaGLConfig.__buffered_current_context is None:
            return cls.current_context
        else:
            return _MetaGLConfig.__buffered_current_context

    @buffered_current_context.setter
    @record_old_value
    def buffered_current_context(cls, context_id: int):
        _MetaGLConfig.__buffered_current_context = context_id

    @property
    def version(cls) -> str:
        if _MetaGLConfig.__gl_version is None:
            _MetaGLConfig.__gl_version = GL.glGetString(GL.GL_VERSION).decode("utf-8")

        return _MetaGLConfig.__gl_version

    @property
    def major_version(cls) -> str:
        if _MetaGLConfig.__gl_major_version is None:
            try:
                _MetaGLConfig.__gl_major_version = GL.glGetInteger(GL.GL_MAJOR_VERSION)
            except:
                _MetaGLConfig.__gl_major_version = cls.version.split(" ")[0].split(".")[
                    0
                ]

        return _MetaGLConfig.__gl_major_version

    @property
    def minor_version(cls) -> str:
        if _MetaGLConfig.__gl_minor_version is None:
            try:
                _MetaGLConfig.__gl_minor_version = GL.glGetInteger(GL.GL_MINOR_VERSION)
            except:
                _MetaGLConfig.__gl_minor_version = cls.version.split(" ")[0].split(".")[
                    1
                ]

        return _MetaGLConfig.__gl_minor_version

    @property
    def renderer(cls) -> str:
        if _MetaGLConfig.__gl_renderer is None:
            _MetaGLConfig.__gl_renderer = GL.glGetString(GL.GL_RENDERER).decode("utf-8")

        return _MetaGLConfig.__gl_renderer

    @property
    def available_texture_units(cls):
        if _MetaGLConfig.__available_texture_units is None:
            _MetaGLConfig.__available_texture_units = set(range(cls.max_texture_units))

        return _MetaGLConfig.__available_texture_units

    @property
    def available_image_units(cls):
        if _MetaGLConfig.__available_image_units is None:
            _MetaGLConfig.__available_image_units = set(range(cls.max_image_units))

        return _MetaGLConfig.__available_image_units

    @property
    def available_extensions(cls):
        if _MetaGLConfig.__available_extensions is None:
            extensions = GL.glGetString(GL.GL_EXTENSIONS).decode("utf-8")
            _MetaGLConfig.__available_extensions = extensions.split()

        return _MetaGLConfig.__available_extensions


def setter_methods(cls):
    setters = set()
    for name, member in inspect.getmembers(cls):
        if isinstance(member, property) and member.fset is not None:
            setters.add(name)
    return setters


class GLConfig(metaclass=_MetaGLConfig):

    class LocalEnv:

        def __init__(self):
            self._recover_funcs = []
            self._old_values = {}

        def add_recover_func(self, func, *args, **kwargs):
            self._recover_funcs.append({"func": func, "args": args, "kwargs": kwargs})

        def add_old_value(self, key, old_value):
            self._old_values[key] = old_value

        def __enter__(self):
            _MetaGLConfig._active_local_env = self
            self._recover_funcs.clear()

        def __exit__(self, *exc_details):
            _MetaGLConfig._active_local_env = None

            for func_info in self._recover_funcs:
                func_info["func"](*func_info["args"], **func_info["kwargs"])

            for key, value in self._old_values.items():
                setattr(GLConfig, key, value)

    @staticmethod
    def hassetter(name:str):
        if _MetaGLConfig._all_setters is None:
            _MetaGLConfig._all_setters = setter_methods(_MetaGLConfig)

        return (name in _MetaGLConfig._all_setters)

    @staticmethod
    def clear_buffers(bits=None):
        if bits is None:
            bits = (
                GL.GL_COLOR_BUFFER_BIT
                | GL.GL_DEPTH_BUFFER_BIT
                | GL.GL_STENCIL_BUFFER_BIT
            )

        GL.glClear(bits)

    @staticmethod
    def clear_buffer(target, color: Union[Tuple[float], float, glm.vec3, glm.vec4]):
        np_color = np.array([0] * 4)
        if isinstance(color, float):
            np_color[0] = color
            np_color[1] = color
            np_color[2] = color
            np_color[3] = color
        elif len(color) == 3:
            np_color[0] = color[0]
            np_color[1] = color[1]
            np_color[2] = color[2]
            np_color[3] = 1
        elif len(color) == 4:
            np_color[0] = color[0]
            np_color[1] = color[1]
            np_color[2] = color[2]
            np_color[3] = color[3]
        else:
            raise ValueError(color)

        if 0 <= target < GLConfig.max_color_attachments:
            GL.glClearBufferfv(GL.GL_COLOR, target, np_color)
        elif (
            GL.GL_COLOR_ATTACHMENT0
            <= target
            < GL.GL_COLOR_ATTACHMENT0 + GLConfig.max_color_attachments
        ):
            GL.glClearBufferfv(GL.GL_COLOR, target - GL.GL_COLOR_ATTACHMENT0, np_color)
        elif target in [GL.GL_DEPTH, GL.GL_DEPTH_BUFFER_BIT, GL.GL_DEPTH_ATTACHMENT]:
            GL.glClearBufferfv(GL.GL_DEPTH, 0, np_color)
        elif target in [
            GL.GL_STENCIL,
            GL.GL_STENCIL_BUFFER_BIT,
            GL.GL_STENCIL_ATTACHMENT,
        ]:
            GL.glClearBufferfv(GL.GL_STENCIL, 0, np_color)
        elif target in [
            GL.GL_DEPTH_STENCIL,
            GL.GL_DEPTH_BUFFER_BIT | GL.GL_STENCIL_BUFFER_BIT,
            GL.GL_DEPTH_STENCIL_ATTACHMENT,
        ]:
            GL.glClearBufferfv(GL.GL_DEPTH_STENCIL, 0, np_color)
