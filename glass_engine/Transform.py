import glm
from glass import Instance

class Transform(Instance):
	def __init__(self):
		Instance.__init__(self)
		
		self["col0"] = glm.vec4(1, 0, 0, 0)
		self["col1"] = glm.vec4(0, 1, 0, 0)
		self["col2"] = glm.vec4(0, 0, 1, 0)
		self["col3"] = glm.vec4(0, 0, 0, 1)
		self["env_map_handle"] = 0
		self["visible"] = 1

	def apply(self, pos:glm.vec3):
		transform_mat = glm.mat4(self["col0"], self["col1"], self["col2"], self["col3"])
		result = transform_mat * glm.vec4(pos, 1)
		return result.xyz