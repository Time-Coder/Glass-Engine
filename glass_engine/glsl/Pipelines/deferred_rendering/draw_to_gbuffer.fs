#version 430 core

#if USE_BINDLESS_TEXTURE
#extension GL_ARB_bindless_texture : require
#endif

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

#if USE_BINDLESS_TEXTURE && USE_DYNAMIC_ENV_MAPPING
in flat uvec2 env_map_handle;
#endif

layout(location=3) out vec4 view_pos_and_alpha;
layout(location=4) out vec4 view_normal_and_emission_r;
layout(location=2) out vec4 ambient_and_emission_g;
layout(location=0) out vec4 base_color_and_emission_b;
layout(location=1) out vec4 specular_and_shininess;
layout(location=5) out vec4 reflection;
layout(location=6) out vec4 env_center_and_mixed_value;
layout(location=7) out uvec4 mixed_uint;

#include "../../include/InternalMaterial.glsl"
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
    if (fs_in.visible == 0)
        discard;
    vec2 tex_coord = fs_in.tex_coord.st;
    mat3 view_TBN = fs_in.view_TBN;
    vec3 view_pos = fs_in.view_pos;
    vec3 env_center = transform_apply(fs_in.affine_transform, mesh_center);
    InternalMaterial internal_material;

    if (gl_FrontFacing)
    {
        change_geometry(material, tex_coord, view_TBN, view_pos);
        internal_material = fetch_internal_material(fs_in.color, material, tex_coord);

#if USE_SHADING_MODEL_FLAT || USE_SHADING_MODEL_GOURAUD
        if (material.shading_model == SHADING_MODEL_FLAT ||
            material.shading_model == SHADING_MODEL_GOURAUD)
        {
            internal_material.base_color = fs_in.color.rgb;
        }
#endif
    }
    else
    {
        change_geometry(back_material, tex_coord, view_TBN, view_pos);
        internal_material = fetch_internal_material(fs_in.back_color, back_material, tex_coord);

#if USE_SHADING_MODEL_FLAT || USE_SHADING_MODEL_GOURAUD
        if (back_material.shading_model == SHADING_MODEL_FLAT ||
            back_material.shading_model == SHADING_MODEL_GOURAUD)
        {
            internal_material.base_color = fs_in.back_color.rgb;
        }
#endif
    }
    
    write_to_gbuffer(
        internal_material, view_pos, view_TBN[2], env_center,

#if USE_BINDLESS_TEXTURE && USE_DYNAMIC_ENV_MAPPING
        env_map_handle,
#endif

        is_sphere,
        view_pos_and_alpha, view_normal_and_emission_r, ambient_and_emission_g,
        base_color_and_emission_b, specular_and_shininess,
        reflection, env_center_and_mixed_value, mixed_uint
    );
}