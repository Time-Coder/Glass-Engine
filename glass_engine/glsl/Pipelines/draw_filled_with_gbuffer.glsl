#ifndef _DRAW_FILLED_WITH_GBUFFER__
#define _DRAW_FILLED_WITH_GBUFFER__

vec4 draw_filled_with_gbuffer(Camera camera,
    vec4 view_pos_and_alpha,
    vec4 view_normal_and_emission_r,
    vec4 ambient_or_arm_and_emission_g,
    vec4 diffuse_or_base_color_and_emission_b,
    vec4 specular_or_prelight_and_shininess,
    vec4 reflection, vec4 env_center_and_refractive_index, float SSAO_factor,
    uvec3 mix_uint
)
{
    vec3 view_pos = view_pos_and_alpha.xyz;
    if(hasnan(view_pos) || length(view_pos) < 1E-6)
    {
        discard;
        // return vec4(0, 0, 0, 0);
    }

    vec3 view_normal = view_normal_and_emission_r.rgb;
    if(hasnan(view_normal) || length(view_normal) < 1E-6)
    {
        discard;
        // return vec4(0, 0, 0, 0);
    }

    float refractive_index = env_center_and_refractive_index.a;
    vec3 env_center = env_center_and_refractive_index.rgb;
    uvec2 env_map_handle = mix_uint.xy;
    uint shading_model = uint((mix_uint.z >> 3) & 0xF);
    bool use_fog = bool((mix_uint.z >> 2) & 0x1);
    bool recv_shadows = bool((mix_uint.z >> 1) & 0x1);
    bool is_sphere = bool(mix_uint.z & 0x1);

    InternalMaterial internal_material;
    internal_material.fog = use_fog;
    internal_material.shading_model = shading_model;
    internal_material.emission = vec3(view_normal_and_emission_r.a, ambient_or_arm_and_emission_g.a, diffuse_or_base_color_and_emission_b.a);
    internal_material.opacity = view_pos_and_alpha.a;
    internal_material.reflection = reflection;
    internal_material.refractive_index = refractive_index;
    internal_material.recv_shadows = recv_shadows;

    internal_material.ambient_occlusion = 1;
    if(shading_model == 8 || shading_model == 11)
    {
        internal_material.ambient_occlusion = ambient_or_arm_and_emission_g.r;
        internal_material.roughness = ambient_or_arm_and_emission_g.g;
        internal_material.metallic = ambient_or_arm_and_emission_g.b;
        internal_material.base_color = diffuse_or_base_color_and_emission_b.rgb;
    }
    else
    {
        internal_material.ambient = ambient_or_arm_and_emission_g.rgb;
        internal_material.diffuse = diffuse_or_base_color_and_emission_b.rgb;
        internal_material.specular = specular_or_prelight_and_shininess.rgb;
        internal_material.shininess = specular_or_prelight_and_shininess.a;
    }

    // 透明度过低丢弃
    if (internal_material.shading_model != 9 && internal_material.opacity < 1E-6)
    {
        discard;
    }

    if (internal_material.shading_model == 9)
    {
        return vec4(internal_material.emission, internal_material.opacity);
    }

    vec3 frag_pos = view_to_world(camera, view_pos);
    vec3 frag_normal = view_dir_to_world(camera, view_normal);

    // 环境映射
    vec3 view_dir = normalize(frag_pos - camera.abs_position);
    vec4 env_color = vec4(0, 0, 0, 0);
    bool use_env_map = (env_map_handle != 0);
    if (is_sphere)
    {
        env_color = sphere_reflect_refract_color(
            internal_material, camera,
            env_center, view_dir, frag_pos, frag_normal,
            use_skybox_map, skybox_map,
            use_skydome_map, skydome_map,
            use_env_map, sampler2D(env_map_handle)
        );
    }
    else
    {
        env_color = reflect_refract_color(
            internal_material, camera,
            env_center, view_dir, frag_pos, frag_normal, 
            use_skybox_map, skybox_map,
            use_skydome_map, skydome_map,
            use_env_map, sampler2D(env_map_handle)
        );
    }

    if (env_color.a > 1-1E-6)
    {
        return vec4(env_color.rgb+internal_material.emission, internal_material.opacity);
    }

    vec3 out_color3 = vec3(0, 0, 0);
    if (shading_model == 1 || shading_model == 2) // pre lighting
    {
        out_color3 = specular_or_prelight_and_shininess.rgb;
    }
    else // frag lighting
    {
        out_color3 = FRAG_LIGHTING(internal_material, camera, camera.abs_position, frag_pos, frag_normal);
    }

    // SSAO
    out_color3 *= (1 - SSAO_factor);

    // AO map
    out_color3 *= internal_material.ambient_occlusion;

    // 自发光
    out_color3 += internal_material.emission;
    out_color3 = mix(out_color3, env_color.rgb, env_color.a);

    // 雾
    if (use_fog)
    {
        out_color3 = fog_apply(fog, out_color3, camera.abs_position, frag_pos);
    }

    return vec4(out_color3, internal_material.opacity);
}

#endif