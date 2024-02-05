from OpenGL import GL
import warnings

from .GPUProgram import GPUProgram, LinkError, LinkWarning
from .Shaders import ComputeShader
from .GLConfig import GLConfig
from .GlassConfig import GlassConfig


class ComputeProgram(GPUProgram):

    def __init__(self) -> None:
        GPUProgram.__init__(self)
        self.compute_shader = ComputeShader()
        self._work_group_size: tuple = None
        self._should_join: bool = False

    @staticmethod
    def _check_work_group_size(work_group_size: tuple) -> None:
        max_work_group_size = GLConfig.max_compute_work_group_size
        if work_group_size[0] > max_work_group_size[0]:
            raise ValueError(
                "x-dimension work group size should not be greater than "
                + str(max_work_group_size[0])
                + ", "
                + str(work_group_size[0])
                + " were given"
            )
        if work_group_size[1] > max_work_group_size[1]:
            raise ValueError(
                "y-dimension work group size should not be greater than "
                + str(max_work_group_size[1])
                + ", "
                + str(work_group_size[1])
                + " were given"
            )
        if work_group_size[2] > max_work_group_size[2]:
            raise ValueError(
                "z-dimension work group size should not be greater than "
                + str(max_work_group_size[2])
                + ", "
                + str(work_group_size[2])
                + " were given"
            )

        max_work_group_invocations = GLConfig.max_compute_work_group_invocations
        work_group_invocations = (
            work_group_size[0] * work_group_size[1] * work_group_size[2]
        )
        if work_group_invocations > max_work_group_invocations:
            raise ValueError(
                "work group invocation should not be greater than "
                + str(max_work_group_invocations)
                + ", "
                + str(work_group_invocations)
                + " were given"
            )

    @staticmethod
    def _check_work_group_count(work_group_count: tuple) -> None:
        max_work_group_count = GLConfig.max_compute_work_group_count
        if work_group_count[0] > max_work_group_count[0]:
            raise ValueError(
                "x-dimension work group size should not be greater than "
                + str(max_work_group_count[0])
                + ", "
                + str(work_group_count[0])
                + " were given"
            )
        if work_group_count[1] > max_work_group_count[1]:
            raise ValueError(
                "y-dimension work group size should not be greater than "
                + str(max_work_group_count[1])
                + ", "
                + str(work_group_count[1])
                + " were given"
            )
        if work_group_count[2] > max_work_group_count[2]:
            raise ValueError(
                "z-dimension work group size should not be greater than "
                + str(max_work_group_count[2])
                + ", "
                + str(work_group_count[2])
                + " were given"
            )

    def compile(self, file_name: str) -> None:
        self.compute_shader = ComputeShader.load(file_name)

        self._work_group_size = self.compute_shader.work_group_side
        self._uniforms_info = self.compute_shader.uniforms_info
        self._uniform_blocks_info = self.compute_shader.uniform_blocks_info
        self._shader_storage_blocks_info = (
            self.compute_shader._shader_storage_blocks_info
        )
        self._structs_info = self.compute_shader._structs_info

        ComputeProgram._check_work_group_size(self._work_group_size)

        self._is_linked = False

    def _apply(self) -> None:
        if not self._linked_but_not_applied:
            return

        if self._id == 0:
            self._id = GL.glCreateProgram()
            if self._id == 0:
                raise MemoryError("failed to create ComputeProgram")

        GL.glAttachShader(self._id, self.compute_shader._id)
        GL.glLinkProgram(self._id)

        if GlassConfig.debug:
            message_bytes = GL.glGetProgramInfoLog(self._id)
            message = message_bytes
            if isinstance(message_bytes, bytes):
                message = str(message_bytes, encoding="utf-8")

            error_messages, warning_messages = self._format_error_warning(message)
            if warning_messages and GlassConfig.warning:
                warnings.warn("\n" + "\n".join(warning_messages), category=LinkWarning)

            if error_messages:
                self._is_linked = False
                raise LinkError("\n" + "\n".join(error_messages))

        self._apply_uniform_blocks()
        self._apply_shader_storage_blocks()

        self._linked_but_not_applied = True

    def _link(self) -> None:
        if self._is_linked:
            return

        if not self.compute_shader.is_compiled:
            raise RuntimeError("should compile compute shader before link")

        self._resolve_uniforms()
        self._resolve_uniform_blocks()
        self._resolve_shader_storage_blocks()

        self._is_linked = True
        self._linked_but_not_applied = True
        if GL.glCreateProgram:
            self._apply()

    def start_computing(
        self,
        x_work_group_count: int,
        y_work_group_count: int = 1,
        z_work_group_count: int = 1,
    ) -> None:
        ComputeProgram._check_work_group_count(
            (x_work_group_count, y_work_group_count, z_work_group_count)
        )
        self.use()
        GL.glDispatchCompute(x_work_group_count, y_work_group_count, z_work_group_count)
        self._should_join = True

    def join(self, barrier_type=GL.GL_ALL_BARRIER_BITS) -> None:
        if self._should_join:
            GL.glMemoryBarrier(barrier_type)
            self._should_join = False

    def compute(
        self,
        x_work_group_count: int,
        y_work_group_count: int = 1,
        z_work_group_count: int = 1,
        barrier=GL.GL_ALL_BARRIER_BITS,
    ) -> None:
        self.start_computing(x_work_group_count, y_work_group_count, z_work_group_count)
        self.join(barrier)

    @property
    def work_group_size(self) -> tuple:
        return self._work_group_size

    @property
    def related_files(self) -> list:
        return [self.compute_shader._file_name]
