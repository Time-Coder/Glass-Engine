from .Block import Block
from .UBO import UBO

from .utils import checktype
from functools import wraps

class UniformBlock(Block):
	
	_bound_vars = {}
	BO = UBO

	class HostClass:
		def __init__(self):
			self._dirty = True

		@property
		def dirty(self):
			return self._dirty
		
		@dirty.setter
		@checktype
		def dirty(self, flag:bool):
			self._dirty = flag

		def upload(self):
			if self._dirty:
				UniformBlock.upload_var(self)
				self._dirty = False

		@staticmethod
		def not_const(func):
			@wraps(func)
			def wrapper(*args, **kwargs):
				self = args[0]
				result = func(*args, **kwargs)
				self._dirty = True
				return result

	def __init__(self, shader_program):
		Block.__init__(self, shader_program)