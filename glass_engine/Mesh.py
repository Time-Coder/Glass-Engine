from .SceneNode import SceneNode
from .Material import Material
from .algorithm import generate_auto_TBN, generate_smooth_TBN
from .callback_vec import callback_vec4

from glass import ShaderProgram, Instances, Vertices, Indices, GLInfo, RenderHints
from glass.utils import checktype, md5s
from glass.AttrList import AttrList

import glm
from functools import wraps
from OpenGL import GL
import inspect
import types
from enum import Enum
import copy
import numpy as np


class Mesh(SceneNode):

    __geometry_map = {}
    __builder_map = {}
    __mesh_vars = None

    class SurfType(Enum):
        Auto = 0
        Smooth = 1
        Flat = 2

    @checktype
    def __init__(
        self,
        primitive_type: GLInfo.primitive_types = GL.GL_TRIANGLES,
        color: (glm.vec3, glm.vec4) = glm.vec4(0.396, 0.74151, 0.69102, 1),
        back_color: (glm.vec3, glm.vec4) = None,
        name: str = "",
        block: bool = True,
        shared: bool = True,
        auto_build: bool = True,
        surf_type: SurfType = None,
    ):
        SceneNode.__init__(self, name)

        draw_type = GL.GL_DYNAMIC_DRAW if not block else GL.GL_STATIC_DRAW
        self._vertices = Vertices(draw_type=draw_type)
        self._indices = Indices(draw_type=draw_type)

        if isinstance(color, glm.vec3):
            color = glm.vec4(color, 1)

        if isinstance(back_color, glm.vec3):
            back_color = glm.vec4(back_color, 1)

        self._color = callback_vec4(
            color.r, color.g, color.b, color.a, self._color_change_callback
        )
        self._back_color_user_set = back_color is not None
        if self._back_color_user_set:
            self._back_color = callback_vec4(
                back_color.r,
                back_color.g,
                back_color.b,
                back_color.a,
                self._back_color_change_callback,
            )
        else:
            self._back_color = callback_vec4(
                color.r, color.g, color.b, color.a, self._back_color_change_callback
            )

        self._should_add_color = True
        self._should_callback = True

        self._material = Material()
        self._material._opacity = 0
        self._material._parent_meshes.add(self)
        self._back_material = self._material
        self._back_material_user_set = False
        self._render_hints = RenderHints()

        self._propagation_props["explode_distance"] = 0

        self.__block = block
        self.__shared = shared
        self.__auto_build = auto_build
        self.__surf_type = surf_type
        self.__primitive = primitive_type
        self.__geometry_info = None
        self.__self_calculated_normal = False
        self.__has_transparent = False
        self.__has_opaque = True

    def __hash__(self):
        return id(self)

    @property
    def self_calculated_normal(self):
        return self.__self_calculated_normal

    @self_calculated_normal.setter
    def self_calculated_normal(self, flag: bool):
        self.__self_calculated_normal = flag

    @property
    def is_sphere(self):
        return (
            self.__class__.__name__ == "Sphere"
            and self.scale.x == self.scale.y == self.scale.z
            and self.span_lat >= 180
            and self.span_lon >= 360
        ) or (
            self.__class__.__name__ == "Icosphere"
            and self.scale.x == self.scale.y == self.scale.z
        )

    @property
    def has_transparent(self):
        return self.__has_transparent

    @property
    def has_opaque(self):
        return self.__has_opaque

    @property
    def is_filled(self):
        return self.primitive_type in GLInfo.triangle_types

    def build(self):
        pass

    @checktype
    def explode(self, distance: float):
        self.set_propagation_prop("explode_distance", distance)

    @property
    def explode_distance(self):
        return self.propagation_prop("explode_distance")

    @explode_distance.setter
    @checktype
    def explode_distance(self, distance: float):
        self.set_propagation_prop("explode_distance", distance)

    @staticmethod
    def _update_mesh_callback(child):
        if not isinstance(child, Mesh):
            return

        for scene in child.scenes:
            scene._update_mesh(child)

    @property
    def should_add_color(self):
        return self._should_add_color

    @should_add_color.setter
    def should_add_color(self, flag: bool):
        self._should_add_color = flag

    def __set_color(self):
        if not self._should_add_color:
            self._test_transparent()
            return

        color_array = np.dot(
            np.ones((len(self.vertices), 1), dtype=np.float32),
            np.array(
                [[self._color.r, self._color.g, self._color.b, self._color.a]],
                dtype=np.float32,
            ),
        )
        if "color" not in self.vertices._attr_list_map:
            self.vertices._attr_list_map["color"] = AttrList(
                color_array, dtype=glm.vec4
            )
        else:
            self.vertices._attr_list_map["color"].ndarray = color_array

        back_color_array = np.dot(
            np.ones((len(self.vertices), 1), dtype=np.float32),
            np.array(
                [
                    [
                        self._back_color.r,
                        self._back_color.g,
                        self._back_color.b,
                        self._back_color.a,
                    ]
                ],
                dtype=np.float32,
            ),
        )
        if "back_color" not in self.vertices._attr_list_map:
            self.vertices._attr_list_map["back_color"] = AttrList(
                back_color_array, dtype=glm.vec4
            )
        else:
            self.vertices._attr_list_map["back_color"].ndarray = back_color_array

        self._test_transparent()

    def _color_change_callback(self):
        if not self._should_callback:
            return

        self._should_callback = False

        color_array = np.dot(
            np.ones((len(self.vertices), 1), dtype=np.float32),
            np.array(
                [[self._color.r, self._color.g, self._color.b, self._color.a]],
                dtype=np.float32,
            ),
        )
        if "color" not in self.vertices._attr_list_map:
            self.vertices._attr_list_map["color"] = AttrList(
                color_array, dtype=glm.vec4
            )
        else:
            self.vertices._attr_list_map["color"].ndarray = color_array

        if not self._back_color_user_set:
            if "back_color" not in self.vertices._attr_list_map:
                self.vertices._attr_list_map["back_color"] = AttrList(
                    color_array, dtype=glm.vec4
                )
            else:
                self.vertices._attr_list_map["back_color"].ndarray = color_array

        self._test_transparent()

        self._should_callback = True

    @property
    def color(self) -> callback_vec4:
        old_should_callback = self._should_callback
        self._should_callback = False
        if "color" not in self.vertices._attr_list_map:
            self._color.r = 0
            self._color.g = 0
            self._color.b = 0
            self._color.a = 0
        else:
            color_array = self.vertices._attr_list_map["color"].ndarray
            if len(color_array.shape) != 2 or color_array.shape[1] != 4:
                color_array = color_array.reshape(-1, 4)

            if color_array.size > 0:
                if np.all(color_array[:, 0] == color_array[0, 0]):
                    self._color.r = color_array[0, 0]
                else:
                    self._color.r = 0

                if np.all(color_array[:, 1] == color_array[0, 1]):
                    self._color.g = color_array[0, 1]
                else:
                    self._color.g = 0

                if np.all(color_array[:, 2] == color_array[0, 2]):
                    self._color.b = color_array[0, 2]
                else:
                    self._color.b = 0

                if np.all(color_array[:, 3] == color_array[0, 3]):
                    self._color.a = color_array[0, 3]
                else:
                    self._color.a = 0

        self._should_callback = old_should_callback

        return self._color

    @color.setter
    def color(self, color: (glm.vec3, glm.vec4)):
        if isinstance(color, glm.vec3):
            color = glm.vec4(color, 1)

        color_array = np.dot(
            np.ones((len(self.vertices), 1), dtype=np.float32),
            np.array([[color.r, color.g, color.b, color.a]], dtype=np.float32),
        )
        if "color" not in self.vertices._attr_list_map:
            self.vertices._attr_list_map["color"] = AttrList(
                color_array, dtype=glm.vec4
            )
        else:
            self.vertices._attr_list_map["color"].ndarray = color_array

        if not self._back_color_user_set:
            if "back_color" not in self.vertices._attr_list_map:
                self.vertices._attr_list_map["back_color"] = AttrList(
                    color_array, dtype=glm.vec4
                )
            else:
                self.vertices._attr_list_map["back_color"].ndarray = color_array

        self._test_transparent()

    def _back_color_change_callback(self):
        if not self._should_callback:
            return

        self._should_callback = False

        self._back_color_user_set = True

        color_array = np.dot(
            np.ones((len(self.vertices), 1), dtype=np.float32),
            np.array(
                [
                    [
                        self._back_color.r,
                        self._back_color.g,
                        self._back_color.b,
                        self._back_color.a,
                    ]
                ],
                dtype=np.float32,
            ),
        )
        if "back_color" not in self.vertices._attr_list_map:
            self.vertices._attr_list_map["back_color"] = AttrList(
                color_array, dtype=glm.vec4
            )
        else:
            self.vertices._attr_list_map["back_color"].ndarray = color_array

        self._test_transparent()

        self._should_callback = True

    @property
    def back_color(self) -> callback_vec4:
        old_should_callback = self._should_callback
        self._should_callback = False
        if "back_color" not in self.vertices._attr_list_map:
            self._back_color.r = 0
            self._back_color.g = 0
            self._back_color.b = 0
            self._back_color.a = 0
        else:
            color_array = self.vertices._attr_list_map["back_color"].ndarray
            if len(color_array.shape) != 2 or color_array.shape[1] != 4:
                color_array = color_array.reshape(-1, 4)

            if color_array.size > 0:
                if np.all(color_array[:, 0] == color_array[0, 0]):
                    self._back_color.r = color_array[0, 0]
                else:
                    self._back_color.r = 0

                if np.all(color_array[:, 1] == color_array[0, 1]):
                    self._back_color.g = color_array[0, 1]
                else:
                    self._back_color.g = 0

                if np.all(color_array[:, 2] == color_array[0, 2]):
                    self._back_color.b = color_array[0, 2]
                else:
                    self._back_color.b = 0

                if np.all(color_array[:, 3] == color_array[0, 3]):
                    self._back_color.a = color_array[0, 3]
                else:
                    self._back_color.a = 0
            else:
                self._back_color.r = 0
                self._back_color.g = 0
                self._back_color.b = 0
                self._back_color.a = 0
        self._should_callback = old_should_callback

        return self._back_color

    @back_color.setter
    def back_color(self, color: (glm.vec3, glm.vec4)):
        if isinstance(color, glm.vec3):
            color = glm.vec4(color, 1)

        self._back_color_user_set = True
        color_array = np.dot(
            np.ones((len(self.vertices), 1), dtype=np.float32),
            np.array([[color.r, color.g, color.b, color.a]], dtype=np.float32),
        )
        if "back_color" not in self.vertices._attr_list_map:
            self.vertices._attr_list_map["back_color"] = AttrList(
                color_array, dtype=glm.vec4
            )
        else:
            self.vertices._attr_list_map["back_color"].ndarray = color_array

        self._test_transparent()

    @property
    def back_material(self):
        if self._back_material is self._material and not self._back_material_user_set:
            self._back_material = copy.deepcopy(self._material)
            self._back_material._parent_meshes.clear()
            self._back_material._parent_meshes.add(self)

        return self._back_material

    @back_material.setter
    @checktype
    def back_material(self, material: Material):
        if material is None:
            self._back_material = self._material
        elif self._back_material is not material:
            self._back_material._parent_meshes.remove(self)
            material._parent_meshes.add(self)
            self._back_material = material

        self._back_material_user_set = True

        self._test_transparent()

    @property
    def render_hints(self):
        return self._render_hints

    @staticmethod
    def param_setter(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            self = args[0]
            value = args[1]

            equal = False
            try:
                lvalue = getattr(self, func.__name__)
                if type(lvalue) != type(value):
                    equal = False
                else:
                    equal = bool(getattr(self, func.__name__) == value)
            except:
                equal = False

            if equal:
                return

            safe_func = checktype(func)
            return_value = safe_func(*args, **kwargs)

            if self.auto_build:
                self.start_building()

            return return_value

        return wrapper

    @property
    def surf_type(self):
        return self.__surf_type

    @surf_type.setter
    @checktype
    def surf_type(self, surf_type: SurfType):
        self.__surf_type = surf_type

    @property
    def block(self):
        return self.__block

    @block.setter
    @checktype
    def block(self, flag: bool):
        self.__block = flag

    @property
    def shared(self):
        return self.__shared

    @shared.setter
    @checktype
    def shared(self, flag: bool):
        self.__shared = flag

    @property
    def auto_build(self):
        return self.__auto_build

    @auto_build.setter
    @checktype
    def auto_build(self, flag: bool):
        self.__auto_build = flag

    @property
    def bounding_box(self):
        return (self.x_min, self.x_max, self.y_min, self.y_max, self.z_min, self.z_max)

    @property
    def center(self):
        return glm.vec3(
            0.5 * (self.x_min + self.x_max),
            0.5 * (self.y_min + self.y_max),
            0.5 * (self.z_min + self.z_max),
        )

    @property
    def x_min(self):
        if self.__geometry_info is None:
            return 0

        return self.__geometry_info["x_min"]

    @x_min.setter
    @checktype
    def x_min(self, x_min: float):
        if self.__geometry_info is None:
            return

        self.__geometry_info["x_min"] = x_min

    @property
    def x_max(self):
        if self.__geometry_info is None:
            return 0

        return self.__geometry_info["x_max"]

    @x_max.setter
    @checktype
    def x_max(self, x_max: float):
        if self.__geometry_info is None:
            return

        self.__geometry_info["x_max"] = x_max

    @property
    def y_min(self):
        if self.__geometry_info is None:
            return 0

        return self.__geometry_info["y_min"]

    @y_min.setter
    @checktype
    def y_min(self, y_min: float):
        if self.__geometry_info is None:
            return

        self.__geometry_info["y_min"] = y_min

    @property
    def y_max(self):
        if self.__geometry_info is None:
            return 0

        return self.__geometry_info["y_max"]

    @y_max.setter
    @checktype
    def y_max(self, y_max: float):
        if self.__geometry_info is None:
            return

        self.__geometry_info["y_max"] = y_max

    @property
    def z_min(self):
        if self.__geometry_info is None:
            return 0

        return self.__geometry_info["z_min"]

    @z_min.setter
    @checktype
    def z_min(self, z_min: float):
        if self.__geometry_info is None:
            return

        self.__geometry_info["z_min"] = z_min

    @property
    def z_max(self):
        if self.__geometry_info is None:
            return 0

        return self.__geometry_info["z_max"]

    @z_max.setter
    @checktype
    def z_max(self, z_max: float):
        if self.__geometry_info is None:
            return

        self.__geometry_info["z_max"] = z_max

    def __copy_vertices(self, shared_vertices):
        if self._vertices is shared_vertices:
            return

        for key, value in shared_vertices._attr_list_map.items():
            if key not in ["color", "back_color"]:
                self._vertices._attr_list_map[key] = value

        self.__set_color()

    def start_building(self):
        if self.__class__.__name__ == "Mesh":
            return

        if self.__shared:
            instance_key = self.__instance_key
            if instance_key in Mesh.__geometry_map:
                geometry_info = Mesh.__geometry_map[instance_key]
                self.__copy_vertices(geometry_info["vertices"])
                self._indices = geometry_info["indices"]
                self.__geometry_info = geometry_info
                if not self.__block:
                    return

                builder = self.__geometry_info["builder"]
                if builder is None:
                    return

                try:
                    while True:
                        next(builder)
                except StopIteration:
                    del Mesh.__builder_map[builder]
                    self.__post_build(self.__geometry_info)
                    self.__geometry_info["builder"] = None

                return
            else:
                draw_type = (
                    GL.GL_DYNAMIC_DRAW if not self.__block else GL.GL_STATIC_DRAW
                )
                geometry_info = {
                    "vertices": Vertices(draw_type=draw_type),
                    "indices": Indices(draw_type=draw_type),
                    "builder": None,
                    "x_min": 0,
                    "x_max": 0,
                    "y_min": 0,
                    "y_max": 0,
                    "z_min": 0,
                    "z_max": 0,
                }
                Mesh.__geometry_map[instance_key] = geometry_info
                self._vertices = geometry_info["vertices"]
                self._indices = geometry_info["indices"]
                self.__geometry_info = geometry_info
        elif self.__geometry_info is None:
            draw_type = GL.GL_DYNAMIC_DRAW if not self.__block else GL.GL_STATIC_DRAW
            self.__geometry_info = {
                "vertices": Vertices(draw_type=draw_type),
                "indices": Indices(draw_type=draw_type),
                "builder": None,
                "x_min": 0,
                "x_max": 0,
                "y_min": 0,
                "y_max": 0,
                "z_min": 0,
                "z_max": 0,
            }
            self._vertices = self.__geometry_info["vertices"]
            self._indices = self.__geometry_info["indices"]

        if self.__block:
            if inspect.isgeneratorfunction(self.build):
                builder = self.build()
                try:
                    while True:
                        next(builder)
                except StopIteration:
                    self.__post_build(self.__geometry_info)
                    self.__geometry_info["builder"] = None

            else:  # not generator
                self.build()
                self.__post_build(self.__geometry_info)
                self.__geometry_info["builder"] = None

        else:  # not block
            if inspect.isgeneratorfunction(self.build):
                builder = self.build()
                self.__geometry_info["builder"] = builder
                Mesh.__builder_map[builder] = self.__geometry_info
                try:
                    next(builder)
                except StopIteration:
                    del Mesh.__builder_map[builder]
                    self.__post_build(self.__geometry_info)
                    self.__geometry_info["builder"] = None
            else:
                self.build()
                self.__post_build(self.__geometry_info)
                self.__geometry_info["builder"] = None

    @property
    def __instance_key(self):
        if Mesh.__mesh_vars is None:
            temp_mesh = Mesh()
            Mesh.__mesh_vars = set(temp_mesh.__dict__.keys())

        self_vars = set(self.__dict__.keys())
        new_vars = sorted(list(self_vars - Mesh.__mesh_vars))
        len_new_vars = len(new_vars)
        instance_key = self.__class__.__name__ + "("
        for i in range(len_new_vars):
            key = new_vars[i]
            value = self.__dict__[key]
            str_value = None
            if isinstance(value, (int, float, bool, complex, str, bytes, bytearray)):
                str_value = str(value)
            else:
                try:
                    str_value = f"md5({md5s(value)})"
                except:
                    str_value = f"id({id(value)})"

            instance_key += key + "=" + str_value
            if i < len_new_vars - 1:
                instance_key += ", "
        instance_key += ")"
        return instance_key

    @property
    def is_building(self):
        return (
            self.__geometry_info is not None
            and self.__geometry_info["builder"] is not None
        )

    @property
    def is_generating(self):
        return (
            self.__geometry_info is not None
            and self.__geometry_info["builder"] is not None
            and isinstance(self.__geometry_info["builder"], types.GeneratorType)
        )

    def generate(self):
        builder = self.__geometry_info["builder"]
        if builder is None:
            return

        try:
            next(builder)
        except StopIteration:
            del Mesh.__builder_map[builder]
            self.__post_build(self.__geometry_info)
            self.__geometry_info["builder"] = None

    def __eq__(self, other):
        return id(self) == id(other)

    @property
    def vertices(self):
        return self._vertices

    @vertices.setter
    @checktype
    def vertices(self, vertices: (Vertices, list)):
        if self._vertices is vertices:
            return

        if isinstance(vertices, Vertices):
            self._vertices = vertices
        else:
            self._vertices = Vertices(vertices)

        self.__geometry_info["vertices"] = self._vertices

    @property
    def indices(self):
        return self._indices

    @indices.setter
    @checktype
    def indices(self, indices: (Indices, list)):
        if self._indices is indices:
            return

        if isinstance(indices, Indices):
            self._indices = indices
        else:
            self._indices = Indices(indices)

        self.__geometry_info["indices"] = self._indices

    @property
    def material(self):
        return self._material

    @material.setter
    @checktype
    def material(self, material: Material):
        if material is None:
            raise ValueError(material)

        if self._material is material:
            return

        self._material._parent_meshes.remove(self)
        material._parent_meshes.add(self)

        self._material = material

        if not material._opacity_user_set:
            material._opacity = 1

        if not self._back_color_user_set:
            self._back_material = material

        self._test_transparent()

    def __post_build(self, geometry_info):
        self.__set_color()
        self.__calculate_bounding_box(geometry_info)
        self.__generate_TBN(geometry_info)

    def __calculate_bounding_box(self, geometry_info):
        vertices = geometry_info["vertices"]
        if not vertices or "position" not in vertices:
            return

        if (
            geometry_info["x_min"] == 0
            and geometry_info["x_max"] == 0
            and geometry_info["y_min"] == 0
            and geometry_info["y_max"] == 0
            and geometry_info["z_min"] == 0
            and geometry_info["z_max"] == 0
        ):
            geometry_info["x_min"] = vertices["position"].ndarray[:, 0].min()
            geometry_info["x_max"] = vertices["position"].ndarray[:, 0].max()
            geometry_info["y_min"] = vertices["position"].ndarray[:, 1].min()
            geometry_info["y_max"] = vertices["position"].ndarray[:, 1].max()
            geometry_info["z_min"] = vertices["position"].ndarray[:, 2].min()
            geometry_info["z_max"] = vertices["position"].ndarray[:, 2].max()

    @property
    def primitive_type(self):
        return self.__primitive

    @primitive_type.setter
    @checktype
    def primitive_type(self, primitive_type: GLInfo.primitive_types):
        self.__primitive = primitive_type

    def generate_temp_TBN(self, vertex0, vertex1, vertex2):
        v01 = vertex1.position - vertex0.position
        v02 = vertex2.position - vertex0.position

        st01 = vertex1.tex_coord - vertex0.tex_coord
        st02 = vertex2.tex_coord - vertex0.tex_coord

        det = st01.s * st02.t - st02.s * st01.t

        normal = glm.cross(v01, v02)
        len_normal = glm.length(normal)
        if len_normal > 1e-6:
            normal = normal / len_normal
        else:
            normal = glm.vec3(0)

        tangent = st02.t * v01 - st01.t * v02
        bitangent = st01.s * v02 - st02.s * v01
        if abs(det) > 1e-6:
            tangent /= det
            bitangent /= det
        else:
            tangent = glm.vec3(0)
            bitangent = glm.vec3(0)

        # vertex0
        vertex0.tangent = tangent
        vertex0.bitangent = bitangent

        # vertex1
        vertex1.tangent = tangent
        vertex1.bitangent = bitangent

        # vertex2
        vertex2.tangent = tangent
        vertex2.bitangent = bitangent

        if not self.self_calculated_normal:
            vertex0.normal = normal
            vertex1.normal = normal
            vertex2.normal = normal

    def __generate_TBN(self, geometry_info):
        vertices = geometry_info["vertices"]
        indices = geometry_info["indices"]

        if (
            not vertices
            or not indices
            or "position" not in vertices
            or "color" not in vertices
        ):
            return

        if "tangent" not in vertices._attr_list_map:
            vertices._attr_list_map["tangent"] = AttrList(
                np.zeros_like(vertices["position"].ndarray), dtype=glm.vec3
            )

        if "bitangent" not in vertices._attr_list_map:
            vertices._attr_list_map["bitangent"] = AttrList(
                np.zeros_like(vertices["position"].ndarray), dtype=glm.vec3
            )

        if "normal" not in vertices._attr_list_map:
            vertices._attr_list_map["normal"] = AttrList(
                np.zeros_like(vertices["position"].ndarray), dtype=glm.vec3
            )

        if self.__surf_type == Mesh.SurfType.Auto:
            generate_auto_TBN(vertices, indices, not self.self_calculated_normal)
        elif self.__surf_type == Mesh.SurfType.Smooth:
            generate_smooth_TBN(vertices, indices, not self.self_calculated_normal)

    def draw(self, program: ShaderProgram, instances: Instances = None):
        if not self.visible:
            return

        with self.render_hints:
            if self.__primitive in GLInfo.triangle_types:
                program.draw_triangles(
                    vertices=self._vertices,
                    indices=self._indices,
                    instances=instances,
                    primitive_type=self.__primitive,
                )
            elif self.__primitive in GLInfo.line_types:
                if self.__primitive in [GL.GL_LINE_STRIP, GL.GL_LINE_LOOP]:
                    program.draw_lines(
                        vertices=self._vertices,
                        instances=instances,
                        primitive_type=self.__primitive,
                    )
                else:
                    program.draw_lines(
                        vertices=self._vertices,
                        indices=self._indices,
                        instances=instances,
                        primitive_type=self.__primitive,
                    )
            elif self.__primitive == GL.GL_POINTS:
                program.draw_points(vertices=self._vertices, instances=instances)
            elif self.__primitive == GL.GL_PATCHES:
                program.draw_patches(
                    vertices=self._vertices, indices=self._indices, instances=instances
                )

    def _test_transparent(self):
        if not self._vertices:
            return

        front_has_transparent = (
            self._vertices.front_has_transparent and self._material.has_transparent
        )
        back_has_transparent = (
            self._vertices.back_has_transparent and self._back_material.has_transparent
        )
        self.__has_transparent = front_has_transparent or back_has_transparent

        front_has_opaque = self._vertices.front_has_opaque or self._material.has_opaque
        back_has_opaque = (
            self._vertices.back_has_opaque or self._back_material.has_opaque
        )
        self.__has_opaque = front_has_opaque or back_has_opaque
