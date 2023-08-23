import glm
from glass import Instance

class AffineTransform(Instance):
	def __init__(self):
		Instance.__init__(self)
		
		self["affine_transform_row0"] = glm.dvec4(1, 0, 0, 0)
		self["affine_transform_row1"] = glm.dvec4(0, 1, 0, 0)
		self["affine_transform_row2"] = glm.dvec4(0, 0, 1, 0)
		self["env_map_handle"] = 0
		self["visible"] = 1

	def apply(self, pos):
		transform_mat = glm.dmat4(self["affine_transform_row0"],
			                      self["affine_transform_row1"],
								  self["affine_transform_row2"],
								  glm.dvec4(0, 0, 0, 1))
		transform_mat = glm.transpose(transform_mat)
		result = transform_mat * glm.dvec4(*pos, 1)
		return result.xyz