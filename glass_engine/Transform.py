import glm
from glass import Instance
from glass.utils import vec4_to_quat

class Transform(Instance):
	def __init__(self):
		Instance.__init__(self)
		
		self["abs_position"] = glm.vec3(0, 0, 0)
		self["abs_orientation"] = glm.vec4(1, 0, 0, 0)
		self["abs_scale"] = glm.vec3(1, 1, 1)
		self["env_map_handle"] = 0
		self["visible"] = 1

	def update(self, other):
		self["abs_position"] = other["abs_position"]
		self["abs_orientation"] = other["abs_orientation"]
		self["abs_scale"] = other["abs_scale"]
		self["visible"] = other["visible"]

	def apply(self, pos):
		abs_orientation = vec4_to_quat(self["abs_orientation"])
		return abs_orientation * (self["abs_scale"] * pos) + self["abs_position"]
	
	def inverse_apply(self, pos):
		abs_orientation = vec4_to_quat(self["abs_orientation"])
		return glm.inverse(abs_orientation) * (pos - self["abs_position"]) / self["abs_scale"]