#version 460 core

#extension GL_ARB_bindless_texture : require
#extension GL_EXT_texture_array : require

in TexCoord
{
    vec2 tex_coord;
} fs_in;

out vec4 out_color;

#include "../../include/shading_all.glsl"
#include "read_from_gbuffer.glsl"

uniform sampler2D view_pos_and_alpha_map;
uniform sampler2D view_normal_and_emission_r_map;
uniform sampler2D ambient_and_emission_g_map;
uniform sampler2D diffuse_or_base_color_and_emission_b_map;
uniform sampler2D specular_or_preshading_and_shininess_map;
uniform sampler2D reflection_map;
uniform sampler2D env_center_and_mixed_value_map;
uniform usampler2D mixed_uint_map;

uniform Camera camera;
uniform bool use_skybox_map;
uniform bool use_skydome_map;
uniform sampler2D SSAO_map;
uniform sampler2D skydome_map;
uniform samplerCube skybox_map;
uniform Fog fog;

void main()
{
    PostShadingInfo shading_info = read_from_gbuffer(
        camera,
        view_pos_and_alpha_map,
        view_normal_and_emission_r_map,
        ambient_and_emission_g_map,
        diffuse_or_base_color_and_emission_b_map,
        specular_or_preshading_and_shininess_map,
        reflection_map,
        env_center_and_mixed_value_map,
        mixed_uint_map,
        fs_in.tex_coord
    );

    shading_info.use_skybox_map = use_skybox_map;
    shading_info.skybox_map = skybox_map;
    shading_info.use_skydome_map = use_skydome_map;
    shading_info.skydome_map = skydome_map;
    shading_info.SSAO_map = SSAO_map;
    shading_info.fog = fog;
    out_color = post_shading_all(camera, camera, shading_info);
}