from .BO import BO

from OpenGL import GL

class EBO(BO):

	_basic_info = \
	{
		"gen_func": GL.glGenBuffers,
		"bind_func": GL.glBindBuffer,
		"del_func": GL.glDeleteBuffers,
		"target_type": GL.GL_ELEMENT_ARRAY_BUFFER,
		"binding_type": GL.GL_ELEMENT_ARRAY_BUFFER_BINDING,
		"need_number": True,
	}

	def __init__(self):
		BO.__init__(self)