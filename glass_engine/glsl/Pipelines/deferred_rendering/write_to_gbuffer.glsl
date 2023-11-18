#include "../../include/Material.glsl"

void write_to_gbuffer(
    in InternalMaterial internal_material,
    in vec3 view_pos, in vec3 view_normal, in vec3 env_center,
    in uvec2 env_map_handle, in bool is_sphere,
    out vec4 view_pos_and_alpha, out vec4 view_normal_and_emission_r,
    out vec4 ambient_and_emission_g, out vec4 diffuse_or_base_color_and_emission_b,
    out vec4 specular_or_preshading_and_shininess, out vec4 reflection,
    out vec4 env_center_and_mixed_value, out uvec4 mixed_uint)
{
    if (internal_material.opacity < 1-1E-6)
    {
        discard;
    }

    view_pos_and_alpha.xyz = view_pos;
    view_pos_and_alpha.a = internal_material.opacity;
    view_normal_and_emission_r.xyz = view_normal;
    view_normal_and_emission_r.a = internal_material.emission.r;
    ambient_and_emission_g.rgb = internal_material.ambient;

    if (internal_material.shading_model == SHADING_MODEL_COOK_TORRANCE ||
        internal_material.shading_model == SHADING_MODEL_PBR)
    {
        diffuse_or_base_color_and_emission_b.rgb = internal_material.base_color;
    }
    else
    {
        diffuse_or_base_color_and_emission_b.rgb = internal_material.diffuse;
    }

    ambient_and_emission_g.a = internal_material.emission.g;
    diffuse_or_base_color_and_emission_b.a = internal_material.emission.b;

    if (internal_material.shading_model == SHADING_MODEL_FLAT ||
        internal_material.shading_model == SHADING_MODEL_GOURAUD)
    {
        specular_or_preshading_and_shininess.rgb = internal_material.preshading_color;
    }
    else
    {
        specular_or_preshading_and_shininess.rgb = internal_material.specular;
    }

    specular_or_preshading_and_shininess.a = internal_material.shininess;
    reflection = internal_material.reflection;
    env_center_and_mixed_value.xyz = env_center;
    env_center_and_mixed_value.w =
        internal_material.refractive_index + 
        10 * internal_material.diffuse_bands + 
        100 * internal_material.specular_bands;

    mixed_uint.x = env_map_handle.x;
    mixed_uint.y = env_map_handle.y;
    mixed_uint.z = uint(
        (internal_material.shading_model << 3) |
        (uint(internal_material.fog) << 2) |
        (uint(internal_material.recv_shadows) << 1) |
        uint(is_sphere));
    mixed_uint.w =
        (uint(255 * internal_material.ao) << 24) | 
        (uint(255 * internal_material.roughness) << 16) | 
        (uint(255 * internal_material.metallic) << 8) | 
         uint(255 * internal_material.rim_power);
}