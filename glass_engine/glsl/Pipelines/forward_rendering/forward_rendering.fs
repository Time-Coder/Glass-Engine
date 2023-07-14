#version 460 core

#extension GL_ARB_bindless_texture : require

in GeometryOut
{
    vec3 view_pos;
    mat3 view_TBN;
    vec3 tex_coord;
    vec4 color;
    vec4 back_color;
    flat bool visible;
} fs_in;

in flat int env_map_index;

in PreShadingColors
{
    vec3 Gouraud_color;
    vec3 Gouraud_back_color;
    flat vec3 Flat_color;
    flat vec3 Flat_back_color;
} pre_shading_colors;

layout(location=0) out vec4 out_color;
layout(location=1) out vec4 accum;
layout(location=2) out float reveal;

#include "../../include/Material.glsl"
#include "../../Lights/Lights.glsl"
#include "../../include/fragment_utils.glsl"
#include "../../include/env_mapping.glsl"
#include "../../include/math.glsl"
#include "../../include/OIT.glsl"

buffer BindlessSampler2Ds
{
    int n_bindless_sampler2Ds;
    sampler2D bindless_sampler2Ds[];
};

uniform Material material;
uniform Material back_material;
uniform sampler2D SSAO_map;
uniform Camera camera;
uniform bool is_opaque_pass;
uniform bool is_filled;
uniform bool is_sphere;

// 环境映射
uniform bool use_skybox_map;
uniform bool use_skydome_map;
uniform samplerCube skybox_map;
uniform sampler2D skydome_map;

#include "../draw_filled.glsl"
#include "../draw_none_filled.glsl"

void main()
{
    if (!fs_in.visible)
    {
        discard;
    }    

    if (is_filled)
    {
        out_color = draw_filled(camera);
    }
    else
    {
        out_color = draw_none_filled();
    }

    // OIT
    if (!is_opaque_pass && out_color.a < 1)
    {
        get_OIT_info(out_color, accum, reveal);
        out_color = vec4(0, 0, 0, 0);
    }
}