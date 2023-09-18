from .SceneNode import SceneNode
from .Mesh import Mesh
from .Material import Material

from glass.utils import checktype
from glass.AttrList import AttrList
from glass import Vertices, sampler2D, Indices, GLInfo
from glass.ImageLoader import ImageLoader

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/AssimpModelLoader")
import AssimpModelLoader
import glm
from OpenGL import GL
from enum import Flag

class AssimpImportError(Exception):
    pass

class ModelMesh(Mesh):

    @checktype
    def __init__(self, assimp_mesh:AssimpModelLoader.Mesh, shared:bool=False):
        Mesh.__init__(self, name=assimp_mesh.name, shared=shared, primitive_type=GLInfo.enum_map[assimp_mesh.primitive_type])
        self.__assimp_mesh = assimp_mesh
        self.start_building()

    def build(self):
        assimp_mesh = self.__assimp_mesh

        self.x_min = assimp_mesh.x_min
        self.x_max = assimp_mesh.x_max
        self.y_min = assimp_mesh.y_min
        self.y_max = assimp_mesh.y_max
        self.z_min = assimp_mesh.z_min
        self.z_max = assimp_mesh.z_max

        self.should_add_color = False
        self.vertices = Vertices(
            position=AttrList.frombuffer(assimp_mesh.position_buffer, glm.vec3),
            tangent=AttrList.frombuffer(assimp_mesh.tangent_buffer, glm.vec3),
            bitangent=AttrList.frombuffer(assimp_mesh.bitangent_buffer, glm.vec3),
            normal=AttrList.frombuffer(assimp_mesh.normal_buffer, glm.vec3),
            tex_coord=AttrList.frombuffer(assimp_mesh.tex_coord_buffers[0], glm.vec3),
            color=AttrList.frombuffer(assimp_mesh.color_buffers[0], glm.vec4),
            back_color=AttrList.frombuffer(assimp_mesh.color_buffers[1], glm.vec4)
        )
        self.indices = Indices.frombuffer(assimp_mesh.indices_buffer, glm.uvec3)

class Model(SceneNode):

    class PostProcessSteps(Flag):
        Nothing = 0x0
        CalcTangentSpace = 0x1
        JoinIdenticalVertices = 0x2
        MakeLeftHanded = 0x4
        Triangulate = 0x8
        RemoveComponent = 0x10
        GenNormals = 0x20
        GenSmoothNormals = 0x40
        SplitLargeMeshes = 0x80
        PreTransformVertices = 0x100
        LimitBoneWeights = 0x200
        ValidateDataStructure = 0x400
        ImproveCacheLocality = 0x800
        RemoveRedundantMaterials = 0x1000
        FixInfacingNormals = 0x2000
        PopulateArmatureData = 0x4000
        SortByPType = 0x8000
        FindDegenerates = 0x10000
        FindInvalidData = 0x20000
        GenUVCoords = 0x40000
        TransformUVCoords = 0x80000
        FindInstances = 0x100000
        OptimizeMeshes  = 0x200000
        OptimizeGraph  = 0x400000
        FlipUVs = 0x800000
        FlipWindingOrder  = 0x1000000
        SplitByBoneCount  = 0x2000000
        Debone  = 0x4000000
        GlobalScale = 0x8000000
        EmbedTextures  = 0x10000000
        ForceGenNormals = 0x20000000
        DropNormals = 0x40000000
        GenBoundingBoxes = 0x80000000

    __model_map = {}

    @checktype
    def __init__(self, file_name:str="", flags:PostProcessSteps=(PostProcessSteps.SortByPType | PostProcessSteps.ValidateDataStructure | PostProcessSteps.SplitLargeMeshes | PostProcessSteps.JoinIdenticalVertices | PostProcessSteps.Triangulate | PostProcessSteps.CalcTangentSpace | PostProcessSteps.GenNormals | PostProcessSteps.GenBoundingBoxes), extra_flags:PostProcessSteps=PostProcessSteps.Nothing, exclude_flags:PostProcessSteps=PostProcessSteps.Nothing, shared:bool=True):
        self.__shared = shared
        self.__flags = ((flags | extra_flags) & (~exclude_flags))

        if file_name:
            name = os.path.basename(file_name)
            SceneNode.__init__(self, name)
            self.load(file_name, flags=self.__flags, shared=shared)
        else:
            SceneNode.__init__(self, "")
    
    @property
    def flags(self):
        return self.__flags

    @property
    def shared(self):
        return self.__shared

    @checktype
    def load(self, file_name:str, flags:PostProcessSteps=(PostProcessSteps.SplitLargeMeshes | PostProcessSteps.JoinIdenticalVertices | PostProcessSteps.Triangulate | PostProcessSteps.CalcTangentSpace | PostProcessSteps.GenNormals | PostProcessSteps.GenBoundingBoxes), extra_flags:PostProcessSteps=PostProcessSteps.Nothing, exclude_flags:PostProcessSteps=PostProcessSteps.Nothing, shared=False):
        if not os.path.isfile(file_name):
            raise FileNotFoundError(file_name)
        
        self.__shared = shared
        self.__flags = ((flags | extra_flags) & (~exclude_flags))
        self.__file_name = os.path.abspath(file_name)
        self.__dir_name = os.path.dirname(file_name)

        self["root"].clear_children()
        if self.__shared and (self.__file_name, self.__flags) in Model.__model_map:
            loaded_model_root = Model.__model_map[self.__file_name, self.__flags]
            for child in loaded_model_root.children.values():
                self["root"].add_child(child)
            return

        self.__materials = []
        self.__meshes = []

        assimp_model = AssimpModelLoader.load(self.__file_name, flags.value)

        if not assimp_model.success:
            raise AssimpImportError(assimp_model.error_message)
        if not assimp_model.nodes or \
           (not assimp_model.nodes[0].children and not assimp_model.nodes[0].meshes):
            return

        for assimp_material in assimp_model.materials:
            material = Material(name=assimp_material.name)

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
                        image = ImageLoader.load(image_path)
                        if len(image.shape) > 2 and image.shape[2] >= 3:
                            material.arm_map = sampler2D.load(image_path)
                            material.ao_map = None
                            break

                    if texture_map == "metallic_map" and image_path == arm_map:
                        image = ImageLoader.load(image_path)
                        if len(image.shape) > 2 and image.shape[2] >= 3:
                            material.arm_map = sampler2D.load(image_path)
                            material.ao_map = None
                            material.roughness_map = None
                            break

                    if texture_map in ["ao_map", "roughness_map", "metallic_map"]:
                        arm_map = image_path

                    if os.path.isfile(image_path):
                        if texture_map == "ambient_map":
                            image = ImageLoader.load(image_path)
                            image_dtype = image.dtype
                            threshold = 0.5
                            if "int" in str(image_dtype):
                                threshold = 127

                            if image.max() > threshold:
                                image = (0.2*image).astype(image_dtype)

                            material.ambient_map = sampler2D(image)
                        else:
                            setattr(material, texture_map, sampler2D.load(image_path))

            self.__materials.append(material)

        len_materials = len(self.__materials)
        for assimp_mesh in assimp_model.meshes:
            mesh = ModelMesh(assimp_mesh=assimp_mesh, shared=self.__shared)
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
        if self.__shared:
            Model.__model_map[self.__file_name, self.__flags] = self["root"]
    
    def __load_node(self, assimp_node, assimp_model, parent_node=None):
        node = parent_node
        if node is None:
            node = SceneNode(name=assimp_node.name)

        node.orientation.w = assimp_node.orientation.w
        node.orientation.x = assimp_node.orientation.x
        node.orientation.y = assimp_node.orientation.y
        node.orientation.z = assimp_node.orientation.z

        node.position.x = assimp_node.position.x
        node.position.y = assimp_node.position.y
        node.position.z = assimp_node.position.z

        node.scale.x = assimp_node.scale.x
        node.scale.y = assimp_node.scale.y
        node.scale.z = assimp_node.scale.z

        for mesh_index in assimp_node.meshes:
            node.add_child(self.__meshes[mesh_index])
        for node_index in assimp_node.children:
            assimp_child = assimp_model.nodes[node_index]
            if not assimp_child.meshes and not assimp_child.children:
                continue
            node.add_child(self.__load_node(assimp_model.nodes[node_index], assimp_model))
        return node
