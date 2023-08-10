from .FBOAttachment import FBOAttachment
from .GLInfo import GLInfo
from .utils import checktype
from .helper import get_dtype

from OpenGL import GL

class RBO(FBOAttachment):
	
	_basic_info = \
	{
		"gen_func": GL.glGenRenderbuffers,
		"bind_func": GL.glBindRenderbuffer,
		"del_func": GL.glDeleteRenderbuffers,
		"target_type": GL.GL_RENDERBUFFER,
		"binding_type": GL.GL_RENDERBUFFER_BINDING,
		"need_number": True,
	}

	@checktype
	def __init__(self, width:int=0, height:int=0, samples:int=None, internal_format:GLInfo.internal_formats=GL.GL_DEPTH24_STENCIL8):
		FBOAttachment.__init__(self)

		self._samples = samples
		self._width = width
		self._height = height
		self._internal_format = internal_format
		self._param_changed = True

	def bind(self, update_fbo:bool=False, force_update_image:bool=False):
		FBOAttachment.bind(self, update_fbo, force_update_image)

		if self._param_changed or force_update_image:
			if self._samples is not None:
				GL.glRenderbufferStorageMultisample(GL.GL_RENDERBUFFER, self._samples, self._internal_format, self._width, self._height)
			else:
				GL.glRenderbufferStorage(GL.GL_RENDERBUFFER, self._internal_format, self._width, self._height)
			self._param_changed = False

	@property
	def samples(self):
		return self._samples
	
	@samples.setter
	def samples(self, samples:int):
		if self._samples != samples:
			self._samples = samples
			self._param_changed = True

	@property
	def dtype(self):
		return get_dtype(self._internal_format)

	@checktype
	def malloc(self, width:int, height:int, samples:int=None, layers:int=None, internal_format:GLInfo.internal_formats=None):
		self.width = width
		self.height = height

		if internal_format is None:
			internal_format = internal_format

		if internal_format is None:
			internal_format = GL.GL_DEPTH24_STENCIL8

		self.internal_format = internal_format

		if samples is not None:
			self.samples = samples

	@property
	def width(self):
		return self._width

	@width.setter
	def width(self, width):
		if self._width != width:
			self._width = width
			self._param_changed = True

	@property
	def height(self):
		return self._height

	@height.setter
	def height(self, height):
		if self._height != height:
			self._height = height
			self._param_changed = True

	@property
	def internal_format(self):
		return self._internal_format

	@internal_format.setter
	@checktype
	def internal_format(self, format:GLInfo.internal_formats):
		if self._internal_format != format:
			self._internal_format = format
			self._param_changed = True
