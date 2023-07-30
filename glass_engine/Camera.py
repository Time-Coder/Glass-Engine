from .SinglePathNode import SinglePathNode
from .Screen import Screen

from glass.utils import checktype

import glm
import math
from enum import Enum

class Camera(SinglePathNode):

	class ProjectionMode(Enum):
		Perspective = 0
		Orthographic = 1

	@checktype
	def __init__(self, projection_mode:ProjectionMode=ProjectionMode.Perspective, name:str=""):
		SinglePathNode.__init__(self, name)
		self.__projection_type = projection_mode

		self.__fov_deg = 45
		self.__fov_rad = math.pi/4
		half_fov = self.__fov_rad/2
		self.__tan_half_fov = math.tan(half_fov)
		self.__sin_half_fov = math.sin(half_fov)
		self.__far = 100
		self.__near = 0.1
		self.__clip = self.__far - self.__near
		self.__height = 40*2*self.__near*self.__tan_half_fov
		self.__focus = 0.9*self.__near
		self.__aperture = 0.01
		self.__auto_focus = True
		self.__focus_tex_coord = glm.vec2(0.5, 0.5)
		self.__focus_change_speed = 0.005 # m/s
		self.__screen = Screen(self)
		self.__CSM_levels = 5

	@property
	def projection_mode(self):
		return self.__projection_type
	
	@projection_mode.setter
	@checktype
	def projection_mode(self, projection_mode:ProjectionMode):
		self.__projection_type = projection_mode

	@property
	def tan_half_fov(self):
		return self.__tan_half_fov
	
	@property
	def sin_half_fov(self):
		return self.__sin_half_fov

	@property
	def aspect(self):
		return self.__screen.width() / self.__screen.height()
	
	@property
	def fov_x(self):
		return 2*math.atan(self.aspect*self.__tan_half_fov)/math.pi*180
	
	@property
	def fov_y(self):
		return self.__fov_deg
	
	@property
	def fov(self):
		return self.__fov_deg
	
	@fov.setter
	@checktype
	def fov(self, angle_deg:float):
		self.__fov_deg = angle_deg
		self.__fov_rad = angle_deg/180*math.pi
		half_fov = self.__fov_rad/2
		self.__tan_half_fov = math.tan(half_fov)
		self.__sin_half_fov = math.sin(half_fov)
		self.__height = 40*2*self.__near*self.__tan_half_fov

	@property
	def fov_rad(self):
		return self.__fov_rad
	
	@fov_rad.setter
	@checktype
	def fov_rad(self, angle_rad:float):
		self.__fov_deg = angle_rad/math.pi*180
		self.__fov_rad = angle_rad
		half_fov = self.__fov_rad/2
		self.__tan_half_fov = math.tan(half_fov)
		self.__sin_half_fov = math.sin(half_fov)
		self.__height = 40*2*self.__near*self.__tan_half_fov

	@property
	def near(self):
		return self.__near
	
	@near.setter
	@checktype
	def near(self, near:float):
		self.__near = near
		self.__clip = self.__far - self.__near
		self.__height = 40*2*self.__near*self.__tan_half_fov
	
	@property
	def far(self):
		return self.__far
	
	@far.setter
	@checktype
	def far(self, far:float):
		self.__far = far
		self.__clip = self.__far - self.__near

	@property
	def clip(self):
		return self.__clip
	
	@clip.setter
	@checktype
	def clip(self, clip:float):
		self.__clip = clip
		self.__far = self.__near + clip

	@property
	def height(self):
		return self.__height

	@height.setter
	@checktype
	def height(self, height:float):
		self.__height = height

		self.__tan_half_fov = self.__height / (40*2*self.__near)
		half_fov = math.atan(self.__tan_half_fov)
		self.__fov_rad = 2*half_fov
		self.__fov_deg = self.__fov_rad/math.pi*180
		self.__sin_half_fov = math.sin(half_fov)

	@property
	def width(self):
		return self.__height * self.aspect
	
	@width.setter
	@checktype
	def width(self, width:float):
		self.__height = width / self.screen.width() * self.screen.height()

	@property
	def screen(self):
		return self.__screen
	
	@property
	def focus(self):
		return self.__focus
	
	@focus.setter
	@checktype
	def focus(self, focus:float):
		self.__focus = focus

	@property
	def aperture(self):
		return self.__aperture
	
	@aperture.setter
	@checktype
	def aperture(self, diameter:float):
		self.__aperture = diameter

	@property
	def clear_distance(self):
		return 1/(1/self.focus - 1/self.near)
	
	@clear_distance.setter
	@checktype
	def clear_distance(self, distance:float):
		self.focus = 1/(1/self.near + 1/distance)

	@property
	def auto_focus(self):
		return self.__auto_focus
	
	@auto_focus.setter
	@checktype
	def auto_focus(self, flag:bool):
		self.__auto_focus = flag

	@property
	def focus_tex_coord(self):
		return self.__focus_tex_coord
	
	@focus_tex_coord.setter
	@checktype
	def focus_tex_coord(self, tex_coord:glm.vec2):
		self.__focus_tex_coord = tex_coord

	@property
	def focus_change_speed(self):
		return self.__focus_change_speed
	
	@focus_change_speed.setter
	@checktype
	def focus_change_speed(self, speed:float):
		self.__focus_change_speed = speed

	def project(self, world_coord:glm.vec3):
		# 相机坐标系下的坐标
		q = self.abs_orientation
		p = glm.quat(q.w, -q.x, -q.y, -q.z)
		view_coord = p * (world_coord - self.abs_position)

		# 标准设备坐标系下的坐标
		device_coord = glm.vec4(0, 0, 0, 0)
		if self.projection_mode == Camera.ProjectionMode.Perspective:
			device_coord.x = view_coord.x/view_coord.y / (self.aspect * self.tan_half_fov)
			device_coord.y = view_coord.z/view_coord.y / self.tan_half_fov
			device_coord.z = 2*self.far*(1-self.near/view_coord.y)/self.clip-1
			device_coord.w = 1
		else:
			device_coord.x = 2*view_coord.x / self.width
			device_coord.y = 2*view_coord.z / self.height
			device_coord.z = 2*(view_coord.y-self.near)/self.clip-1
			device_coord.w = 1
		
		return device_coord
	
	@property
	def CSM_levels(self):
		return self.__CSM_levels
	
	@CSM_levels.setter
	@checktype
	def CSM_levels(self, levels:int):
		self.__CSM_levels = levels
