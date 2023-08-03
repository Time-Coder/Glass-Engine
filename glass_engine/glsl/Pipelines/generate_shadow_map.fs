#version 460 core

#extension GL_ARB_bindless_texture : require
#extension GL_EXT_texture_array : require

in GeometryOut
{
    vec3 view_pos;
    mat3 view_TBN;
    vec3 tex_coord;
    vec4 color;
    vec4 back_color;
    flat bool visible;
} fs_in;

layout(location=0) out vec2 shadow_and_dev;

#include "../include/Material.glsl"
#include "../Lights/Lights.glsl"
#include "../include/fragment_utils.glsl"
#include "../include/math.glsl"

uniform Camera camera;
uniform Material material;
uniform Material back_material;

#define CURRENT_MATERIAL (gl_FrontFacing ? material : back_material)
#define CURRENT_COLOR (gl_FrontFacing ? fs_in.color : fs_in.back_color)

void main()
{
    if (!fs_in.visible)
    {
        discard;
    }    

    mat3 view_TBN = fs_in.view_TBN;
    vec3 view_normal = normalize(view_TBN[2]);
    if (!gl_FrontFacing)
    {
        view_normal = -view_normal;
    }
    view_TBN[2] = view_normal;
    if (hasnan(view_TBN))
    {
        shadow_and_dev = vec2(0, 0);
        return;
    }

    vec3 view_pos = fs_in.view_pos;
    vec2 frag_tex_coord = fs_in.tex_coord.st;

    // 高度贴图和法线贴图改变几何信息
    change_geometry(
        CURRENT_MATERIAL,
        view_pos, view_normal,
        frag_tex_coord, view_TBN
    );

    // 实际使用的材质
    InternalMaterial internal_material = fetch_internal_material(
        CURRENT_COLOR, CURRENT_MATERIAL, frag_tex_coord
    );

    // 透明度过低丢弃
    if (internal_material.shading_model != 9 && internal_material.opacity < 1E-6)
    {
        discard;
    }

    vec3 frag_pos = view_to_world(camera, view_pos);
    vec3 frag_normal = view_dir_to_world(camera, view_normal);
    uint shading_model = internal_material.shading_model;

    if (shading_model == 9) // Unlit
    {
        shadow_and_dev = vec2(0, 0);
        return;
    }

    float visibility = 1;
    float dev = 0;
    for (int i = 0; i < n_dir_lights; i++)
    {
        if (internal_material.shading_model == 9 ||
            !dir_lights[i].generate_shadows ||
            dir_lights[i].depth_map_handle == 0 ||
            !internal_material.recv_shadows)
        {
            continue;
        }

        vec2 visibility_dev = PCF(dir_lights[i], camera, frag_pos, frag_normal);

        visibility *= visibility_dev.x;
        dev += visibility_dev.y;
    }

    for (int i = 0; i < n_point_lights; i++)
    {
        if (internal_material.shading_model == 9 ||
            !point_lights[i].generate_shadows ||
            point_lights[i].depth_map_handle == 0 ||
            !internal_material.recv_shadows)
        {
            continue;
        }

        vec2 visibility_dev = PCF(point_lights[i], frag_pos, frag_normal);

        visibility *= visibility_dev.x;
        dev += visibility_dev.y;
    }

    dev /= (n_dir_lights + n_point_lights);

    shadow_and_dev = vec2(1 - visibility, dev);
}