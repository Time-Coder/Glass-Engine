from OpenGL import GL
import OpenGL.GL.ARB.gpu_shader_int64 as gsi64
import ctypes

from .utils import checktype
from .helper import nitems, sizeof
from .GLObject import GLObject
from .GLInfo import GLInfo

class VAP:
	def __init__(self, vao, location):
		self._vao = vao
		self._location = location
		self._vbo = None
		self._element_type = None
		self._stride = 0
		self._offset = 0
		self._divisor = 0
		self._enabled = False

	def interp(self, vbo, element_type, stride = 0, offset = 0):
		self._vao.bind()
		vbo.bind()
		if stride == 0:
			stride = sizeof(element_type)

		gl_type = GLInfo.dtype_inverse_map[element_type]
		if gl_type in [GL.GL_DOUBLE, gsi64.GL_UNSIGNED_INT64_ARB]:
			GL.glVertexAttribLPointer(self._location, nitems(element_type), gl_type, stride, ctypes.c_void_p(offset))
		elif gl_type in GLInfo.int_types:
			GL.glVertexAttribIPointer(self._location, nitems(element_type), gl_type, stride, ctypes.c_void_p(offset))
		else:
			GL.glVertexAttribPointer(self._location, nitems(element_type), gl_type, GL.GL_FALSE, stride, ctypes.c_void_p(offset))
		self.enabled = True

		self._vbo = vbo
		self._element_type = element_type
		self._stride = stride
		self._offset = offset

	@property
	def vbo(self):
		return self._vbo

	@property
	def element_type(self):
		return self._element_type

	@property
	def stride(self):
		return self._stride

	@property
	def offset(self):
		return self._offset

	@property
	def divisor(self):
		return self._divisor
	
	@property
	def enabled(self):
		return self._enabled
	
	@enabled.setter
	def enabled(self, flag:bool):
		self._enabled = flag
		if flag:
			GL.glEnableVertexAttribArray(self._location)
		else:
			GL.glDisableVertexAttribArray(self._location)

	@divisor.setter
	@checktype
	def divisor(self, value:int):
		if value < 0:
			raise ValueError("divisor should be integer that not less than 0")

		if self._divisor == value:
			return

		self._divisor = value
		GL.glVertexAttribDivisor(self._location, self._divisor)
		self.enabled = True

class VAO(GLObject):

	_basic_info = \
	{
		"gen_func": GL.glGenVertexArrays,
		"bind_func": GL.glBindVertexArray,
		"del_func": GL.glDeleteVertexArrays,
		"target_type": None,
		"binding_type": GL.GL_VERTEX_ARRAY_BINDING,
		"need_number": True,
	}

	def __init__(self):
		GLObject.__init__(self)
		self._ebo = None
		self._VAP_map = {}

	def __getitem__(self, location):
		if location not in self._VAP_map:
			self._VAP_map[location] = VAP(self, location)
			
		return self._VAP_map[location]
	
	def __contains__(self, location):
		return (location in self._VAP_map)

	def setEBO(self, ebo):
		if self._ebo is ebo:
			return
			
		self.bind()
		ebo.bind()
		self._ebo = ebo

	@property
	def ebo(self):
		return self._ebo