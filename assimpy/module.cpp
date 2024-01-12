#include "assimpy_ext.h"

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

PYBIND11_MODULE(assimpy_ext, m)
{
    pybind11::class_<aiColor3D>(m, "aiColor3D")
        .def_readwrite("r", &aiColor3D::r)
        .def_readwrite("g", &aiColor3D::g)
        .def_readwrite("b", &aiColor3D::b);

    pybind11::class_<aiColor4D>(m, "aiColor4D")
        .def_readwrite("r", &aiColor4D::r)
        .def_readwrite("g", &aiColor4D::g)
        .def_readwrite("b", &aiColor4D::b)
        .def_readwrite("a", &aiColor4D::a);

    pybind11::class_<aiVector3D>(m, "aiVector3D")
        .def_readwrite("x", &aiVector3D::x)
        .def_readwrite("y", &aiVector3D::y)
        .def_readwrite("z", &aiVector3D::z);

    pybind11::class_<aiQuaternion>(m, "aiQuaternion")
        .def_readwrite("w", &aiQuaternion::w)
        .def_readwrite("x", &aiQuaternion::x)
        .def_readwrite("y", &aiQuaternion::y)
        .def_readwrite("z", &aiQuaternion::z);

    pybind11::enum_<aiShadingMode>(m, "aiShadingMode")
        .value("aiShadingMode_Flat", aiShadingMode_Flat)
        .value("aiShadingMode_Gouraud", aiShadingMode_Gouraud)
        .value("aiShadingMode_Phong", aiShadingMode_Phong)
        .value("aiShadingMode_Blinn", aiShadingMode_Blinn)
        .value("aiShadingMode_Toon", aiShadingMode_Toon)
        .value("aiShadingMode_OrenNayar", aiShadingMode_OrenNayar)
        .value("aiShadingMode_Minnaert", aiShadingMode_Minnaert)
        .value("aiShadingMode_CookTorrance", aiShadingMode_CookTorrance)
        .value("aiShadingMode_NoShading", aiShadingMode_NoShading)
        .value("aiShadingMode_Unlit", aiShadingMode_Unlit)
        .value("aiShadingMode_Fresnel", aiShadingMode_Fresnel)
        .value("aiShadingMode_PBR_BRDF", aiShadingMode_PBR_BRDF)
        .export_values();

    pybind11::enum_<aiBlendMode>(m, "aiBlendMode")
        .value("aiBlendMode_Default", aiBlendMode_Default)
        .value("aiBlendMode_Additive", aiBlendMode_Additive)
        .export_values();
    
    pybind11::class_<Texture>(m, "Texture")
        .def_readwrite("key", &Texture::key)
        .def_readwrite("file_name", &Texture::file_name)
        .def_readwrite("content", &Texture::content)
        .def_readwrite("width", &Texture::width)
        .def_readwrite("height", &Texture::height);

    pybind11::class_<Material>(m, "Material")
        .def_readwrite("name", &Material::name)
        .def_readwrite("ambient", &Material::ambient)
        .def_readwrite("diffuse", &Material::diffuse)
        .def_readwrite("specular", &Material::specular)
        .def_readwrite("emission", &Material::emission)
        .def_readwrite("base_color", &Material::base_color)
        .def_readwrite("reflection", &Material::reflection)
        .def_readwrite("refractive_index", &Material::refractive_index)
        .def_readwrite("transparent", &Material::transparent)
        .def_readwrite("wireframe", &Material::wireframe)
        .def_readwrite("twoside", &Material::twoside)
        .def_readwrite("shading_model", &Material::shading_model)
        .def_readwrite("blend_func", &Material::blend_func)

        .def_readwrite("roughness", &Material::roughness)
        .def_readwrite("metallic", &Material::metallic)
        .def_readwrite("shininess", &Material::shininess)
        .def_readwrite("shininess_strength", &Material::shininess_strength)
        .def_readwrite("opacity", &Material::opacity)

        .def_readwrite("diffuse_map", &Material::diffuse_map)
        .def_readwrite("specular_map", &Material::specular_map)
        .def_readwrite("ambient_map", &Material::ambient_map)
        .def_readwrite("emission_map", &Material::emission_map)
        .def_readwrite("height_map", &Material::height_map)
        .def_readwrite("normal_map", &Material::normal_map)
        .def_readwrite("shininess_map", &Material::shininess_map)
        .def_readwrite("opacity_map", &Material::opacity_map)
        .def_readwrite("displacement_map", &Material::displacement_map)
        .def_readwrite("lightmap_map", &Material::lightmap_map)
        .def_readwrite("reflection_map", &Material::reflection_map)
        .def_readwrite("base_color_map", &Material::base_color_map)
        .def_readwrite("normal_camera_map", &Material::normal_camera_map)
        .def_readwrite("emission_color_map", &Material::emission_color_map)
        .def_readwrite("metallic_map", &Material::metallic_map)
        .def_readwrite("roughness_map", &Material::roughness_map)
        .def_readwrite("ao_map", &Material::ao_map)
        .def_readwrite("sheen_map", &Material::sheen_map)
        .def_readwrite("clearcoat_map", &Material::clearcoat_map)
        .def_readwrite("transmission_map", &Material::transmission_map)
        .def_readwrite("unknown_map", &Material::unknown_map);

    pybind11::class_<Mesh>(m, "Mesh")
        .def_readwrite("name", &Mesh::name)
        .def_readwrite("primitive_type", &Mesh::primitive_type)
        .def_readwrite("x_min", &Mesh::x_min)
        .def_readwrite("x_max", &Mesh::x_max)
        .def_readwrite("y_min", &Mesh::y_min)
        .def_readwrite("y_max", &Mesh::y_max)
        .def_readwrite("z_min", &Mesh::z_min)
        .def_readwrite("z_max", &Mesh::z_max)
        .def_readwrite("material_index", &Mesh::material_index)
        .def_readwrite("position_buffer", &Mesh::position_buffer)
        .def_readwrite("tangent_buffer", &Mesh::tangent_buffer)
        .def_readwrite("bitangent_buffer", &Mesh::bitangent_buffer)
        .def_readwrite("normal_buffer", &Mesh::normal_buffer)
        .def_readwrite("color_buffers", &Mesh::color_buffers)
        .def_readwrite("tex_coord_buffers", &Mesh::tex_coord_buffers)
        .def_readwrite("indices_buffer", &Mesh::indices_buffer);

    pybind11::class_<Node>(m, "Node")
        .def_readwrite("name", &Node::name)
        .def_readwrite("orientation", &Node::orientation)
        .def_readwrite("scale", &Node::scale)
        .def_readwrite("position", &Node::position)
        .def_readwrite("parent", &Node::parent)
        .def_readwrite("children", &Node::children)
        .def_readwrite("meshes", &Node::meshes);

    pybind11::class_<Model>(m, "Model")
        .def_readwrite("name", &Model::name)
        .def_readwrite("success", &Model::success)
        .def_readwrite("error_message", &Model::error_message)
        .def_readwrite("nodes", &Model::nodes)
        .def_readwrite("meshes", &Model::meshes)
        .def_readwrite("materials", &Model::materials);

    m.def("load", &Model::load);
}