#version 460 core

#extension GL_ARB_bindless_texture : enable

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

in vec3 preshading_color;
in vec3 preshading_back_color;
in flat uvec2 env_map_handle;

// 几何信息
layout(location=3) out vec4 view_pos_and_alpha;
layout(location=4) out vec4 view_normal_and_emission_r;

// 光照信息
layout(location=2) out vec4 ambient_and_emission_g;
layout(location=0) out vec4 diffuse_or_base_color_and_emission_b;
layout(location=1) out vec4 specular_or_preshading_and_shininess;
layout(location=5) out vec4 reflection;
layout(location=6) out vec4 env_center_and_mixed_value;
layout(location=7) out uvec4 mixed_uint;

#include "../../include/Material.glsl"
#include "../../include/parallax_mapping.glsl"
#include "../../include/math.glsl"
#include "../../include/transform.glsl"
#include "write_to_gbuffer.glsl"

uniform Material material;
uniform Material back_material;
uniform bool is_sphere;
uniform vec3 mesh_center;

void main()
{
    if (!fs_in.visible)
    {
        discard;
    }
    
    vec2 tex_coord = fs_in.tex_coord.st;
    mat3 view_TBN = fs_in.view_TBN;
    vec3 view_pos = fs_in.view_pos;
    vec3 env_center = transform_apply(fs_in.affine_transform, mesh_center);

    Material current_material = (gl_FrontFacing ? material : back_material);
    vec4 current_color = (gl_FrontFacing ? fs_in.color : fs_in.back_color);
    change_geometry(current_material, tex_coord, view_TBN, view_pos);

    InternalMaterial internal_material = 
        fetch_internal_material(current_color, current_material, tex_coord);
    if (current_material.shading_model == SHADING_MODEL_FLAT ||
        current_material.shading_model == SHADING_MODEL_GOURAUD)
    {
        internal_material.preshading_color = (gl_FrontFacing ? preshading_color : preshading_back_color);
    }
    
    write_to_gbuffer(
        internal_material,
        view_pos,
        view_TBN[2],
        env_center,
        env_map_handle,
        is_sphere,

        view_pos_and_alpha,
        view_normal_and_emission_r,
        ambient_and_emission_g,
        diffuse_or_base_color_and_emission_b,
        specular_or_preshading_and_shininess,
        reflection,
        env_center_and_mixed_value,
        mixed_uint
    );
}