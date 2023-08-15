#version 460 core

layout(location=0) out vec4 view_pos_alpha;
layout(location=1) out vec3 view_normal;

in GeometryOut
{
    vec3 view_pos;
    mat3 view_TBN;
    vec3 tex_coord;
    vec4 color;
    vec4 back_color;
    flat bool visible;
} fs_in;

#include "../../include/Material.glsl"
#include "../../include/parallax_mapping.glsl"
#include "../../include/math.glsl"

uniform Material material;
uniform Material back_material;
uniform Camera camera;

void main()
{
    if (!fs_in.visible)
    {
        discard;
    }

    mat3 view_TBN = fs_in.view_TBN;
    view_normal = normalize(view_TBN[2]);
    if (!gl_FrontFacing)
    {
        view_normal = -view_normal;
    }
    view_TBN[2] = view_normal;
    if (hasnan(view_normal))
    {
        return;
    }

    vec3 view_pos = fs_in.view_pos;
    vec2 frag_tex_coord = fs_in.tex_coord.st;

    // 高度贴图和法线贴图改变几何信息
    change_geometry(
        (gl_FrontFacing ? material : back_material),
        view_pos, view_normal,
        frag_tex_coord, view_TBN
    );

    // 实际使用的材质
    InternalMaterial internal_material = fetch_internal_material(
        (gl_FrontFacing ? fs_in.color : fs_in.back_color),
        (gl_FrontFacing ? material : back_material),
        frag_tex_coord
    );

    if (internal_material.shading_model != 9 && internal_material.opacity < 1E-6)
    {
        discard;
    }

    view_pos_alpha = vec4(view_pos, internal_material.opacity);
}