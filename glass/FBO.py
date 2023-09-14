import numpy as np
from OpenGL import GL

from .FBOAttachment import FBOAttachment
from .GLInfo import GLInfo
from .GLConfig import GLConfig
from .GlassConfig import GlassConfig
from .BO import BO
from .samplerCube import samplerCube
from .sampler2DArray import sampler2DArray
from .sampler2D import sampler2D
from .isampler2D import isampler2D
from .usampler2D import usampler2D
from .sampler2DMS import sampler2DMS
from .isampler2DMS import isampler2DMS
from .usampler2DMS import usampler2DMS
from .RBO import RBO
from .utils import checktype
from .helper import get_external_format, get_channels

class FBO(BO):
	COLOR = GL.GL_COLOR_ATTACHMENT0
	DEPTH = GL.GL_DEPTH_ATTACHMENT
	STENCIL = GL.GL_STENCIL_ATTACHMENT
	DEPTH_STENCIL = GL.GL_DEPTH_STENCIL_ATTACHMENT

	_basic_info = \
	{
		"gen_func": GL.glGenFramebuffers,
		"bind_func": GL.glBindFramebuffer,
		"del_func": GL.glDeleteFramebuffers,
		"target_type": GL.GL_FRAMEBUFFER,
		"binding_type": GL.GL_FRAMEBUFFER_BINDING,
		"need_number": True,
	}

	_attachment_types = (sampler2D, sampler2DMS, isampler2D, isampler2DMS, usampler2D, usampler2DMS, samplerCube, sampler2DArray, RBO)
	_resolve_type_map = \
	{
		sampler2DMS: sampler2D,
		isampler2DMS: isampler2D,
		usampler2DMS: usampler2D
	}

	@checktype
	def __init__(self, width:int=0, height:int=0, samples:int=None, layers:int=None):
		BO.__init__(self, context_shared=False)
		self._last_active_id = 0
		self._resolved_fbo = None
		self._content_changed = False

		self._width = width
		self._height = height
		self._samples = samples
		self._layers = layers

		self._color_attachments = {}
		self._depth_attachment = None
		self._stencil_attachment = None
		self._depth_stencil_attachment = None

		self._attachments_attached = False
		self._can_resize = True
		self._auto_clear = True

	@checktype
	def attach(self, attach_point:int, attachment, internal_format:GLInfo.internal_formats=None):
		
		if self._attachments_attached:
			raise RuntimeError("attempt to attach new attachment to used FBO")
		
		if not (0 <= attach_point < GLConfig.max_color_attachments) and \
		   not (GL.GL_COLOR_ATTACHMENT0 <= attach_point < GL.GL_COLOR_ATTACHMENT0 + GLConfig.max_color_attachments) and \
		   attach_point not in GLInfo.none_color_attachment_types:
			max_value = GLConfig.max_color_attachments-1
			max_enum = GLInfo.enum_map[GL.GL_COLOR_ATTACHMENT0 + max_value]
			error_message = f"attach target(given as {attach_point}) should be in 0~{max_value} or GL_COLOR_ATTACHMENT0~{max_enum} for color attachment\n"
			error_message += f"or be one of {GLInfo.none_color_attachment_types} for other attachments."
			raise ValueError(error_message)
		
		if GL.GL_COLOR_ATTACHMENT0 <= attach_point < GL.GL_COLOR_ATTACHMENT0 + GLConfig.max_color_attachments:
			attach_point = attach_point - GL.GL_COLOR_ATTACHMENT0

		attachment_type = None
		if isinstance(attachment, type):
			attachment_type = attachment
			if attachment_type not in FBO._attachment_types:
				raise TypeError(f"only {FBO._attachment_types} can be attached. {attachment} was given.")
			attachment = None
		elif not isinstance(attachment, FBOAttachment):
			raise TypeError(f"only instance of FBOAttachment can be attached. {type(attachment)} value was given.")
		
		if GlassConfig.debug:
			if self._samples is not None and \
			attachment_type not in (sampler2DMS, isampler2DMS, usampler2DMS, RBO) and \
			not isinstance(attachment, (sampler2DMS, isampler2DMS, usampler2DMS, RBO)):
				raise TypeError("can only attach (sampler2DMS, isampler2DMS, usampler2DMS, RBO) to multi-samples FBO")
			
			if self._layers is not None and \
			attachment_type not in (sampler2DArray,) and \
			not isinstance(attachment, (sampler2DArray,)):
				raise TypeError(f"can only attach (sampler2DArray,) to multi-layers FBO, {attachment_type.__class__.__name__} were given.")

		if attachment is None:
			if internal_format is None:
				if attach_point == GL.GL_DEPTH_ATTACHMENT:
					internal_format = GL.GL_DEPTH_COMPONENT
				elif attach_point == GL.GL_STENCIL_ATTACHMENT:
					internal_format = GL.GL_STENCIL_INDEX
				elif attach_point == GL.GL_DEPTH_STENCIL_ATTACHMENT:
					internal_format = GL.GL_DEPTH24_STENCIL8
				elif attachment_type in [sampler2D, sampler2DMS, samplerCube, sampler2DArray, RBO]:
					internal_format = GL.GL_RGBA32F
				elif attachment_type in [isampler2D, isampler2DMS]:
					internal_format = GL.GL_RGBA32I
				elif attachment_type in [usampler2D, usampler2DMS]:
					internal_format = GL.GL_RGBA32UI

			attachment = attachment_type(internal_format=internal_format)
			if isinstance(attachment, (sampler2D, isampler2D, usampler2D, samplerCube, sampler2DArray)):
				attachment.wrap = GL.GL_CLAMP_TO_EDGE
				attachment.filter_mipmap = None
			internal_format = attachment.internal_format
		else:
			if internal_format is None:
				internal_format = attachment.internal_format

		if GlassConfig.debug:
			if attach_point == GL.GL_DEPTH_ATTACHMENT:
				if internal_format not in GLInfo.depth_internal_formats:
					raise ValueError(f"depth attachment internal format should be in {GLInfo.depth_internal_formats}, {internal_format} was given.")
			elif attach_point == GL.GL_STENCIL_ATTACHMENT:
				if internal_format not in GLInfo.stencil_internal_formats:
					raise ValueError(f"stencil attachment internal format should be in {GLInfo.depth_internal_formats}, {internal_format} was given.")
			elif attach_point == GL.GL_DEPTH_STENCIL_ATTACHMENT:
				if internal_format not in GLInfo.depth_stencil_internal_formats:
					raise ValueError(f"depth_stencil attachment internal format should be in {GLInfo.depth_stencil_internal_formats}, {internal_format} was given.")
			elif internal_format not in GLInfo.color_internal_formats:
				raise ValueError(f"color attachment internal format should be in {GLInfo.color_internal_formats}, {internal_format} was given.")

		attachment._fbo = self
		attachment._fbo_attach_point = attach_point
		attachment.malloc(width=self._width, height=self._height, samples=self._samples, layers=self._layers, internal_format=internal_format)
		if attach_point == GL.GL_DEPTH_ATTACHMENT:
			self._depth_attachment = attachment
		elif attach_point == GL.GL_STENCIL_ATTACHMENT:
			self._stencil_attachment = attachment
		elif attach_point == GL.GL_DEPTH_STENCIL_ATTACHMENT:
			self._depth_stencil_attachment = attachment
		else:
			self._color_attachments[attach_point] = attachment

	@property
	def width(self):
		return self._width
	
	@property
	def height(self):
		return self._height
	
	@property
	def samples(self):
		return self._samples

	def resize(self, width:int, height:int, samples:int=None, layers:int=None):
		if not self._can_resize:
			return
		
		if samples is None:
			samples = self._samples

		if layers is None:
			layers = self._layers
		
		self._can_resize = False

		if self._width == width and \
		   self._height == height and \
		   self._samples == samples and \
		   self._layers == layers:
			self._can_resize = True
			return False

		self._width = width
		self._height = height
		self._samples = samples
		self._layers = layers
		
		for attachment in self._color_attachments.values():
			attachment.resize(width, height, samples, layers)

		if self._depth_attachment is not None:
			self._depth_attachment.resize(width, height, samples, layers)

		if self._stencil_attachment is not None:
			self._stencil_attachment.resize(width, height, samples, layers)

		if self._depth_stencil_attachment is not None:
			self._depth_stencil_attachment.resize(width, height, samples, layers)

		self._can_resize = True
		return True

	def __enter__(self):
		self.bind()

	def __exit__(self, *exc_details):
		self.unbind()

	def bind(self):
		if self._width == 0 or self._height == 0:
			raise ValueError("current FBO is empty")

		self._last_active_id = FBO.active_id
		self._old_viewport = GLConfig.viewport

		if not self._attachments_attached:
			has_attachments = False
			color_locations = []
			max_color_location = 0
			for key, attachment in self._color_attachments.items():
				color_location = key
				if color_location > max_color_location:
					max_color_location = color_location

				BO.bind(self)
				attachment.bind(update_fbo=True)
				if isinstance(attachment, (sampler2D,isampler2D,usampler2D)):
					GL.glFramebufferTexture2D(GL.GL_FRAMEBUFFER, GL.GL_COLOR_ATTACHMENT0+color_location, GL.GL_TEXTURE_2D, attachment.id, 0)
				elif isinstance(attachment, (sampler2DMS,isampler2DMS,usampler2DMS)):
					GL.glFramebufferTexture2D(GL.GL_FRAMEBUFFER, GL.GL_COLOR_ATTACHMENT0+color_location, GL.GL_TEXTURE_2D_MULTISAMPLE, attachment.id, 0)
				elif isinstance(attachment, (samplerCube,sampler2DArray)):
					GL.glFramebufferTexture(GL.GL_FRAMEBUFFER, GL.GL_COLOR_ATTACHMENT0+color_location, attachment.id, 0)
				elif isinstance(attachment, RBO):
					GL.glFramebufferRenderbuffer(GL.GL_FRAMEBUFFER, GL.GL_COLOR_ATTACHMENT0+color_location, GL.GL_RENDERBUFFER, attachment.id)
				else:
					raise TypeError(f"not support attachment type {type(attachment).__name__}")
				color_locations.append(color_location)

				has_attachments = True

			if self._depth_attachment is not None:
				BO.bind(self)
				self._depth_attachment.bind(update_fbo=True)
				if isinstance(self._depth_attachment, (sampler2D,isampler2D,usampler2D)):
					GL.glFramebufferTexture2D(GL.GL_FRAMEBUFFER, GL.GL_DEPTH_ATTACHMENT, GL.GL_TEXTURE_2D, self._depth_attachment.id, 0)
				elif isinstance(self._depth_attachment, (sampler2DMS,isampler2DMS,usampler2DMS)):
					GL.glFramebufferTexture2D(GL.GL_FRAMEBUFFER, GL.GL_DEPTH_ATTACHMENT, GL.GL_TEXTURE_2D_MULTISAMPLE, self._depth_attachment.id, 0)
				elif isinstance(self._depth_attachment, (samplerCube,sampler2DArray)):
					GL.glFramebufferTexture(GL.GL_FRAMEBUFFER, GL.GL_DEPTH_ATTACHMENT, self._depth_attachment.id, 0)
				elif isinstance(self._depth_attachment, RBO):
					GL.glFramebufferRenderbuffer(GL.GL_FRAMEBUFFER, GL.GL_DEPTH_ATTACHMENT, GL.GL_RENDERBUFFER, self._depth_attachment.id)
				else:
					raise TypeError(type(self._depth_attachment))

				has_attachments = True

			if self._stencil_attachment is not None:
				BO.bind(self)
				self._stencil_attachment.bind(update_fbo=True)
				if isinstance(self._stencil_attachment, (sampler2D,isampler2D,usampler2D)):
					GL.glFramebufferTexture2D(GL.GL_FRAMEBUFFER, GL.GL_STENCIL_ATTACHMENT, GL.GL_TEXTURE_2D, self._stencil_attachment.id, 0)
				elif isinstance(self._stencil_attachment, (sampler2DMS,isampler2DMS,usampler2DMS)):
					GL.glFramebufferTexture2D(GL.GL_FRAMEBUFFER, GL.GL_STENCIL_ATTACHMENT, GL.GL_TEXTURE_2D_MULTISAMPLE, self._stencil_attachment.id, 0)
				elif isinstance(self._stencil_attachment, (samplerCube,sampler2DArray)):
					GL.glFramebufferTexture(GL.GL_FRAMEBUFFER, GL.GL_STENCIL_ATTACHMENT, self._stencil_attachment.id, 0)
				elif isinstance(self._stencil_attachment, RBO):
					GL.glFramebufferRenderbuffer(GL.GL_FRAMEBUFFER, GL.GL_STENCIL_ATTACHMENT, GL.GL_RENDERBUFFER, self._stencil_attachment.id)
				else:
					raise TypeError(type(self._stencil_attachment))

				has_attachments = True

			if self._depth_stencil_attachment is not None:
				BO.bind(self)
				self._depth_stencil_attachment.bind(update_fbo=True)
				if isinstance(self._depth_stencil_attachment, (sampler2D,isampler2D,usampler2D)):
					GL.glFramebufferTexture2D(GL.GL_FRAMEBUFFER, GL.GL_DEPTH_STENCIL_ATTACHMENT, GL.GL_TEXTURE_2D, self._depth_stencil_attachment.id, 0)
				elif isinstance(self._depth_stencil_attachment, (sampler2DMS,isampler2DMS,usampler2DMS)):
					GL.glFramebufferTexture2D(GL.GL_FRAMEBUFFER, GL.GL_DEPTH_STENCIL_ATTACHMENT, GL.GL_TEXTURE_2D_MULTISAMPLE, self._depth_stencil_attachment.id, 0)
				elif isinstance(self._depth_stencil_attachment, (samplerCube,sampler2DArray)):
					GL.glFramebufferTexture(GL.GL_FRAMEBUFFER, GL.GL_DEPTH_STENCIL_ATTACHMENT, self._depth_stencil_attachment.id, 0)
				elif isinstance(self._depth_stencil_attachment, RBO):
					GL.glFramebufferRenderbuffer(GL.GL_FRAMEBUFFER, GL.GL_DEPTH_STENCIL_ATTACHMENT, GL.GL_RENDERBUFFER, self._depth_stencil_attachment.id)
				else:
					raise TypeError(type(self._depth_stencil_attachment))

				has_attachments = True

			if not has_attachments:
				raise RuntimeError("FBO " + str(self._id) + " do not have any attachments")

			if color_locations:
				color_attach_points = []
				for i in range(max_color_location+1):
					if i in color_locations:
						color_attach_points.append(GL.GL_COLOR_ATTACHMENT0 + i)
					else:
						color_attach_points.append(GL.GL_NONE)
				GL.glDrawBuffers(len(color_attach_points), np.array(color_attach_points))
			else:
				GL.glDrawBuffer(GL.GL_NONE)
				GL.glReadBuffer(GL.GL_NONE)

			if GlassConfig.debug:
				self.check_status()

			self._attachments_attached = True
		else:
			for attachment in self._color_attachments.values():
				attachment.bind(update_fbo=True)
			if self._depth_attachment is not None:
				self._depth_attachment.bind(update_fbo=True)
			if self._stencil_attachment is not None:
				self._stencil_attachment.bind(update_fbo=True)
			if self._depth_stencil_attachment is not None:
				self._depth_stencil_attachment.bind(update_fbo=True)

		BO.bind(self)
		GLConfig.viewport = (0, 0, self._width, self._height)
		if self._auto_clear:
			GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT | GL.GL_STENCIL_BUFFER_BIT)
		
		self._content_changed = True

	def check_status(self):
		status = GL.glCheckFramebufferStatus(GL.GL_FRAMEBUFFER)
		if status == GL.GL_FRAMEBUFFER_COMPLETE:
			return
		
		error_message = status.__repr__() + ": "
		messages = GLInfo.fbo_status_errors[status]
		if isinstance(messages, list):
			error_message += "Maybe one of following reasons:\n" + "\n".join(messages)
		else:
			error_message += messages

		raise RuntimeError(error_message)

	def _unbind(self):		
		GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, self._last_active_id)
		self._last_active_id = self._id

	@property
	def auto_clear(self):
		return self._auto_clear
	
	@auto_clear.setter
	@checktype
	def auto_clear(self, flag:bool):
		self._auto_clear = flag

	def unbind(self):
		self._unbind()
		GLConfig.viewport = self._old_viewport
	
	def copy_from_active(self, *targets):
		if self.id == FBO.active_id:
			return

		targets = list(targets)
		if not targets:
			targets = [*self._color_attachments.keys(), GL.GL_DEPTH_ATTACHMENT, GL.GL_STENCIL_ATTACHMENT, GL.GL_DEPTH_STENCIL_ATTACHMENT]
		
		for i, target in enumerate(targets):
			if GL.GL_COLOR_ATTACHMENT0 <= target < GL.GL_COLOR_ATTACHMENT0 + GLConfig.max_color_attachments:
				targets[i] = target - GL.GL_COLOR_ATTACHMENT0

		viewport = GLConfig.viewport
		with self:
			GL.glBindFramebuffer(GL.GL_READ_FRAMEBUFFER, FBO.active_id)
			GL.glBindFramebuffer(GL.GL_DRAW_FRAMEBUFFER, self._id)

			for target in self._color_attachments:
				if target not in targets:
					continue

				GL.glReadBuffer(GL.GL_COLOR_ATTACHMENT0 + target)
				GL.glDrawBuffer(GL.GL_COLOR_ATTACHMENT0 + target)
				GL.glBlitFramebuffer(
					viewport[0], viewport[1], viewport[2], viewport[3],
					0, 0, self._width, self._height,
					GL.GL_COLOR_BUFFER_BIT, GL.GL_LINEAR
				)
				
			if self._depth_attachment is not None and GL.GL_DEPTH_ATTACHMENT in targets:
				GL.glBlitFramebuffer(
					viewport[0], viewport[1], viewport[2], viewport[3],
					0, 0, self._width, self._height,
					GL.GL_DEPTH_BUFFER_BIT, GL.GL_NEAREST
				)
			if self._stencil_attachment is not None and GL.GL_STENCIL_ATTACHMENT in targets:
				GL.glBlitFramebuffer(
					viewport[0], viewport[1], viewport[2], viewport[3],
					0, 0, self._width, self._height,
					GL.GL_STENCIL_BUFFER_BIT, GL.GL_NEAREST
				)
			if self._depth_stencil_attachment is not None and GL.GL_DEPTH_STENCIL_ATTACHMENT in targets:
				GL.glBlitFramebuffer(
					viewport[0], viewport[1], viewport[2], viewport[3],
					0, 0, self._width, self._height,
					GL.GL_DEPTH_BUFFER_BIT | GL.GL_STENCIL_BUFFER_BIT, GL.GL_NEAREST
				)

	def draw_to_active(self, *targets):
		if self.id == FBO.active_id:
			return

		targets = list(targets)
		if not targets:
			targets = [*self._color_attachments.keys(), GL.GL_DEPTH_ATTACHMENT, GL.GL_STENCIL_ATTACHMENT, GL.GL_DEPTH_STENCIL_ATTACHMENT]
		
		for i, target in enumerate(targets):
			if GL.GL_COLOR_ATTACHMENT0 <= target < GL.GL_COLOR_ATTACHMENT0 + GLConfig.max_color_attachments:
				targets[i] = target - GL.GL_COLOR_ATTACHMENT0

		GL.glBindFramebuffer(GL.GL_READ_FRAMEBUFFER, self._id)
		GL.glBindFramebuffer(GL.GL_DRAW_FRAMEBUFFER, FBO.active_id)

		viewport = GLConfig.viewport
		for target in self._color_attachments:
			if target not in targets:
				continue

			GL.glReadBuffer(GL.GL_COLOR_ATTACHMENT0 + target)
			GL.glDrawBuffer(GL.GL_COLOR_ATTACHMENT0 + target)
			GL.glBlitFramebuffer(
				0, 0, self._width, self._height,
				viewport[0], viewport[1], viewport[2], viewport[3],
				GL.GL_COLOR_BUFFER_BIT, GL.GL_LINEAR
			)
			
		if self._depth_attachment is not None and GL.GL_DEPTH_ATTACHMENT in targets:
			GL.glBlitFramebuffer(
				0, 0, self._width, self._height,
				viewport[0], viewport[1], viewport[2], viewport[3],
				GL.GL_DEPTH_BUFFER_BIT, GL.GL_NEAREST
			)
		if self._stencil_attachment is not None and GL.GL_STENCIL_ATTACHMENT in targets:
			GL.glBlitFramebuffer(
				0, 0, self._width, self._height,
				viewport[0], viewport[1], viewport[2], viewport[3],
				GL.GL_STENCIL_BUFFER_BIT, GL.GL_NEAREST
			)
		if self._depth_stencil_attachment is not None and GL.GL_DEPTH_STENCIL_ATTACHMENT in targets:
			GL.glBlitFramebuffer(
				0, 0, self._width, self._height,
				viewport[0], viewport[1], viewport[2], viewport[3],
				GL.GL_DEPTH_BUFFER_BIT | GL.GL_STENCIL_BUFFER_BIT, GL.GL_NEAREST
			)

	def draw_to(self, fbo, src_targets, dest_targets=None):
		if fbo is self or fbo is None or fbo.id == self.id:
			return

		if not isinstance(src_targets, list):
			src_targets = [src_targets]

		if not src_targets:
			src_targets = [*self._color_attachments.keys(), GL.GL_DEPTH_ATTACHMENT, GL.GL_STENCIL_ATTACHMENT, GL.GL_DEPTH_STENCIL_ATTACHMENT]
		
		if dest_targets is None:
			dest_targets = src_targets

		if not isinstance(dest_targets, list):
			dest_targets = [dest_targets]

		for i, target in enumerate(src_targets):
			if GL.GL_COLOR_ATTACHMENT0 <= target < GL.GL_COLOR_ATTACHMENT0 + GLConfig.max_color_attachments:
				src_targets[i] = target - GL.GL_COLOR_ATTACHMENT0

		for i, target in enumerate(dest_targets):
			if GL.GL_COLOR_ATTACHMENT0 <= target < GL.GL_COLOR_ATTACHMENT0 + GLConfig.max_color_attachments:
				dest_targets[i] = target - GL.GL_COLOR_ATTACHMENT0

		with fbo:
			GL.glBindFramebuffer(GL.GL_READ_FRAMEBUFFER, self._id)
			GL.glBindFramebuffer(GL.GL_DRAW_FRAMEBUFFER, fbo._id)

			for target in self._color_attachments:
				if target not in src_targets:
					continue

				index = src_targets.index(target)
				dest_target = dest_targets[index]

				GL.glReadBuffer(GL.GL_COLOR_ATTACHMENT0 + target)
				GL.glDrawBuffer(GL.GL_COLOR_ATTACHMENT0 + dest_target)
				GL.glBlitFramebuffer(
					0, 0, self._width, self._height,
					0, 0, fbo.width, fbo.height,
					GL.GL_COLOR_BUFFER_BIT, GL.GL_LINEAR
				)

			if self._depth_attachment is not None and GL.GL_DEPTH_ATTACHMENT in src_targets:
				GL.glBlitFramebuffer(
					0, 0, self._width, self._height,
					0, 0, fbo.width, fbo.height,
					GL.GL_DEPTH_BUFFER_BIT, GL.GL_NEAREST
				)
			if self._stencil_attachment is not None and GL.GL_STENCIL_ATTACHMENT in src_targets:
				GL.glBlitFramebuffer(
					0, 0, self._width, self._height,
					0, 0, fbo.width, fbo.height,
					GL.GL_STENCIL_BUFFER_BIT, GL.GL_NEAREST
				)
			if self._depth_stencil_attachment is not None and GL.GL_DEPTH_STENCIL_ATTACHMENT in src_targets:
				GL.glBlitFramebuffer(
					0, 0, self._width, self._height,
					0, 0, fbo.width, fbo.height,
					GL.GL_DEPTH_BUFFER_BIT | GL.GL_STENCIL_BUFFER_BIT, GL.GL_NEAREST
				)

	@staticmethod
	def _resolve_type(attachment):
		type_attachment = type(attachment)
		if type_attachment in FBO._resolve_type_map:
			type_attachment = FBO._resolve_type_map[type_attachment]
		return type_attachment

	@property
	def resolved(self):
		if self._samples is None:
			return self

		if self._resolved_fbo is None:
			self._resolved_fbo = FBO(self._width, self._height)
			for key, attachment in self._color_attachments.items():
				type_attachment = FBO._resolve_type(attachment)
				self._resolved_fbo.attach(key, type_attachment, attachment.internal_format)
			
			if self._depth_attachment is not None:
				type_attachment = FBO._resolve_type(self._depth_attachment)
				self._resolved_fbo.attach(GL.GL_DEPTH_ATTACHMENT, type_attachment, self._depth_attachment.internal_format)

			if self._stencil_attachment is not None:
				type_attachment = FBO._resolve_type(self._stencil_attachment)
				self._resolved_fbo.attach(GL.GL_STENCIL_ATTACHMENT, type_attachment, self._stencil_attachment.internal_format)

			if self._depth_stencil_attachment is not None:
				type_attachment = FBO._resolve_type(self._depth_stencil_attachment)
				self._resolved_fbo.attach(GL.GL_DEPTH_STENCIL_ATTACHMENT, type_attachment, self._depth_stencil_attachment.internal_format)
		else:
			self._resolved_fbo.resize(self._width, self._height)
		
		if self._content_changed:
			with self._resolved_fbo:
				GL.glBindFramebuffer(GL.GL_READ_FRAMEBUFFER, self._id)
				GL.glBindFramebuffer(GL.GL_DRAW_FRAMEBUFFER, self._resolved_fbo._id)
				for key, attachment in self._color_attachments.items():
					GL.glReadBuffer(GL.GL_COLOR_ATTACHMENT0 + key)
					GL.glDrawBuffer(GL.GL_COLOR_ATTACHMENT0 + key)
					GL.glBlitFramebuffer(
						0, 0, self._width, self._height,
						0, 0, self._width, self._height,
						GL.GL_COLOR_BUFFER_BIT, GL.GL_NEAREST
					)
				if self._depth_attachment is not None:
					GL.glBlitFramebuffer(
						0, 0, self._width, self._height,
						0, 0, self._width, self._height,
						GL.GL_DEPTH_BUFFER_BIT, GL.GL_NEAREST
					)
				if self._stencil_attachment is not None:
					GL.glBlitFramebuffer(
						0, 0, self._width, self._height,
						0, 0, self._width, self._height,
						GL.GL_STENCIL_BUFFER_BIT, GL.GL_NEAREST
					)
				if self._depth_stencil_attachment is not None:
					GL.glBlitFramebuffer(
						0, 0, self._width, self._height,
						0, 0, self._width, self._height,
						GL.GL_DEPTH_BUFFER_BIT | GL.GL_STENCIL_BUFFER_BIT, GL.GL_NEAREST
					)

			self._content_changed = False
		
		return self._resolved_fbo

	def color_attachment(self, key:int=0):
		try:
			return self._color_attachments[key]
		except:
			return self._color_attachments[key - GL.GL_COLOR_ATTACHMENT0]

	@property
	def depth_attachment(self):
		return self._depth_attachment

	@property
	def stencil_attachment(self):
		return self._stencil_attachment

	@property
	def depth_stencil_attachment(self):
		return self._depth_stencil_attachment

	def data(self, attach_point:int=0):
		if attach_point in [GL.GL_DEPTH_ATTACHMENT, GL.GL_STENCIL_ATTACHMENT, GL.GL_DEPTH_STENCIL_ATTACHMENT]:
			raise RuntimeError("cannot read depth or stencil data")

		attachment = None
		if GL.GL_COLOR_ATTACHMENT0 <= attach_point < GL.GL_COLOR_ATTACHMENT0 + GLConfig.max_color_attachments:
			attachment = self._color_attachments[attach_point - GL.GL_COLOR_ATTACHMENT0]
		else:
			attachment = self._color_attachments[attach_point]
			attach_point = GL.GL_COLOR_ATTACHMENT0 + attach_point			

		self._last_active_id = FBO.active_id
		BO.bind(self)
		GL.glBindBuffer(GL.GL_PIXEL_PACK_BUFFER, 0)
		GL.glReadBuffer(attach_point)
		GL.glPixelStorei(GL.GL_PACK_ALIGNMENT, 1)

		external_format = get_external_format(attachment.internal_format)
		dtype = attachment.dtype
		np_dtype = GLInfo.dtype_map[attachment.dtype]
		channels = get_channels(attachment.internal_format)

		result_data = None
		if channels == 1:
			result_data = np.zeros((self._height, self._width), dtype=np_dtype)
		else:
			result_data = np.zeros((self._height, self._width, channels), dtype=np_dtype)
		
		GL.glReadPixels(0, 0, self._width, self._height, external_format, dtype, result_data)
		self._unbind()

		return result_data

	@property
	def empty(self):
		return (self._width == 0 or self._height == 0)