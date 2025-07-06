#version 430 core

#if USE_BINDLESS_TEXTURE
#extension GL_ARB_bindless_texture : require
#endif
#extension GL_EXT_texture_array : require

in VertexOut
{
    mat4 affine_transform;
    vec3 world_pos;
    vec3 world_normal;
    vec3 tex_coord;
    vec4 color;
    flat int visible;
} fs_in;

layout(location=3) out vec3 world_pos;
layout(location=4) out vec3 world_normal;

#include "../../include/InternalMaterial.glsl"
#include "../../include/Material.glsl"
#include "../../include/Camera.glsl"

uniform Material material;
uniform Camera camera;

void main()
{
    if (fs_in.visible == 0)
    {
        discard;
    }

    InternalMaterial internal_material =
        fetch_internal_material(fs_in.color, material, fs_in.tex_coord.st);

    if (internal_material.opacity < 1E-6)
    {
        discard;
    }

    world_pos = fs_in.world_pos;
    world_normal = fs_in.world_normal;
}