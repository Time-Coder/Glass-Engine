#version 460 core

#extension GL_ARB_bindless_texture : require
#extension GL_EXT_texture_array : require

in VertexOut
{
    mat4 affine_transform;
    vec3 view_pos;
    vec3 view_normal;
    vec3 tex_coord;
    vec4 color;
    flat bool visible;
} fs_in;

layout(location=3) out vec3 view_pos;
layout(location=4) out vec3 view_normal;

#include "../../include/Material.glsl"

uniform Material material;
uniform Camera camera;

void main()
{
    if (!fs_in.visible)
    {
        discard;
    }

    // 实际使用的材质
    InternalMaterial internal_material = fetch_internal_material(
        fs_in.color,
        material,
        fs_in.tex_coord.st
    );
    if (internal_material.opacity < 1E-6)
    {
        discard;
    }
    view_pos = fs_in.view_pos;
    view_normal = fs_in.view_normal;
}