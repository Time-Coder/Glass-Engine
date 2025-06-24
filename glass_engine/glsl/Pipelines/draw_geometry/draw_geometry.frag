#version 430 core

#if USE_BINDLESS_TEXTURE
#extension GL_ARB_bindless_texture : require
#endif
#extension GL_EXT_texture_array : require

in GeometryOut
{
    mat4 affine_transform;
    vec3 world_pos;
    mat3 world_TBN;
    vec3 tex_coord;
    vec4 color;
    vec4 back_color;
    flat int visible;
} fs_in;

layout(location=3) out vec3 world_pos;
layout(location=4) out vec3 world_normal;

#include "../../include/InternalMaterial.glsl"
#include "../../include/shading_all.glsl"

uniform Material material;
uniform Material back_material;
uniform Camera camera;

void main()
{
    if (fs_in.visible == 0)
    {
        discard;
    }

    vec2 tex_coord = fs_in.tex_coord.st;
    mat3 world_TBN = fs_in.world_TBN;
    world_pos = fs_in.world_pos;
    InternalMaterial internal_material;

    if (gl_FrontFacing)
    {
        change_geometry(camera, material, tex_coord, world_TBN, world_pos);
        if (hasnan(world_TBN[2]) || length(world_TBN[2]) < 1E-6)
        {
            discard;
        }

        internal_material = fetch_internal_material(fs_in.color, material, tex_coord);
    }
    else
    {
        change_geometry(camera, back_material, tex_coord, world_TBN, world_pos);
        if (hasnan(world_TBN[2]) || length(world_TBN[2]) < 1E-6)
        {
            discard;
        }

        internal_material = fetch_internal_material(fs_in.back_color, back_material, tex_coord);
    }

    if (internal_material.opacity < 1E-6)
    {
        discard;
    }

    world_normal = world_TBN[2];
}