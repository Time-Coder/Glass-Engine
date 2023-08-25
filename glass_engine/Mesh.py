from .SceneNode import SceneNode
from .Material import Material
from .algorithm import generate_auto_TBN, generate_sharp_TBN, generate_smooth_TBN

from glass import ShaderProgram, Instances, Vertices, Indices, GLInfo, RenderHint
from glass.utils import checktype, md5s
from glass.AttrList import AttrList

import glm
from functools import wraps
from OpenGL import GL
import inspect
import types
from enum import Enum
import copy

class Mesh(SceneNode):

    __geometry_map = {}
    __builder_map = {}
    __mesh_vars = None

    class SurfType(Enum):
        Auto = 0
        Smooth = 1
        Sharp = 2

    @checktype
    def __init__(self, element_type:GLInfo.element_types=GL.GL_TRIANGLES,
                 color:(glm.vec3,glm.vec4)=glm.vec4(0.396, 0.74151, 0.69102, 1), back_color:(glm.vec3,glm.vec4)=None,
                 name:str="", block:bool=True, shared:bool=True,
                 auto_build:bool=True, surf_type:SurfType=None):
        SceneNode.__init__(self, name)

        draw_type = GL.GL_DYNAMIC_DRAW if not block else GL.GL_STATIC_DRAW
        self._vertices = Vertices(draw_type=draw_type)
        self._indices = Indices(draw_type=draw_type)

        if isinstance(color, glm.vec3):
            color = glm.vec4(color, 1)

        if isinstance(back_color, glm.vec3):
            back_color = glm.vec4(back_color, 1)

        self._color = color
        self._back_color_user_set = (back_color is not None)
        self._back_color = back_color if self._back_color_user_set else color
        self._should_add_color = True
        
        self._material = Material()
        self._material._opacity = 0
        self._material._parent_meshes.add(self)
        self._back_material = self._material
        self._back_material_user_set = False
        self._render_hint = RenderHint()
        
        self._propagation_props["explode_distance"] = 0

        self._propagation_props["tangent_scale"] = 0
        self._propagation_props["tangent_line_width"] = 2
        self._propagation_props["tangent_color"] = glm.vec4(1, 0, 0, 1)

        self._propagation_props["bitangent_scale"] = 0
        self._propagation_props["bitangent_line_width"] = 2
        self._propagation_props["bitangent_color"] = glm.vec4(0, 1, 0, 1)

        self._propagation_props["normal_scale"] = 0
        self._propagation_props["normal_line_width"] = 2
        self._propagation_props["normal_color"] = glm.vec4(0, 0, 1, 1)

        self._draw_outline_map = {}
        self._draw_all_outlines = False
        self.__outline_color = glm.vec3(1, 1, 0)
        self.__outline_width = 3

        self.__block = block
        self.__shared = shared
        self.__auto_build = auto_build
        self.__surf_type = surf_type
        self.__element_type = element_type
        self.__geometry_info = None
        self.__self_calculated_normal = False
        self.__has_transparent = False
        self.__has_opaque = True

    def __hash__(self):
        return id(self)

    def _set_transform_dirty(self, scenes):
        self._transform_dirty.update(scenes)
        return True

    @property
    def self_calculated_normal(self):
        return self.__self_calculated_normal
    
    @self_calculated_normal.setter
    def self_calculated_normal(self, flag:bool):
        self.__self_calculated_normal = flag

    @property
    def is_sphere(self):
        return (self.__class__.__name__ == "Sphere" and \
                self.scale.x == self.scale.y == self.scale.z and \
                self.span_lat >= 180 and self.span_lon >= 360) or \
               (self.__class__.__name__ == "Icosphere" and \
                self.scale.x == self.scale.y == self.scale.z)

    @property
    def has_transparent(self):
        return self.__has_transparent
    
    @property
    def has_opaque(self):
        return self.__has_opaque
    
    @property
    def is_filled(self):
        return (self.element_type in GLInfo.triangle_types)

    def build(self):
        pass

    @checktype
    def explode(self, distance:float):
        self.set_propagation_prop("explode_distance", distance)

    @property
    def explode_distance(self):
        return self.propagation_prop("explode_distance")
    
    @explode_distance.setter
    @checktype
    def explode_distance(self, distance:float):
        self.set_propagation_prop("explode_distance", distance)
    
    @checktype
    def draw_normal(self, scale:float=0.1, color:(glm.vec4,glm.vec3)=glm.vec4(0,0,1,1), normal_line_width:int=2):
        if isinstance(color, glm.vec3):
            color = glm.vec4(color, 1)

        self.set_propagation_prop("normal_scale", scale)
        self.set_propagation_prop("normal_color", color, callback=Mesh._update_mesh_callback)
        self.set_propagation_prop("normal_line_width", normal_line_width)

    @checktype
    def draw_tangent(self, scale:float=0.1, color:(glm.vec4,glm.vec3)=glm.vec4(1,0,0,1), tangent_line_width:int=2):
        if isinstance(color, glm.vec3):
            color = glm.vec4(color, 1)

        self.set_propagation_prop("tangent_scale", scale)
        self.set_propagation_prop("tangent_color", color, callback=Mesh._update_mesh_callback)
        self.set_propagation_prop("tangent_line_width", tangent_line_width)

    @checktype
    def draw_bitangent(self, scale:float=0.1, color:(glm.vec4,glm.vec3)=glm.vec4(0,1,0,1), bitangent_line_width:int=2):
        if isinstance(color, glm.vec3):
            color = glm.vec4(color, 1)

        self.set_propagation_prop("bitangent_scale", scale)
        self.set_propagation_prop("bitangent_color", color, callback=Mesh._update_mesh_callback)
        self.set_propagation_prop("bitangent_line_width", bitangent_line_width)

    @staticmethod
    def _update_mesh_callback(child):
        if not isinstance(child, Mesh):
            return
        
        for scene in child.scenes:
            scene._update_mesh(child)

    @property
    def normal_scale(self):
        return self.propagation_prop("normal_scale")
    
    @normal_scale.setter
    @checktype
    def normal_scale(self, scale:float):
        self.set_propagation_prop("normal_scale", scale, callback=Mesh._update_mesh_callback)
    
    @property
    def normal_color(self):
        return self.propagation_prop("normal_color")
    
    @normal_color.setter
    @checktype
    def normal_color(self, color:glm.vec3):
        self.set_propagation_prop("normal_color", color, callback=Mesh._update_mesh_callback)

    @property
    def normal_line_width(self):
        return self.propagation_prop("normal_line_width")
    
    @normal_line_width.setter
    @checktype
    def normal_line_width(self, width:int):
        self.set_propagation_prop("normal_line_width", width)

    @property
    def tangent_scale(self):
        return self.propagation_prop("tangent_scale")
    
    @tangent_scale.setter
    @checktype
    def tangent_scale(self, scale:float):
        self.set_propagation_prop("tangent_scale", scale, callback=Mesh._update_mesh_callback)
    
    @property
    def tangent_color(self):
        return self._tangent_color
    
    @tangent_color.setter
    @checktype
    def tangent_color(self, color:glm.vec3):
        self.set_propagation_prop("tangent_color", color, callback=Mesh._update_mesh_callback)

    @property
    def tangent_line_width(self):
        return self._tangent_line_width
    
    @tangent_line_width.setter
    @checktype
    def tangent_line_width(self, width:int):
        self.set_propagation_prop("tangent_line_width", width)

    @property
    def bitangent_scale(self):
        return self.propagation_prop("bitangent_scale")

    @bitangent_scale.setter
    @checktype
    def bitangent_scale(self, scale:float):
        self.set_propagation_prop("bitangent_scale", scale, callback=Mesh._update_mesh_callback)
    
    @property
    def bitangent_color(self):
        return self._bitangent_color
    
    @bitangent_color.setter
    @checktype
    def bitangent_color(self, color:glm.vec3):
        self.set_propagation_prop("bitangent_color", color, callback=Mesh._update_mesh_callback)

    @property
    def bitangent_line_width(self):
        return self._bitangent_line_width
    
    @bitangent_line_width.setter
    @checktype
    def bitangent_line_width(self, width:int):
        self.set_propagation_prop("bitangent_line_width", width)

    @checktype
    def draw_outline(self, node_path:(list,tuple,bool)=None, flag:bool=True, width:float=None):
        if node_path is None:
            self._draw_all_outlines = flag
            if width is not None:
                self.__outline_width = width
            return
        
        if isinstance(node_path, bool):
            self._draw_all_outlines = node_path
            if width is not None:
                self.__outline_width = width
            return

        used_path = node_path
        if used_path[-1] is not self:
            used_path = [*node_path, self]
        key = SceneNode.path_str(used_path)

        if flag:
            if width is None:
                width = self.outline_width
            self._draw_outline_map[key] = width
        else:
            del self._draw_outline_map[key]

    def has_outline(self, node_path:list=None):
        if node_path is None:
            return (self._draw_all_outlines or self._draw_outline_map)
        else:
            return (SceneNode.path_str(node_path) in self._draw_outline_map)
        
    def clear_outline(self):
        self._draw_outline_map.clear()
        self._draw_all_outlines = False

    @property
    def outline_color(self):
        return self.__outline_color
    
    @outline_color.setter
    def outline_color(self, color:glm.vec3):
        self.__outline_color = color

    @property
    def outline_width(self):
        return self.__outline_width
    
    @outline_width.setter
    def outline_width(self, width:float):
        self.__outline_width = width

    @property
    def should_add_color(self):
        return self._should_add_color
    
    @should_add_color.setter
    def should_add_color(self, flag:bool):
        self._should_add_color = flag

    def __set_color(self):
        if not self._should_add_color:
            self._test_transparent()
            return

        if "color" not in self.vertices._attr_list_map:
            self.vertices._attr_list_map["color"] = AttrList()

        if "back_color" not in self.vertices._attr_list_map:
            self.vertices._attr_list_map["back_color"] = AttrList()

        for i in range(len(self.vertices)):
            self.vertices._attr_list_map["color"][i] = self.color

        for i in range(len(self.vertices)):
            self.vertices._attr_list_map["back_color"][i] = self.back_color

        self._test_transparent()

    @property
    def color(self):
        return self._color
    
    @color.setter
    @checktype
    def color(self, color:(glm.vec3,glm.vec4)):
        if isinstance(color, glm.vec3):
            color = glm.vec4(color, 1)

        self._color = color
        if "color" not in self.vertices._attr_list_map:
            self.vertices._attr_list_map["color"] = AttrList()

        if "back_color" not in self.vertices._attr_list_map:
            self.vertices._attr_list_map["back_color"] = AttrList()

        for i in range(len(self.vertices)):
            self.vertices._attr_list_map["color"][i] = self._color

        if not self._back_color_user_set:
            for i in range(len(self.vertices)):
                self.vertices._attr_list_map["back_color"][i] = self._color

        self._test_transparent()

    @property
    def back_color(self):
        return self._back_color
    
    @back_color.setter
    @checktype
    def back_color(self, color:(glm.vec3,glm.vec4)):
        if isinstance(color, glm.vec3):
            color = glm.vec4(color, 1)

        self._back_color_user_set = True
        self._back_color = color

        if "color" not in self.vertices._attr_list_map:
            self.vertices._attr_list_map["color"] = AttrList()

        if "back_color" not in self.vertices._attr_list_map:
            self.vertices._attr_list_map["back_color"] = AttrList()

        for i in range(len(self.vertices)):
            self.vertices._attr_list_map["back_color"][i] = self._back_color

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
    def back_material(self, material:Material):
        if material is None:
            self._back_material = self._material
        elif self._back_material is not material:
            self._back_material._parent_meshes.remove(self)
            material._parent_meshes.add(self)
            self._back_material = material

        self._back_material_user_set = True

        self._test_transparent()

    @property
    def render_hint(self):
        return self._render_hint

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
    def surf_type(self, surf_type:SurfType):
        self.__surf_type = surf_type

    @property
    def block(self):
        return self.__block
    
    @block.setter
    @checktype
    def block(self, flag:bool):
        self.__block = flag

    @property
    def shared(self):
        return self.__shared
    
    @shared.setter
    @checktype
    def shared(self, flag:bool):
        self.__shared = flag

    @property
    def auto_build(self):
        return self.__auto_build
    
    @auto_build.setter
    @checktype
    def auto_build(self, flag:bool):
        self.__auto_build = flag

    @property
    def bounding_box(self):
        return (self.x_min, self.x_max, self.y_min, self.y_max, self.z_min, self.z_max)

    @property
    def center(self):
        return glm.vec3(0.5*(self.x_min + self.x_max),
                        0.5*(self.y_min + self.y_max),
                        0.5*(self.z_min + self.z_max))

    @property
    def x_min(self):
        if self.__geometry_info is None:
            return 0
        
        return self.__geometry_info["x_min"]
    
    @x_min.setter
    @checktype
    def x_min(self, x_min:float):
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
    def x_max(self, x_max:float):
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
    def y_min(self, y_min:float):
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
    def y_max(self, y_max:float):
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
    def z_min(self, z_min:float):
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
    def z_max(self, z_max:float):
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
                
                if self.__geometry_info["build_state"] == "build":
                    try:
                        while True:
                            next(builder)
                    except StopIteration:
                        del Mesh.__builder_map[builder]
                        self.__post_build(self.__geometry_info)
                        self.__geometry_info["builder"] = None
                        self.__geometry_info["build_state"] = "done"

                return
            else:
                draw_type = GL.GL_DYNAMIC_DRAW if not self.__block else GL.GL_STATIC_DRAW
                geometry_info = \
                {
                    "vertices": Vertices(draw_type=draw_type),
                    "indices": Indices(draw_type=draw_type),
                    "builder": None,
                    "build_state": "build",
                    "x_min": 0, "x_max": 0,
                    "y_min": 0, "y_max": 0,
                    "z_min": 0, "z_max": 0,
                }
                Mesh.__geometry_map[instance_key] = geometry_info
                self._vertices = geometry_info["vertices"]
                self._indices = geometry_info["indices"]
                self.__geometry_info = geometry_info
        elif self.__geometry_info is None:
            draw_type = GL.GL_DYNAMIC_DRAW if not self.__block else GL.GL_STATIC_DRAW
            self.__geometry_info = \
            {
                "vertices": Vertices(draw_type=draw_type),
                "indices": Indices(draw_type=draw_type),
                "builder": None,
                "build_state": "build",
                "x_min": 0, "x_max": 0,
                "y_min": 0, "y_max": 0,
                "z_min": 0, "z_max": 0,
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
                
            else: # not generator
                self.build()
                self.__post_build(self.__geometry_info)

            self.__geometry_info["build_state"] = "done"
        else: # not block
            if inspect.isgeneratorfunction(self.build):
                builder = self.build()
                self.__geometry_info["builder"] = builder
                Mesh.__builder_map[builder] = self.__geometry_info
                try:
                    next(builder)
                except StopIteration:
                    del Mesh.__builder_map[builder]
                    self.__post_build(self.__geometry_info)
                    self.__geometry_info["build_state"] = "done"
                    self.__geometry_info["builder"] = None
            else:
                self.build()
                self.__post_build(self.__geometry_info)
                self.__geometry_info["builder"] = None
                self.__geometry_info["build_state"] = "done"

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
            if isinstance(value, (int,float,bool,complex,str,bytes,bytearray)):
                str_value = str(value)
            else:
                try:
                    str_value = f"md5({md5s(value)})"
                except:
                    str_value = f"id({id(value)})"

            instance_key += (key + "=" + str_value)
            if i < len_new_vars-1:
                instance_key += ", "
        instance_key += ")"
        return instance_key

    @property
    def is_building(self):
        return (self.__geometry_info is not None and self.__geometry_info["builder"] is not None)

    @property
    def is_generating(self):
        return (self.__geometry_info is not None and self.__geometry_info["builder"] is not None and isinstance(self.__geometry_info["builder"], types.GeneratorType))

    def generate(self):
        builder = self.__geometry_info["builder"]
        if builder is None:
            return
        
        if self.__geometry_info["build_state"] == "build":
            try:
                next(builder)
            except StopIteration:
                del Mesh.__builder_map[builder]
                self.__post_build(self.__geometry_info)
                self.__geometry_info["builder"] = None
                self.__geometry_info["build_state"] = "done"
    
    def __eq__(self, other):
        return (id(self) == id(other))

    @property
    def vertices(self):
        return self._vertices

    @vertices.setter
    @checktype
    def vertices(self, vertices:(Vertices, list)):
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
    def indices(self, indices:(Indices, list)):
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
    def material(self, material:Material):
        if material is None:
            raise ValueError(material)

        if self._material is material:
            return

        self._material._parent_meshes.remove(self)
        material._parent_meshes.add(self)

        self._material = material
        
        if not material.opacity_user_set:
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
        
        if geometry_info["x_min"] == 0 and geometry_info["x_max"] == 0 and \
           geometry_info["y_min"] == 0 and geometry_info["y_max"] == 0 and \
           geometry_info["z_min"] == 0 and geometry_info["z_max"] == 0:
            geometry_info["x_min"] = vertices["position"].ndarray[:,0].min()
            geometry_info["x_max"] = vertices["position"].ndarray[:,0].max()
            geometry_info["y_min"] = vertices["position"].ndarray[:,1].min()
            geometry_info["y_max"] = vertices["position"].ndarray[:,1].max()
            geometry_info["z_min"] = vertices["position"].ndarray[:,2].min()
            geometry_info["z_max"] = vertices["position"].ndarray[:,2].max()

    @property
    def element_type(self):
        return self.__element_type

    @element_type.setter
    @checktype
    def element_type(self, element_type:GLInfo.element_types):
        self.__element_type = element_type

    def generate_temp_TBN(self, vertex0, vertex1, vertex2):
        if self.should_add_color:
            if "color" not in vertex0:
                vertex0.color = self.color
            if "back_color" not in vertex0:
                vertex0.back_color = self.back_color

            if "color" not in vertex1:
                vertex1.color = self.color
            if "back_color" not in vertex1:
                vertex1.back_color = self.back_color

            if "color" not in vertex2:
                vertex2.color = self.color
            if "back_color" not in vertex2:
                vertex2.back_color = self.back_color

        v01 = vertex1.position - vertex0.position
        v02 = vertex2.position - vertex0.position

        st01 = vertex1.tex_coord - vertex0.tex_coord
        st02 = vertex2.tex_coord - vertex0.tex_coord

        det = st01.s * st02.t - st02.s * st01.t
        
        normal = glm.cross(v01, v02)
        len_normal = glm.length(normal)
        if len_normal > 1E-6:
            normal = normal / len_normal
        else:
            normal = glm.vec3(0, 0, 0)

        tangent = st02.t*v01 - st01.t*v02
        bitangent = st01.s*v02 - st02.s*v01
        if abs(det) > 1E-6:
            tangent /= det
            bitangent /= det
        else:
            tangent = glm.vec3(0, 0, 0)
            bitangent = glm.vec3(0, 0, 0)
        
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
        if self.__surf_type is None:
            return
        
        vertices = geometry_info["vertices"]
        indices = geometry_info["indices"]

        if not vertices or not indices or \
           'position' not in vertices or \
           'color' not in vertices:
            return

        if self.__surf_type == Mesh.SurfType.Auto:
            generate_auto_TBN(vertices, indices, not self.self_calculated_normal)
        elif self.__surf_type == Mesh.SurfType.Sharp:
            generate_sharp_TBN(vertices, indices, not self.self_calculated_normal)
        elif self.__surf_type == Mesh.SurfType.Smooth:
            generate_smooth_TBN(vertices, indices, not self.self_calculated_normal)

    def draw(self, program:ShaderProgram, instances:Instances=None):
        if not self.visible:
            return

        with self.render_hint:
            if self.__element_type in GLInfo.triangle_types:
                program.draw_triangles(self._vertices, self._indices, instances, self.__element_type)
            elif self.__element_type in GLInfo.line_types:
                if self.__element_type in [GL.GL_LINE_STRIP, GL.GL_LINE_LOOP]:
                    program.draw_lines(self._vertices, None, instances, self.__element_type)
                else:
                    program.draw_lines(self._vertices, self._indices, instances, self.__element_type)
            elif self.__element_type == GL.GL_POINTS:
                program.draw_points(self._vertices, instances)
            elif self.__element_type == GL.GL_PATCHES:
                program.draw_patches(self._vertices, self._indices, instances)

    def _test_transparent(self):
        if not self._vertices:
            return

        front_has_transparent = self._vertices.front_has_transparent and self._material.has_transparent
        back_has_transparent = self._vertices.back_has_transparent and self._back_material.has_transparent
        self.__has_transparent = (front_has_transparent or back_has_transparent)

        front_has_opaque = self._vertices.front_has_opaque or self._material.has_opaque
        back_has_opaque = self._vertices.back_has_opaque or self._back_material.has_opaque
        self.__has_opaque = (front_has_opaque or back_has_opaque)