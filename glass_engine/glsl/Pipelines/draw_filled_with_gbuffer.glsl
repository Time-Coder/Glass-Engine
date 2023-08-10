#ifndef _DRAW_FILLED_WITH_GBUFFER__
#define _DRAW_FILLED_WITH_GBUFFER__

vec4 draw_filled_with_gbuffer(Camera camera,
    vec4 view_pos_and_alpha,
    vec4 view_normal_and_emission_r,
    vec4 ambient_or_arm_and_emission_g,
    vec4 diffuse_or_albedo_and_emission_b,
    vec4 specular_or_prelight_and_shininess,
    vec4 reflection, vec4 refraction, float SSAO_factor,
    uvec4 mix_uint
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

    float refractive_index = mix_uint.x * 255;
    uvec2 env_map_handle = mix_uint.yz;
    uint shading_model = (mix_uint.w >> 2);
    bool recv_shadows = bool((mix_uint.w >> 1) & 0x1);
    bool is_sphere = bool(mix_uint.w & 0x1);

    InternalMaterial internal_material;
    internal_material.shading_model = shading_model;
    internal_material.emission = vec3(view_normal_and_emission_r.a, ambient_or_arm_and_emission_g.a, diffuse_or_albedo_and_emission_b.a);
    internal_material.opacity = view_pos_and_alpha.a;
    internal_material.reflection = reflection;
    internal_material.refraction = refraction;
    internal_material.refractive_index = refractive_index;
    internal_material.recv_shadows = recv_shadows;

    internal_material.ambient_occlusion = 1;
    if(shading_model == 8 || shading_model == 11)
    {
        internal_material.ambient_occlusion = ambient_or_arm_and_emission_g.r;
        internal_material.roughness = ambient_or_arm_and_emission_g.g;
        internal_material.metallic = ambient_or_arm_and_emission_g.b;
        internal_material.albedo = diffuse_or_albedo_and_emission_b.rgb;
    }
    else
    {
        internal_material.ambient = ambient_or_arm_and_emission_g.rgb;
        internal_material.diffuse = diffuse_or_albedo_and_emission_b.rgb;
        internal_material.specular = specular_or_prelight_and_shininess.rgb;
        internal_material.shininess = specular_or_prelight_and_shininess.a;
    }

    // 透明度过低丢弃
    if (internal_material.shading_model != 9 && internal_material.opacity < 1E-6)
    {
        discard;
    }

    vec3 frag_pos = view_to_world(camera, view_pos);
    vec3 frag_normal = view_dir_to_world(camera, view_normal);

    vec3 out_color3 = vec3(0, 0, 0);
    if (shading_model == 9) // Unlit
    {
        out_color3 = vec3(0, 0, 0);
    }
    else if (shading_model == 1 || shading_model == 2) // Flat
    {
        float shadow_visibility = 1;
        if (internal_material.recv_shadows)
        {
            shadow_visibility = SHADOW_VISIBILITY(camera, frag_pos, frag_normal);
        }
        out_color3 = max(shadow_visibility, 0.1) * specular_or_prelight_and_shininess.rgb;
    }
    else // Phong, PhongBlinn, CookTorrance
    {
        out_color3 = FRAG_LIGHTING(internal_material, camera, camera.abs_position, frag_pos, frag_normal);
    }

    if (shading_model != 9) // Unlit
    {
        // SSAO
        out_color3 *= (1 - SSAO_factor);

        // AO map
        out_color3 *= internal_material.ambient_occlusion;
    }

    // 自发光
    out_color3 += internal_material.emission;

    // 环境映射
    vec3 view_dir = normalize(frag_pos - camera.abs_position);
    vec4 env_color = vec4(0, 0, 0, 0);
    bool use_env_map = (env_map_handle != 0);
    if (is_sphere)
    {
        env_color = sphere_reflect_refract_color(
            internal_material.reflection,
            internal_material.refraction,
            internal_material.refractive_index,
            view_dir, frag_normal, 
            use_skybox_map, skybox_map,
            use_skydome_map, skydome_map,
            use_env_map, sampler2D(env_map_handle)
        );
    }
    else
    {
        env_color = reflect_refract_color(
            internal_material.reflection,
            internal_material.refraction,
            internal_material.refractive_index,
            view_dir, frag_normal, 
            use_skybox_map, skybox_map,
            use_skydome_map, skydome_map,
            use_env_map, sampler2D(env_map_handle)
        );
    }
    out_color3 = mix(out_color3, env_color.rgb, env_color.a);

    return vec4(out_color3, internal_material.opacity);
}

#endif