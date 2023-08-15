from enum import Enum
import numpy as np

from glass.utils import checktype

class ColorMap:
	class Type(Enum):
		parula = 0
		jet = 1
	
	@staticmethod
	def parula(min_value=None, max_value=None):
		color_map = ColorMap(ColorMap.Type.parula)
		if min_value is not None and max_value is not None:
			color_map.range = (min_value, max_value)

		return color_map
	
	@staticmethod
	def jet(min_value=None, max_value=None):
		color_map = ColorMap(ColorMap.Type.jet)
		if min_value is not None and max_value is not None:
			color_map.range = (min_value, max_value)

		return color_map
	
	def __call__(self, value:(float,np.ndarray)):
		if isinstance(value, (float,int)):
			value = np.array([1.0*value])

		x = (value if self.__type == ColorMap.Type.jet else value.flatten())
		if self.max_value != self.min_value:
			x = (x - self.min_value)/(self.max_value - self.min_value)

		if self.__type == ColorMap.Type.parula:
			r = np.interp(x, self.__x, self.__r).reshape(value.shape)
			g = np.interp(x, self.__x, self.__g).reshape(value.shape)
			b = np.interp(x, self.__x, self.__b).reshape(value.shape)
			a = np.ones_like(r)
			return np.dstack((r, g, b, a))
		elif self.__type == ColorMap.Type.jet:
			r = np.exp( - 60.0 * np.power(np.abs(x - 0.75), 3.2) )
			g = np.exp( - 60.0 * np.power(np.abs(x - 0.50), 3.2) )
			b = np.exp( - 60.0 * np.power(np.abs(x - 0.25), 3.2) )
			a = np.ones_like(r)
			return np.dstack((r, g, b, a))

	@property
	def range(self):
		return self.__range
	
	@range.setter
	@checktype
	def range(self, range:(tuple,list)):
		self.__range = list(range)
	
	@property
	def min_value(self):
		return self.__range[0]
	
	@min_value.setter
	@checktype
	def min_value(self, min_value:float):
		self.__range[0] = min_value
	
	@property
	def max_value(self):
		return self.__range[1]
	
	@max_value.setter
	@checktype
	def max_value(self, max_value:float):
		self.__range[1] = max_value

	@checktype
	def __init__(self, type:Type):
		self.__type = type
		self.__range = [0, 1]
		if type == ColorMap.Type.parula:
			self.__colors = \
			np.array([
				[0.2081, 0.1663, 0.5292],
				[0.2091, 0.1721, 0.5411],
				[0.2101, 0.1779, 0.5530],
				[0.2109, 0.1837, 0.5650],
				[0.2116, 0.1895, 0.5771],
				[0.2121, 0.1954, 0.5892],
				[0.2124, 0.2013, 0.6013],
				[0.2125, 0.2072, 0.6135],
				[0.2123, 0.2132, 0.6258],
				[0.2118, 0.2192, 0.6381],
				[0.2111, 0.2253, 0.6505],
				[0.2099, 0.2315, 0.6629],
				[0.2084, 0.2377, 0.6753],
				[0.2063, 0.2440, 0.6878],
				[0.2038, 0.2503, 0.7003],
				[0.2006, 0.2568, 0.7129],
				[0.1968, 0.2632, 0.7255],
				[0.1921, 0.2698, 0.7381],
				[0.1867, 0.2764, 0.7507],
				[0.1802, 0.2832, 0.7634],
				[0.1728, 0.2902, 0.7762],
				[0.1641, 0.2975, 0.7890],
				[0.1541, 0.3052, 0.8017],
				[0.1427, 0.3132, 0.8145],
				[0.1295, 0.3217, 0.8269],
				[0.1147, 0.3306, 0.8387],
				[0.0986, 0.3397, 0.8495],
				[0.0816, 0.3486, 0.8588],
				[0.0646, 0.3572, 0.8664],
				[0.0482, 0.3651, 0.8722],
				[0.0329, 0.3724, 0.8765],
				[0.0213, 0.3792, 0.8796],
				[0.0136, 0.3853, 0.8815],
				[0.0086, 0.3911, 0.8827],
				[0.0060, 0.3965, 0.8833],
				[0.0051, 0.4017, 0.8834],
				[0.0054, 0.4066, 0.8831],
				[0.0067, 0.4113, 0.8825],
				[0.0089, 0.4159, 0.8816],
				[0.0116, 0.4203, 0.8805],
				[0.0148, 0.4246, 0.8793],
				[0.0184, 0.4288, 0.8779],
				[0.0223, 0.4329, 0.8763],
				[0.0264, 0.4370, 0.8747],
				[0.0306, 0.4410, 0.8729],
				[0.0349, 0.4449, 0.8711],
				[0.0394, 0.4488, 0.8692],
				[0.0437, 0.4526, 0.8672],
				[0.0477, 0.4564, 0.8652],
				[0.0514, 0.4602, 0.8632],
				[0.0549, 0.4640, 0.8611],
				[0.0582, 0.4677, 0.8589],
				[0.0612, 0.4714, 0.8568],
				[0.0640, 0.4751, 0.8546],
				[0.0666, 0.4788, 0.8525],
				[0.0689, 0.4825, 0.8503],
				[0.0710, 0.4862, 0.8481],
				[0.0729, 0.4899, 0.8460],
				[0.0746, 0.4937, 0.8439],
				[0.0761, 0.4974, 0.8418],
				[0.0773, 0.5012, 0.8398],
				[0.0782, 0.5051, 0.8378],
				[0.0789, 0.5089, 0.8359],
				[0.0794, 0.5129, 0.8341],
				[0.0795, 0.5169, 0.8324],
				[0.0793, 0.5210, 0.8308],
				[0.0788, 0.5251, 0.8293],
				[0.0778, 0.5295, 0.8280],
				[0.0764, 0.5339, 0.8270],
				[0.0746, 0.5384, 0.8261],
				[0.0724, 0.5431, 0.8253],
				[0.0698, 0.5479, 0.8247],
				[0.0668, 0.5527, 0.8243],
				[0.0636, 0.5577, 0.8239],
				[0.0600, 0.5627, 0.8237],
				[0.0562, 0.5677, 0.8234],
				[0.0523, 0.5727, 0.8231],
				[0.0484, 0.5777, 0.8228],
				[0.0445, 0.5826, 0.8223],
				[0.0408, 0.5874, 0.8217],
				[0.0372, 0.5922, 0.8209],
				[0.0342, 0.5968, 0.8198],
				[0.0317, 0.6012, 0.8186],
				[0.0296, 0.6055, 0.8171],
				[0.0279, 0.6097, 0.8154],
				[0.0265, 0.6137, 0.8135],
				[0.0255, 0.6176, 0.8114],
				[0.0248, 0.6214, 0.8091],
				[0.0243, 0.6250, 0.8066],
				[0.0239, 0.6285, 0.8039],
				[0.0237, 0.6319, 0.8010],
				[0.0235, 0.6352, 0.7980],
				[0.0233, 0.6384, 0.7948],
				[0.0231, 0.6415, 0.7916],
				[0.0230, 0.6445, 0.7881],
				[0.0229, 0.6474, 0.7846],
				[0.0227, 0.6503, 0.7810],
				[0.0227, 0.6531, 0.7773],
				[0.0232, 0.6558, 0.7735],
				[0.0238, 0.6585, 0.7696],
				[0.0246, 0.6611, 0.7656],
				[0.0263, 0.6637, 0.7615],
				[0.0282, 0.6663, 0.7574],
				[0.0306, 0.6688, 0.7532],
				[0.0338, 0.6712, 0.7490],
				[0.0373, 0.6737, 0.7446],
				[0.0418, 0.6761, 0.7402],
				[0.0467, 0.6784, 0.7358],
				[0.0516, 0.6808, 0.7313],
				[0.0574, 0.6831, 0.7267],
				[0.0629, 0.6854, 0.7221],
				[0.0692, 0.6877, 0.7173],
				[0.0755, 0.6899, 0.7126],
				[0.0820, 0.6921, 0.7078],
				[0.0889, 0.6943, 0.7029],
				[0.0956, 0.6965, 0.6979],
				[0.1031, 0.6986, 0.6929],
				[0.1104, 0.7007, 0.6878],
				[0.1180, 0.7028, 0.6827],
				[0.1258, 0.7049, 0.6775],
				[0.1335, 0.7069, 0.6723],
				[0.1418, 0.7089, 0.6669],
				[0.1499, 0.7109, 0.6616],
				[0.1585, 0.7129, 0.6561],
				[0.1671, 0.7148, 0.6507],
				[0.1758, 0.7168, 0.6451],
				[0.1849, 0.7186, 0.6395],
				[0.1938, 0.7205, 0.6338],
				[0.2033, 0.7223, 0.6281],
				[0.2128, 0.7241, 0.6223],
				[0.2224, 0.7259, 0.6165],
				[0.2324, 0.7275, 0.6107],
				[0.2423, 0.7292, 0.6048],
				[0.2527, 0.7308, 0.5988],
				[0.2631, 0.7324, 0.5929],
				[0.2735, 0.7339, 0.5869],
				[0.2845, 0.7354, 0.5809],
				[0.2953, 0.7368, 0.5749],
				[0.3064, 0.7381, 0.5689],
				[0.3177, 0.7394, 0.5630],
				[0.3289, 0.7406, 0.5570],
				[0.3405, 0.7417, 0.5512],
				[0.3520, 0.7428, 0.5453],
				[0.3635, 0.7438, 0.5396],
				[0.3753, 0.7446, 0.5339],
				[0.3869, 0.7454, 0.5283],
				[0.3986, 0.7461, 0.5229],
				[0.4103, 0.7467, 0.5175],
				[0.4218, 0.7473, 0.5123],
				[0.4334, 0.7477, 0.5072],
				[0.4447, 0.7482, 0.5021],
				[0.4561, 0.7485, 0.4972],
				[0.4672, 0.7487, 0.4924],
				[0.4783, 0.7489, 0.4877],
				[0.4892, 0.7491, 0.4831],
				[0.5000, 0.7491, 0.4786],
				[0.5106, 0.7492, 0.4741],
				[0.5212, 0.7492, 0.4698],
				[0.5315, 0.7491, 0.4655],
				[0.5418, 0.7490, 0.4613],
				[0.5519, 0.7489, 0.4571],
				[0.5619, 0.7487, 0.4531],
				[0.5718, 0.7485, 0.4490],
				[0.5816, 0.7482, 0.4451],
				[0.5913, 0.7479, 0.4412],
				[0.6009, 0.7476, 0.4374],
				[0.6103, 0.7473, 0.4335],
				[0.6197, 0.7469, 0.4298],
				[0.6290, 0.7465, 0.4261],
				[0.6382, 0.7460, 0.4224],
				[0.6473, 0.7456, 0.4188],
				[0.6564, 0.7451, 0.4152],
				[0.6653, 0.7446, 0.4116],
				[0.6742, 0.7441, 0.4081],
				[0.6830, 0.7435, 0.4046],
				[0.6918, 0.7430, 0.4011],
				[0.7004, 0.7424, 0.3976],
				[0.7091, 0.7418, 0.3942],
				[0.7176, 0.7412, 0.3908],
				[0.7261, 0.7405, 0.3874],
				[0.7346, 0.7399, 0.3840],
				[0.7430, 0.7392, 0.3806],
				[0.7513, 0.7385, 0.3773],
				[0.7596, 0.7378, 0.3739],
				[0.7679, 0.7372, 0.3706],
				[0.7761, 0.7364, 0.3673],
				[0.7843, 0.7357, 0.3639],
				[0.7924, 0.7350, 0.3606],
				[0.8005, 0.7343, 0.3573],
				[0.8085, 0.7336, 0.3539],
				[0.8166, 0.7329, 0.3506],
				[0.8246, 0.7322, 0.3472],
				[0.8325, 0.7315, 0.3438],
				[0.8405, 0.7308, 0.3404],
				[0.8484, 0.7301, 0.3370],
				[0.8563, 0.7294, 0.3336],
				[0.8642, 0.7288, 0.3300],
				[0.8720, 0.7282, 0.3265],
				[0.8798, 0.7276, 0.3229],
				[0.8877, 0.7271, 0.3193],
				[0.8954, 0.7266, 0.3156],
				[0.9032, 0.7262, 0.3117],
				[0.9110, 0.7259, 0.3078],
				[0.9187, 0.7256, 0.3038],
				[0.9264, 0.7256, 0.2996],
				[0.9341, 0.7256, 0.2953],
				[0.9417, 0.7259, 0.2907],
				[0.9493, 0.7264, 0.2859],
				[0.9567, 0.7273, 0.2808],
				[0.9639, 0.7285, 0.2754],
				[0.9708, 0.7303, 0.2696],
				[0.9773, 0.7326, 0.2634],
				[0.9831, 0.7355, 0.2570],
				[0.9882, 0.7390, 0.2504],
				[0.9922, 0.7431, 0.2437],
				[0.9952, 0.7476, 0.2373],
				[0.9973, 0.7524, 0.2310],
				[0.9986, 0.7573, 0.2251],
				[0.9991, 0.7624, 0.2195],
				[0.9990, 0.7675, 0.2141],
				[0.9985, 0.7726, 0.2090],
				[0.9976, 0.7778, 0.2042],
				[0.9964, 0.7829, 0.1995],
				[0.9950, 0.7880, 0.1949],
				[0.9933, 0.7931, 0.1905],
				[0.9914, 0.7981, 0.1863],
				[0.9894, 0.8032, 0.1821],
				[0.9873, 0.8083, 0.1780],
				[0.9851, 0.8133, 0.1740],
				[0.9828, 0.8184, 0.1700],
				[0.9805, 0.8235, 0.1661],
				[0.9782, 0.8286, 0.1622],
				[0.9759, 0.8337, 0.1583],
				[0.9736, 0.8389, 0.1544],
				[0.9713, 0.8441, 0.1505],
				[0.9692, 0.8494, 0.1465],
				[0.9672, 0.8548, 0.1425],
				[0.9654, 0.8603, 0.1385],
				[0.9638, 0.8659, 0.1343],
				[0.9623, 0.8716, 0.1301],
				[0.9611, 0.8774, 0.1258],
				[0.9600, 0.8834, 0.1215],
				[0.9593, 0.8895, 0.1171],
				[0.9588, 0.8958, 0.1126],
				[0.9586, 0.9022, 0.1082],
				[0.9587, 0.9088, 0.1036],
				[0.9591, 0.9155, 0.0990],
				[0.9599, 0.9225, 0.0944],
				[0.9610, 0.9296, 0.0897],
				[0.9624, 0.9368, 0.0850],
				[0.9641, 0.9443, 0.0802],
				[0.9662, 0.9518, 0.0753],
				[0.9685, 0.9595, 0.0703],
				[0.9710, 0.9673, 0.0651],
				[0.9736, 0.9752, 0.0597],
				[0.9763, 0.9831, 0.0538]
			])
			self.__r = self.__colors[:, 0]
			self.__g = self.__colors[:, 1]
			self.__b = self.__colors[:, 2]
			self.__x = np.linspace(0, 1, len(self.__r))