#ifndef _DRAW_FILLED_GLSL__
#define _DRAW_FILLED_GLSL__

#define CURRENT_COLOR (gl_FrontFacing ? fs_in.color : fs_in.back_color)
#define CURRENT_MATERIAL (gl_FrontFacing ? material : back_material)
#define CURRENT_GOURAUD_COLOR (gl_FrontFacing ? pre_shading_colors.Gouraud_color : pre_shading_colors.Gouraud_back_color)
#define CURRENT_FLAT_COLOR (gl_FrontFacing ? pre_shading_colors.Flat_color : pre_shading_colors.Flat_back_color)

vec4 draw_filled(Camera camera)
{
    mat3 view_TBN = fs_in.view_TBN;
    vec3 view_normal = normalize(view_TBN[2]);
    if (!gl_FrontFacing)
    {
        view_normal = -view_normal;
    }
    view_TBN[2] = view_normal;
    if (hasnan(view_TBN))
    {
        return vec4(0, 0, 0, 0);
    }

    vec3 view_pos = fs_in.view_pos;
    vec2 frag_tex_coord = fs_in.tex_coord.st;

    // 高度贴图和法线贴图改变几何信息
    change_geometry(
        CURRENT_MATERIAL,
        view_pos, view_normal,
        frag_tex_coord, view_TBN
    );

    // 实际使用的材质
    InternalMaterial internal_material = fetch_internal_material(
        CURRENT_COLOR, CURRENT_MATERIAL, frag_tex_coord
    );

    // 透明度过低丢弃
    if (internal_material.shading_model != 9 && internal_material.opacity < 1E-6)
    {
        discard;
    }

    if (is_opaque_pass)
    {
        if (internal_material.opacity < 1-1E-6)
        {
            discard;
        }
    }
    else
    {
        if (internal_material.opacity >= 1-1E-6)
        {
            discard;
        }
    }

    vec3 frag_pos = view_to_world(camera, view_pos);
    vec3 normal = view_dir_to_world(camera, view_normal);
    uint shading_model = internal_material.shading_model;

    vec3 out_color3 = vec3(0, 0, 0);
    if (shading_model == 9) // Unlit
    {
        out_color3 = vec3(0, 0, 0);
    }
    else if (shading_model == 1) // Flat
    {
        out_color3 = CURRENT_FLAT_COLOR;
    }
    else if (shading_model == 2) // Gouraud
    {
        out_color3 = CURRENT_GOURAUD_COLOR;
    }
    else // Phong, PhongBlinn, CookTorrance(PBR)
    {
        out_color3 = FRAG_LIGHTING(internal_material, camera, frag_pos, normal);
    }

    if (shading_model != 9)
    {
        // SSAO
        vec2 screen_tex_coord = (NDC.xy / NDC.w + 1)/2;
        float ssao_factor = texture(SSAO_map, screen_tex_coord).r;
        out_color3 *= (1-ssao_factor);

        // AO map
        out_color3 *= internal_material.ambient_occlusion;
    }

    // 自发光
    out_color3 += internal_material.emission;

    // 环境映射
    vec3 view_dir = normalize(frag_pos - camera.abs_position);
    vec4 env_color = vec4(0, 0, 0, 0);
    bool use_env_map = (env_map_handle.x > 0 || env_map_handle.y > 0);
    if (is_sphere)
    {
        env_color = sphere_reflect_refract_color(
            internal_material.reflection,
            internal_material.refraction,
            internal_material.refractive_index,
            view_dir, normal, 
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
            view_dir, normal, 
            use_skybox_map, skybox_map,
            use_skydome_map, skydome_map,
            use_env_map, sampler2D(env_map_handle)
        );
    }
    out_color3 = mix(out_color3, env_color.rgb, env_color.a);

    // 最终颜色
    return vec4(out_color3, internal_material.opacity);
}

#endif