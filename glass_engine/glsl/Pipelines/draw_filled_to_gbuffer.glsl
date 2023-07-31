#ifndef _DRAW_FILLED_TO_GBUFFER_GLSL__
#define _DRAW_FILLED_TO_GBUFFER_GLSL__

void draw_filled_to_gbuffer()
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
        return;
    }

    vec3 view_pos = fs_in.view_pos;
    vec2 frag_tex_coord = fs_in.tex_coord.st;

    // 高度贴图和法线贴图改变几何信息
    change_geometry(
        (gl_FrontFacing ? material : back_material),
        view_pos, view_normal,
        frag_tex_coord, view_TBN
    );

    // 实际使用的材质
    InternalMaterial internal_material = fetch_internal_material(
        (gl_FrontFacing ? fs_in.color : fs_in.back_color),
        (gl_FrontFacing ? material : back_material),
        frag_tex_coord
    );

    if (internal_material.shading_model != 9 && internal_material.opacity < 1-1E-6)
    {
        discard;
    }

    // 几何信息
    view_pos_and_alpha.xyz = view_pos;
    view_pos_and_alpha.a = internal_material.opacity;
    view_normal_and_emission_r.xyz = view_normal;
    view_normal_and_emission_r.a = internal_material.emission.r;

    // 输出光照信息
    if (internal_material.shading_model == 8 || internal_material.shading_model == 11)
    {
        ambient_or_arm_and_emission_g.r = internal_material.ambient_occlusion;
        ambient_or_arm_and_emission_g.g = internal_material.roughness;
        ambient_or_arm_and_emission_g.b = internal_material.metallic;
        diffuse_or_albedo_and_emission_b.rgb = internal_material.albedo;
    }
    else
    {
        ambient_or_arm_and_emission_g.rgb = internal_material.ambient;
        diffuse_or_albedo_and_emission_b.rgb = internal_material.diffuse;
    }
    ambient_or_arm_and_emission_g.a = internal_material.emission.g;
    diffuse_or_albedo_and_emission_b.a = internal_material.emission.b;

    if (internal_material.shading_model == 1) // Flat
    {
        specular_or_prelight_and_shininess.rgb = (gl_FrontFacing ? pre_shading_colors.Flat_color : pre_shading_colors.Flat_back_color);
    }
    else if(internal_material.shading_model == 2) // Gouraud
    {
        specular_or_prelight_and_shininess.rgb = (gl_FrontFacing ? pre_shading_colors.Gouraud_color : pre_shading_colors.Gouraud_back_color);
    }
    else
    {
        specular_or_prelight_and_shininess.rgb = internal_material.specular;
    }
    specular_or_prelight_and_shininess.a = internal_material.shininess;

    reflection = internal_material.reflection;    
    refraction = internal_material.refraction;

    mix_uint.x = internal_material.shading_model;
    mix_uint.y = env_map_handle.x;
    mix_uint.z = env_map_handle.y;
    mix_uint.w = uint((uint(255*internal_material.refractive_index) << 1) | uint(is_sphere));
}

#endif