#ifndef _READ_FROM_GBUFFER_GLSL_
#define _READ_FROM_GBUFFER_GLSL_

#include "../../include/ShadingInfo.glsl"

PostShadingInfo read_from_gbuffer(
    in Camera camera,
    in sampler2D world_pos_and_alpha_map,
    in sampler2D world_normal_and_emission_r_map,
    in sampler2D ambient_and_emission_g_map,
    in sampler2D diffuse_or_base_color_and_emission_b_map,
    in sampler2D specular_and_shininess_map,
    in sampler2D reflection_map,
    in sampler2D env_center_and_mixed_value_map,
    in usampler2D mixed_uint_map,
    in vec2 tex_coord)
{
    PostShadingInfo shading_info;
#if USE_DYNAMIC_ENV_MAPPING
    shading_info.env_map_handle = uvec2(0);
#endif
    shading_info.is_sphere = false;
    shading_info.world_pos = vec3(0);
    shading_info.world_normal = vec3(0);
    shading_info.env_center = vec3(0);

    vec4 world_pos_and_alpha = texture(world_pos_and_alpha_map, tex_coord);
    vec4 world_normal_and_emission_r = texture(world_normal_and_emission_r_map, tex_coord);
    vec4 ambient_and_emission_g = max(texture(ambient_and_emission_g_map, tex_coord), 0.0);
    vec4 base_color_and_emission_b = max(texture(diffuse_or_base_color_and_emission_b_map, tex_coord), 0.0);
    vec4 specular_and_shininess = max(texture(specular_and_shininess_map, tex_coord), 0.0);
    uvec4 mixed_uint = texture(mixed_uint_map, tex_coord);
    shading_info.material.reflection = max(texture(reflection_map, tex_coord), 0.0);
    vec4 env_center_and_mixed_value = texture(env_center_and_mixed_value_map, tex_coord);

    vec3 world_pos = world_pos_and_alpha.xyz;
    if (hasnan(world_pos) || length(world_pos) < 1E-6)
    {
        discard;
    }
    
    vec3 world_normal = world_normal_and_emission_r.rgb;
    if (hasnan(world_normal) || length(world_normal) < 1E-6)
    {
        discard;
    }

    shading_info.world_pos = world_pos;
    shading_info.world_normal = world_normal;
    shading_info.env_center = env_center_and_mixed_value.xyz;

#if USE_DYNAMIC_ENV_MAPPING
    shading_info.env_map_handle = mixed_uint.xy;
#endif

    shading_info.material.shading_model = uint((mixed_uint.z >> 3) & 0xF);
    shading_info.material.fog = bool((mixed_uint.z >> 2) & 0x1);
    shading_info.material.recv_shadows = bool((mixed_uint.z >> 1) & 0x1);
    shading_info.is_sphere = bool(mixed_uint.z & 0x1);
    float mixed_value = env_center_and_mixed_value.w;
    uint Toon_bands = uint(mixed_value/10.0);
    shading_info.material.refractive_index = mixed_value - 10*Toon_bands;
    shading_info.material.diffuse_bands = get_digit(Toon_bands, 1);
    shading_info.material.specular_bands = get_digit(Toon_bands, 10);
    shading_info.material.diffuse_softness = 0.05;
    shading_info.material.specular_softness = 0.02;
    shading_info.material.emission = vec3(world_normal_and_emission_r.a, ambient_and_emission_g.a, base_color_and_emission_b.a);
    shading_info.material.opacity = world_pos_and_alpha.a;
    shading_info.material.ambient = ambient_and_emission_g.rgb;

    if (shading_info.material.shading_model == SHADING_MODEL_COOK_TORRANCE ||
        shading_info.material.shading_model == SHADING_MODEL_PBR ||
        shading_info.material.shading_model == SHADING_MODEL_FLAT ||
        shading_info.material.shading_model == SHADING_MODEL_GOURAUD)
    {
        shading_info.material.base_color = base_color_and_emission_b.rgb;
    }
    else
    {
        shading_info.material.base_color = base_color_and_emission_b.rgb;
        shading_info.material.specular = specular_and_shininess.rgb;
        shading_info.material.shininess = specular_and_shininess.a;
    }

    shading_info.material.ao = (mixed_uint.w >> 24) / 255.0;
    shading_info.material.roughness = (((uint(0xFF) << 16) & mixed_uint.w) >> 16) / 255.0;
    shading_info.material.metallic = (((uint(0xFF) << 8) & mixed_uint.w) >> 8) / 255.0;
    shading_info.material.rim_power = (uint(0xFF) & mixed_uint.w) / 255.0;
    shading_info.material.shadow_visibility = 1;
    
    return shading_info;
}

#endif