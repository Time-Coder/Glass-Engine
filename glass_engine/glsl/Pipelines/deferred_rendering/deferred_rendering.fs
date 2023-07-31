#version 460 core

#extension GL_ARB_bindless_texture : require
#extension GL_EXT_texture_array : require

in TexCoord
{
    vec2 tex_coord;
} fs_in;

out vec4 out_color;

#include "../../include/Material.glsl"
#include "../../Lights/Lights.glsl"
#include "../../include/fragment_utils.glsl"
#include "../../include/math.glsl"
#include "../../include/env_mapping.glsl"

uniform sampler2D view_pos_and_alpha_map;
uniform sampler2D view_normal_and_emission_r_map;
uniform sampler2D ambient_or_arm_and_emission_g_map;
uniform sampler2D diffuse_or_albedo_and_emission_b_map;
uniform sampler2D specular_or_prelight_and_shininess_map;
uniform sampler2D reflection_map;
uniform sampler2D refraction_map;
uniform usampler2D mix_uint_map;
uniform sampler2D SSAO_map;
uniform sampler2D skydome_map;
uniform samplerCube skybox_map;

uniform Camera camera;
uniform bool use_skybox_map;
uniform bool use_skydome_map;

#include "../draw_filled_with_gbuffer.glsl"

void main()
{
    vec4 view_pos_and_alpha = texture(view_pos_and_alpha_map, fs_in.tex_coord);
    vec4 view_normal_and_emission_r = texture(view_normal_and_emission_r_map, fs_in.tex_coord);
    vec4 ambient_or_arm_and_emission_g = texture(ambient_or_arm_and_emission_g_map, fs_in.tex_coord);
    vec4 diffuse_or_albedo_and_emission_b = texture(diffuse_or_albedo_and_emission_b_map, fs_in.tex_coord);
    vec4 specular_or_prelight_and_shininess = texture(specular_or_prelight_and_shininess_map, fs_in.tex_coord);
    uvec4 mix_uint = texture(mix_uint_map, fs_in.tex_coord);
    vec4 reflection = texture(reflection_map, fs_in.tex_coord);
    vec4 refraction = texture(refraction_map, fs_in.tex_coord);
    float SSAO_factor = texture(SSAO_map, fs_in.tex_coord).r;

    out_color = draw_filled_with_gbuffer(
        camera,
        view_pos_and_alpha,
        view_normal_and_emission_r,
        ambient_or_arm_and_emission_g,
        diffuse_or_albedo_and_emission_b,
        specular_or_prelight_and_shininess,
        reflection, refraction, SSAO_factor,
        mix_uint
    );
}