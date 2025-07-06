#version 430 core

#if USE_BINDLESS_TEXTURE
#extension GL_ARB_bindless_texture : require
#endif

in VertexOut
{
    mat4 affine_transform;
    vec3 world_pos;
    mat3 world_TBN;
    vec3 tex_coord;
    vec4 color;
    flat int visible;
#if USE_BINDLESS_TEXTURE && USE_DYNAMIC_ENV_MAPPING
    flat uvec2 env_map_handle;
#endif
} fs_in;

layout(location=3) out vec4 world_pos_and_alpha;
layout(location=4) out vec4 world_normal_and_emission_r;
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

uniform Camera camera;
uniform Material material;
uniform vec3 mesh_center;

void main()
{
    if (fs_in.visible == 0)
    {
        discard;
    }

    vec2 tex_coord = fs_in.tex_coord.st;
    mat3 world_TBN = fs_in.world_TBN;
    vec3 world_pos = fs_in.world_pos;
    vec3 env_center = transform_apply(fs_in.affine_transform, mesh_center);
    change_geometry(camera, material, tex_coord, world_TBN, world_pos);
    InternalMaterial internal_material = fetch_internal_material(fs_in.color, material, tex_coord);

    write_to_gbuffer(
        internal_material, world_pos, world_TBN[2], env_center,
#if USE_BINDLESS_TEXTURE && USE_DYNAMIC_ENV_MAPPING
        fs_in.env_map_handle,
#endif
        false,
        world_pos_and_alpha, world_normal_and_emission_r, ambient_and_emission_g,
        base_color_and_emission_b, specular_and_shininess,
        reflection, env_center_and_mixed_value, mixed_uint
    );
}