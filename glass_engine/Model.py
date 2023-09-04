from .SceneNode import SceneNode
from .Mesh import Mesh
from .Material import Material

from glass.utils import checktype
from glass.AttrList import AttrList
from glass import Vertices, sampler2D, Indices, GLInfo

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/AssimpModelLoader")
import AssimpModelLoader
import glm
import numpy as np
from OpenGL import GL

class AssimpImportError(Exception):
    pass

class ModelMesh(Mesh):

    @checktype
    def __init__(self, assimp_mesh:AssimpModelLoader.Mesh, block:bool=True, shared:bool=False):
        Mesh.__init__(self, name=assimp_mesh.name, block=block, shared=shared)
        self.__assimp_mesh = assimp_mesh
        self.start_building()

    def build(self):
        assimp_mesh = self.__assimp_mesh

        np_dtype = GLInfo.np_dtype_map[glm.vec3]
        np_array = np.frombuffer(assimp_mesh.position_buffer, dtype=np_dtype).reshape((-1, 3))
        xx, yy, zz = np_array[:,0], np_array[:,1], np_array[:,2]
        self.x_min, self.x_max = float(xx.min()), float(xx.max())
        self.y_min, self.y_max = float(yy.min()), float(yy.max())
        self.z_min, self.z_max = float(zz.min()), float(zz.max())
        self.should_add_color = False
        self.vertices = Vertices(
            position=AttrList.fromarray(np_array, glm.vec3),
            tangent=AttrList.frombuffer(assimp_mesh.tangent_buffer, glm.vec3),
            bitangent=AttrList.frombuffer(assimp_mesh.bitangent_buffer, glm.vec3),
            normal=AttrList.frombuffer(assimp_mesh.normal_buffer, glm.vec3),
            tex_coord=AttrList.frombuffer(assimp_mesh.tex_coord_buffers[0], glm.vec3),
            color=AttrList.frombuffer(assimp_mesh.color_buffers[0], glm.vec4),
            back_color=AttrList.frombuffer(assimp_mesh.color_buffers[1], glm.vec4)
        )
        self.indices = Indices.frombuffer(assimp_mesh.indices_buffer, glm.uvec3)

class Model(SceneNode):

    __model_map = {}

    @checktype
    def __init__(self, file_name:str="", block:bool=True, dynamic:bool=False):
        self.__block = block
        self.__dynamic = dynamic

        if file_name:
            name = os.path.basename(file_name)
            SceneNode.__init__(self, name)
            self.load(file_name, block, dynamic)
        else:
            SceneNode.__init__(self, "")

    @property
    def block(self):
        return self.__block
    
    @property
    def dynamic(self):
        return self.__dynamic

    @checktype
    def load(self, file_name:str, block=True, dynamic=False):
        if not os.path.isfile(file_name):
            raise FileNotFoundError(file_name)
        
        self.__block = block
        self.__dynamic = dynamic
        self.__file_name = os.path.abspath(file_name)
        self.__dir_name = os.path.dirname(file_name)

        self["root"].clear_children()
        if not self.__dynamic and self.__file_name in Model.__model_map:
            loaded_model_root = Model.__model_map[self.__file_name]
            for child in loaded_model_root.children.values():
                self["root"].add_child(child)
            return

        self.__materials = []
        self.__meshes = []

        assimp_model = AssimpModelLoader.load(self.__file_name)
        if not assimp_model.success:
            raise AssimpImportError(assimp_model.error_message)
        if not assimp_model.nodes or \
           (not assimp_model.nodes[0].children and not assimp_model.nodes[0].meshes):
            return

        for assimp_material in assimp_model.materials:
            material = Material()

            ambient = glm.vec3(assimp_material.ambient.r, assimp_material.ambient.g, assimp_material.ambient.b)
            diffuse = glm.vec3(assimp_material.diffuse.r, assimp_material.diffuse.g, assimp_material.diffuse.b)
            specular = glm.vec3(assimp_material.specular.r, assimp_material.specular.g, assimp_material.specular.b)
            emission = glm.vec3(assimp_material.emission.r, assimp_material.emission.g, assimp_material.emission.b)
            reflection = glm.vec4(assimp_material.reflection.r, assimp_material.reflection.g, assimp_material.reflection.b, assimp_material.reflection.a)
            base_color = glm.vec3(assimp_material.base_color.r, assimp_material.base_color.g, assimp_material.base_color.b)
            shininess = assimp_material.shininess
            shininess_strength = assimp_material.shininess_strength
            opacity = assimp_material.opacity
            refractive_index = assimp_material.refractive_index
            roughness = assimp_material.roughness
            metallic = assimp_material.metallic

            if glm.length(ambient) > 0:
                material.ambient = ambient

            if glm.length(diffuse) > 0:
                material.diffuse = diffuse

            if glm.length(specular) > 0:
                material.specular = specular

            if glm.length(emission) > 0:
                material.emission = emission

            if glm.length(reflection) > 0:
                material.reflection = reflection

            if glm.length(base_color) > 0:
                material.base_color = base_color

            if refractive_index > 0:
                material.refractive_index = refractive_index

            if shininess > 0:
                material.shininess = shininess

            if shininess_strength > 0:
                material.shininess_strength = shininess_strength

            material.shading_model = Material.ShadingModel(assimp_material.shading_model.value)
            material.roughness = roughness
            material.metallic = metallic
            material.opacity = opacity
            texture_maps = \
            [
                "ambient_map", "diffuse_map", "specular_map",
                "shininess_map", "emission_map", "height_map",
                "normal_map", "opacity_map", "reflection_map",
                "base_color_map", "ao_map", "roughness_map", "metallic_map"
            ]

            arm_map = None
            for texture_map in texture_maps:
                texture_map_list = getattr(assimp_material, texture_map)
                if texture_map_list:
                    image_path = self.__dir_name + "/" + texture_map_list[0]
                    
                    if texture_map == "roughness_map" and image_path == arm_map:
                        material.arm_map = image_path
                        material.ao_map = None
                        break

                    if texture_map == "metallic_map" and image_path == arm_map:
                        material.arm_map = image_path
                        material.ao_map = None
                        material.roughness_map = None
                        break

                    if texture_map in ["ao_map", "roughness_map", "metallic_map"]:
                        arm_map = image_path

                    if os.path.isfile(image_path):
                        setattr(material, texture_map, sampler2D.load(image_path))

            self.__materials.append(material)

        len_materials = len(self.__materials)
        for assimp_mesh in assimp_model.meshes:
            mesh = ModelMesh(assimp_mesh=assimp_mesh, block=self.__block, shared=(not self.__dynamic))
            material_index = assimp_mesh.material_index
            if 0 <= material_index < len_materials:
                mesh.material = self.__materials[material_index]

                assimp_material = assimp_model.materials[material_index]
                if assimp_material.wireframe:
                    mesh.render_hint.polygon_mode = GL.GL_LINE
                if assimp_material.twoside:
                    mesh.render_hint.cull_face = None
            
            self.__meshes.append(mesh)

        self.__load_node(assimp_model.nodes[0], assimp_model, self["root"])
        if not self.__dynamic:
            Model.__model_map[self.__file_name] = self["root"]
    
    def __load_node(self, assimp_node, assimp_model, parent_node=None):
        node = parent_node
        if node is None:
            node = SceneNode(name=assimp_node.name)

        for mesh_index in assimp_node.meshes:
            node.add_child(self.__meshes[mesh_index])
        for node_index in assimp_node.children:
            assimp_child = assimp_model.nodes[node_index]
            if not assimp_child.meshes and not assimp_child.children:
                continue
            node.add_child(self.__load_node(assimp_model.nodes[node_index], assimp_model))
        return node
