#version 460 core


in GeometryOut
{
    vec3 view_pos;
    mat3 view_TBN;
    vec3 tex_coord;
    vec4 color;
    vec4 back_color;
    flat bool visible;
} fs_in;

in PreShadingColors
{
    vec3 Gouraud_color;
    vec3 Gouraud_back_color;
    flat vec3 Flat_color;
    flat vec3 Flat_back_color;
} pre_shading_colors;

in flat uvec2 env_map_handle;

// 几何信息
layout(location=0) out vec4 view_pos_and_alpha;
layout(location=1) out vec4 view_normal_and_emission_r;

// 光照信息
layout(location=2) out vec4 ambient_or_arm_and_emission_g;
layout(location=3) out vec4 diffuse_or_albedo_and_emission_b;
layout(location=4) out vec4 specular_or_prelight_and_shininess;
layout(location=5) out vec4 reflection;
layout(location=6) out vec4 refraction;
layout(location=7) out uvec4 mix_uint;

#include "../../include/Material.glsl"
#include "../../include/fragment_utils.glsl"
#include "../../include/math.glsl"

uniform Material material;
uniform Material back_material;
uniform bool is_sphere;

#include "../draw_filled_to_gbuffer.glsl"

void main()
{
    if (!fs_in.visible)
    {
        discard;
    }
    
    draw_filled_to_gbuffer();
}