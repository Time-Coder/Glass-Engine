#version 460 core

#extension GL_ARB_bindless_texture : require
#extension GL_EXT_texture_array : require

in GeometryOut
{
    mat4 affine_transform;
    vec3 view_pos;
    mat3 view_TBN;
    vec3 tex_coord;
    vec4 color;
    vec4 back_color;
    flat bool visible;
} fs_in;

layout(location=3) out vec3 view_pos;
layout(location=4) out vec3 view_normal;

#include "../../include/Material.glsl"
#include "../../include/shading_all.glsl"

uniform Material material;
uniform Material back_material;
uniform Camera camera;

void main()
{
    if (!fs_in.visible)
    {
        discard;
    }

    Material current_material = (gl_FrontFacing ? material : back_material);

    // 高度贴图和法线贴图改变几何信息
    vec2 tex_coord = fs_in.tex_coord.st;
    mat3 view_TBN = fs_in.view_TBN;
    view_pos = fs_in.view_pos;
    change_geometry(current_material, tex_coord, view_TBN, view_pos);
    if (hasnan(view_TBN[2]) || length(view_TBN[2]) < 1E-6)
    {
        discard;
    }

    // 实际使用的材质
    InternalMaterial internal_material = fetch_internal_material(
        (gl_FrontFacing ? fs_in.color : fs_in.back_color),
        (gl_FrontFacing ? material : back_material),
        tex_coord
    );

    // 透明度过低丢弃
    if (internal_material.opacity < 1E-6)
    {
        discard;
    }

    view_normal = view_TBN[2];
}