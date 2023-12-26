#version 430 core

#if USE_BINDLESS_TEXTURE
#extension GL_ARB_bindless_texture : require
#endif
#extension GL_EXT_texture_array : require

in GeometryOut
{
    mat4 affine_transform;
    vec3 view_pos;
    mat3 view_TBN;
    vec3 tex_coord;
    vec4 color;
    vec4 back_color;
    flat int visible;
} fs_in;

layout(location=3) out vec3 view_pos;
layout(location=4) out vec3 view_normal;

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
    mat3 view_TBN = fs_in.view_TBN;
    view_pos = fs_in.view_pos;
    InternalMaterial internal_material;

    if (gl_FrontFacing)
    {
        change_geometry(material, tex_coord, view_TBN, view_pos);
        if (hasnan(view_TBN[2]) || length(view_TBN[2]) < 1E-6)
        {
            discard;
        }

        internal_material = fetch_internal_material(fs_in.color, material, tex_coord);
    }
    else
    {
        change_geometry(back_material, tex_coord, view_TBN, view_pos);
        if (hasnan(view_TBN[2]) || length(view_TBN[2]) < 1E-6)
        {
            discard;
        }

        internal_material = fetch_internal_material(fs_in.back_color, back_material, tex_coord);
    }

    if (internal_material.opacity < 1E-6)
    {
        discard;
    }

    view_normal = view_TBN[2];
}