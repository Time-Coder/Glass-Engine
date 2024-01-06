#include "assimpy.h"

#include <assimp/Importer.hpp>
#include <assimp/scene.h>
#include <assimp/postprocess.h>

#include <sstream>
#include <iomanip>

Texture::Texture(aiTexel* pcData, unsigned _width, unsigned _height):
    width(_width), height(_height)
{
    unsigned length = width;
    if (height > 0)
    {
        length *= (height * 4);
    }
    content = pybind11::bytes((const char*)(pcData), length);
    key = std::to_string((unsigned long long)(pcData));
}

Model Model::load(const std::string& file_name, unsigned flags)
{
    Model model;

    Assimp::Importer importer;
    const aiScene* scene = importer.ReadFile(file_name, flags);
    if (scene == nullptr || (scene->mFlags & AI_SCENE_FLAGS_INCOMPLETE) || scene->mRootNode == nullptr)
    {
        model.success = false;
        model.error_message = importer.GetErrorString();
        return model;
    }

    model.name = std::string(scene->mName.C_Str());
    model.load_materials(scene);
    model.load_meshes(scene);
    model.load_node(scene->mRootNode, scene, -1);
    model.success = true;

    return model;
}

void Model::load_texture(
    const aiScene* assimp_scene, aiMaterial* assimp_material, aiTextureType texture_type,
    std::vector<Texture>& textures)
{
    unsigned texture_count = assimp_material->GetTextureCount(texture_type);
    for (unsigned j = 0; j < texture_count; j++)
    {
        aiString file_name;
        assimp_material->GetTexture(texture_type, j, &file_name);
        if (file_name.length > 1 && file_name.data[0] == '*')
        {
            int texture_index = std::stoi(std::string(file_name.data + 1));
            aiTexture* assimp_texture = assimp_scene->mTextures[texture_index];
            textures.push_back(Texture(assimp_texture->pcData, assimp_texture->mWidth, assimp_texture->mHeight));
        }
        else
        {
            textures.push_back(Texture(file_name.C_Str()));
        }
    }
}

void Model::load_materials(const aiScene* assimp_scene)
{
    for (unsigned i = 0; i < assimp_scene->mNumMaterials; i++)
    {
        aiMaterial* assimp_material = assimp_scene->mMaterials[i];
        Material material;

        material.name = assimp_material->GetName().C_Str();
        assimp_material->Get(AI_MATKEY_COLOR_AMBIENT, material.ambient);
        assimp_material->Get(AI_MATKEY_COLOR_DIFFUSE, material.diffuse);
        assimp_material->Get(AI_MATKEY_COLOR_SPECULAR, material.specular);
        assimp_material->Get(AI_MATKEY_COLOR_EMISSIVE, material.emission);

        aiColor3D reflection;
        aiReturn success = assimp_material->Get(AI_MATKEY_COLOR_REFLECTIVE, reflection);
        if (success == aiReturn_SUCCESS)
        {
            material.reflection.r = reflection.r;
            material.reflection.g = reflection.g;
            material.reflection.b = reflection.b;
        }

        float reflectivity = 0;
        success = assimp_material->Get(AI_MATKEY_REFLECTIVITY, reflectivity);
        if (success == aiReturn_SUCCESS)
        {
            material.reflection.a = reflectivity;
        }

        assimp_material->Get(AI_MATKEY_COLOR_TRANSPARENT, material.transparent);

        int wireframe = 0;
        assimp_material->Get(AI_MATKEY_ENABLE_WIREFRAME, wireframe);
        material.wireframe = wireframe;

        int twoside = 0;
        assimp_material->Get(AI_MATKEY_TWOSIDED, twoside);
        material.twoside = twoside;

        int shading_mode = aiShadingMode_Blinn;
        assimp_material->Get(AI_MATKEY_SHADING_MODEL, shading_mode);
        material.shading_model = (aiShadingMode)shading_mode;

        assimp_material->Get(AI_MATKEY_SHININESS, material.shininess);
        assimp_material->Get(AI_MATKEY_SHININESS_STRENGTH, material.shininess_strength);
        assimp_material->Get(AI_MATKEY_OPACITY, material.opacity);
        assimp_material->Get(AI_MATKEY_REFRACTI, material.refractive_index);

        assimp_material->Get(AI_MATKEY_BASE_COLOR, material.base_color);
        assimp_material->Get(AI_MATKEY_ROUGHNESS_FACTOR, material.roughness);
        assimp_material->Get(AI_MATKEY_METALLIC_FACTOR, material.metallic);

        load_texture(assimp_scene, assimp_material, aiTextureType_DIFFUSE, material.diffuse_map);
        load_texture(assimp_scene, assimp_material, aiTextureType_SPECULAR, material.specular_map);
        load_texture(assimp_scene, assimp_material, aiTextureType_AMBIENT, material.ambient_map);
        load_texture(assimp_scene, assimp_material, aiTextureType_EMISSIVE, material.emission_map);
        load_texture(assimp_scene, assimp_material, aiTextureType_HEIGHT, material.height_map);
        load_texture(assimp_scene, assimp_material, aiTextureType_NORMALS, material.normal_map);
        load_texture(assimp_scene, assimp_material, aiTextureType_SHININESS, material.shininess_map);
        load_texture(assimp_scene, assimp_material, aiTextureType_OPACITY, material.opacity_map);
        load_texture(assimp_scene, assimp_material, aiTextureType_DISPLACEMENT, material.displacement_map);
        load_texture(assimp_scene, assimp_material, aiTextureType_LIGHTMAP, material.lightmap_map);
        load_texture(assimp_scene, assimp_material, aiTextureType_REFLECTION, material.reflection_map);
        load_texture(assimp_scene, assimp_material, aiTextureType_BASE_COLOR, material.base_color_map);
        load_texture(assimp_scene, assimp_material, aiTextureType_NORMAL_CAMERA, material.normal_camera_map);
        load_texture(assimp_scene, assimp_material, aiTextureType_EMISSION_COLOR, material.emission_color_map);
        load_texture(assimp_scene, assimp_material, aiTextureType_METALNESS, material.metallic_map);
        load_texture(assimp_scene, assimp_material, aiTextureType_DIFFUSE_ROUGHNESS, material.roughness_map);
        load_texture(assimp_scene, assimp_material, aiTextureType_AMBIENT_OCCLUSION, material.ao_map);
        load_texture(assimp_scene, assimp_material, aiTextureType_SHEEN, material.sheen_map);
        load_texture(assimp_scene, assimp_material, aiTextureType_CLEARCOAT, material.clearcoat_map);
        load_texture(assimp_scene, assimp_material, aiTextureType_TRANSMISSION, material.transmission_map);
        load_texture(assimp_scene, assimp_material, aiTextureType_UNKNOWN, material.unknown_map);

        materials.push_back(material);
    }
}

void Model::load_meshes(const aiScene* assimp_scene)
{
    for (unsigned i = 0; i < assimp_scene->mNumMeshes; i++)
    {
        aiMesh* assimp_mesh = assimp_scene->mMeshes[i];

        Mesh mesh;
        mesh.name = assimp_mesh->mName.C_Str();
        switch (assimp_mesh->mPrimitiveTypes)
        {
        case aiPrimitiveType_POINT: mesh.primitive_type = 0; break;
        case aiPrimitiveType_LINE: mesh.primitive_type = 1; break;
        case aiPrimitiveType_TRIANGLE:
        default: mesh.primitive_type = 4;
        }
        mesh.x_min = assimp_mesh->mAABB.mMin.x;
        mesh.y_min = assimp_mesh->mAABB.mMin.y;
        mesh.z_min = assimp_mesh->mAABB.mMin.z;
        mesh.x_max = assimp_mesh->mAABB.mMax.x;
        mesh.y_max = assimp_mesh->mAABB.mMax.y;
        mesh.z_max = assimp_mesh->mAABB.mMax.z;

        // vertices buffers
        unsigned n_vertices = assimp_mesh->mNumVertices;
        if (assimp_mesh->HasPositions())
        {
            mesh.position_buffer = pybind11::bytes((const char*)(assimp_mesh->mVertices), n_vertices*sizeof(aiVector3D));
        }
        else
        {
            mesh.position_buffer_ptr = std::shared_ptr<aiVector3D>(new aiVector3D[n_vertices], [](aiVector3D* p) { delete[] p; });
            mesh.position_buffer = pybind11::bytes((const char*)(mesh.position_buffer_ptr.get()), n_vertices * sizeof(aiVector3D));
        }

        if (assimp_mesh->HasTangentsAndBitangents())
        {
            mesh.tangent_buffer = pybind11::bytes((const char*)(assimp_mesh->mTangents), n_vertices*sizeof(aiVector3D));
            mesh.bitangent_buffer = pybind11::bytes((const char*)(assimp_mesh->mBitangents), n_vertices*sizeof(aiVector3D));
        }
        else
        {
            mesh.tangent_buffer_ptr = std::shared_ptr<aiVector3D>(new aiVector3D[n_vertices], [](aiVector3D* p) { delete[] p; });
            mesh.bitangent_buffer_ptr = std::shared_ptr<aiVector3D>(new aiVector3D[n_vertices], [](aiVector3D* p) { delete[] p; });

            mesh.tangent_buffer = pybind11::bytes((const char*)(mesh.tangent_buffer_ptr.get()), n_vertices * sizeof(aiVector3D));
            mesh.bitangent_buffer = pybind11::bytes((const char*)(mesh.bitangent_buffer_ptr.get()), n_vertices * sizeof(aiVector3D));
        }

        if (assimp_mesh->HasNormals())
        {
            mesh.normal_buffer = pybind11::bytes((const char*)(assimp_mesh->mNormals), n_vertices*sizeof(aiVector3D));
        }
        else
        {
            mesh.normal_buffer_ptr = std::shared_ptr<aiVector3D>(new aiVector3D[n_vertices], [](aiVector3D* p) { delete[] p; });
            mesh.normal_buffer = pybind11::bytes((const char*)(mesh.normal_buffer_ptr.get()), n_vertices * sizeof(aiVector3D));
        }

        for (int i = 0; i < 8; i++)
        {
            if (assimp_mesh->HasVertexColors(i))
            {
                mesh.color_buffers[i] = pybind11::bytes((const char*)(assimp_mesh->mColors[i]), n_vertices*sizeof(aiColor4D));
            }
            else
            {
                mesh.color_buffer_ptr[i] = std::shared_ptr<aiColor4D>(new aiColor4D[n_vertices], [](aiColor4D* p) { delete[] p; });
                mesh.color_buffers[i] = pybind11::bytes((const char*)(mesh.color_buffer_ptr[i].get()), n_vertices * sizeof(aiColor4D));
            }

            if (assimp_mesh->HasTextureCoords(i))
            {
                mesh.tex_coord_buffers[i] = pybind11::bytes((const char*)(assimp_mesh->mTextureCoords[i]), n_vertices*sizeof(aiVector3D));
            }
            else
            {
                mesh.tex_coord_buffer_ptr[i] = std::shared_ptr<aiVector3D>(new aiVector3D[n_vertices], [](aiVector3D* p) { delete[] p; });
                mesh.tex_coord_buffers[i] = pybind11::bytes((const char*)(mesh.tex_coord_buffer_ptr[i].get()), n_vertices * sizeof(aiVector3D));
            }
        }

        if (!(assimp_mesh->HasVertexColors(1)))
        {
            mesh.color_buffers[1] = mesh.color_buffers[0];
        }

        // indices buffers
        if (assimp_mesh->mNumFaces == 0)
        {

        }
        else if (assimp_mesh->mNumFaces == 1)
        {
            aiFace assimp_face = assimp_mesh->mFaces[0];
            mesh.indices_buffer = pybind11::bytes((const char*)(assimp_face.mIndices), assimp_face.mNumIndices * sizeof(unsigned));
        }
        else
        {
            unsigned len_indices = 0;
            for (unsigned j = 0; j < assimp_mesh->mNumFaces; j++)
            {
                len_indices += assimp_mesh->mFaces[j].mNumIndices;
            }

            mesh.indices_buffer_ptr = std::shared_ptr<unsigned>(new unsigned[len_indices], [](unsigned* p) { delete[] p; });
            unsigned offset = 0;
            for (unsigned j = 0; j < assimp_mesh->mNumFaces; j++)
            {
                aiFace assimp_face = assimp_mesh->mFaces[j];
                memcpy(mesh.indices_buffer_ptr.get() + offset, assimp_face.mIndices, assimp_face.mNumIndices * sizeof(unsigned));
                offset += assimp_face.mNumIndices;
            }
            mesh.indices_buffer = pybind11::bytes((const char*)(mesh.indices_buffer_ptr.get()), len_indices * sizeof(unsigned));
        }

        mesh.material_index = assimp_mesh->mMaterialIndex;
        meshes.push_back(mesh);
    }
}

size_t Model::load_node(aiNode* assimp_node, const aiScene* scene, size_t parent)
{
    Node node;
    size_t self_index = nodes.size();
    node.parent = parent;
    node.name = std::string(assimp_node->mName.C_Str());
    assimp_node->mTransformation.Decompose(node.scale, node.orientation, node.position);
    for (unsigned i = 0; i < assimp_node->mNumMeshes; i++)
    {
        node.meshes.push_back(assimp_node->mMeshes[i]);
    }
    nodes.push_back(node);

    for (unsigned i = 0; i < assimp_node->mNumChildren; i++)
    {
        size_t child_index = load_node(assimp_node->mChildren[i], scene, self_index);
        nodes[self_index].children.push_back(child_index);
    }
    return self_index;
}
