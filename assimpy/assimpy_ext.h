#pragma once

#include <vector>
#include <string>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <assimp/material.h>
#include <assimp/postprocess.h>

struct aiTexel;
class Texture
{
public:
	Texture(const std::string& _file_name): key(_file_name), file_name(_file_name) {}
	Texture(aiTexel* pcData, unsigned _width, unsigned _height);

public:
	std::string key;
	std::string file_name;
	pybind11::bytes content;
	unsigned width = 0;
	unsigned height = 0;
};

class Material
{
public:
	std::string name;

	aiColor3D ambient;
	aiColor3D diffuse;
	aiColor3D specular;
	aiColor3D emission;
	aiColor4D reflection;
	aiColor3D transparent;
	aiColor3D base_color;
	float roughness;
	float metallic;
	float refractive_index = 0;
	bool wireframe = false;
	bool twoside = false;
	aiShadingMode shading_model = aiShadingMode_Blinn;
	aiBlendMode blend_func = aiBlendMode_Default;

	float shininess = 0;
	float shininess_strength = 1;
	float opacity = 1;

	std::vector<Texture> diffuse_map;
	std::vector<Texture> specular_map;
    std::vector<Texture> ambient_map;
    std::vector<Texture> emission_map;
    std::vector<Texture> height_map;
    std::vector<Texture> normal_map;
    std::vector<Texture> shininess_map;
    std::vector<Texture> opacity_map;
    std::vector<Texture> displacement_map;
    std::vector<Texture> lightmap_map;
    std::vector<Texture> reflection_map;
    std::vector<Texture> base_color_map;
    std::vector<Texture> normal_camera_map;
    std::vector<Texture> emission_color_map;
    std::vector<Texture> metallic_map;
    std::vector<Texture> roughness_map;
    std::vector<Texture> ao_map;
    std::vector<Texture> sheen_map;
    std::vector<Texture> clearcoat_map;
    std::vector<Texture> transmission_map;
    std::vector<Texture> unknown_map;

public:
	Material() {}
};

class Mesh
{
public:
	std::string name;

	unsigned int primitive_type = 4;
	int material_index = -1;
	float x_min = 0.0f;
	float x_max = 0.0f;
	float y_min = 0.0f;
	float y_max = 0.0f;
	float z_min = 0.0f;
	float z_max = 0.0f;

	pybind11::bytes position_buffer;
	pybind11::bytes tangent_buffer;
	pybind11::bytes bitangent_buffer;
	pybind11::bytes normal_buffer;
	std::vector<pybind11::bytes> color_buffers;
	std::vector<pybind11::bytes> tex_coord_buffers;
	pybind11::bytes indices_buffer;

public:
	std::shared_ptr<aiVector3D> position_buffer_ptr;
	std::shared_ptr<aiVector3D> tangent_buffer_ptr;
	std::shared_ptr<aiVector3D> bitangent_buffer_ptr;
	std::shared_ptr<aiVector3D> normal_buffer_ptr;
	std::shared_ptr<aiVector3D> tex_coord_buffer_ptr[8];
	std::shared_ptr<aiColor4D> color_buffer_ptr[8];
	std::shared_ptr<unsigned> indices_buffer_ptr;

public:
	Mesh() : color_buffers(8), tex_coord_buffers(8) {}
};

class Node
{
public:
	std::string name;
	aiVector3D scale;
	aiVector3D position;
	aiQuaternion orientation;

	size_t parent = -1;
	std::vector<size_t> children;
	std::vector<int> meshes;

public:
	Node() {}
};

struct aiNode;
struct aiScene;
class Model
{
public:
	bool success = false;
	std::string error_message;
	std::string name;
	std::vector<Node> nodes;
	std::vector<Mesh> meshes;
	std::vector<Material> materials;

public:
	static Model load(const std::string& file_name, unsigned flags = (aiProcess_SortByPType | aiProcess_ValidateDataStructure | aiProcess_SplitLargeMeshes | aiProcess_JoinIdenticalVertices | aiProcess_Triangulate | aiProcess_CalcTangentSpace | aiProcess_GenNormals | aiProcess_GenBoundingBoxes | aiProcess_GenUVCoords));

private:
	void load_materials(const aiScene* scene);
	void load_meshes(const aiScene* scene);
	size_t load_node(aiNode* assimp_node, const aiScene* scene, size_t parent);
	void load_texture(
		const aiScene* assimp_scene, aiMaterial* assimp_material, aiTextureType texture_type,
		std::vector<Texture>& texture_maps);
};
