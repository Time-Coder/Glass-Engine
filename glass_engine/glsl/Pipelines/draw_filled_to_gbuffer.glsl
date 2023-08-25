#ifndef _DRAW_FILLED_TO_GBUFFER_GLSL__
#define _DRAW_FILLED_TO_GBUFFER_GLSL__

#include "../include/transform.glsl"

void draw_filled_to_gbuffer()
{
    mat3 view_TBN = fs_in.view_TBN;
    vec3 view_normal = normalize(view_TBN[2]);
    if (!gl_FrontFacing)
    {
        view_normal = -view_normal;
    }
    if (hasnan(view_normal))
    {
        return;
    }
    view_TBN[2] = view_normal;

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

    if (internal_material.shading_model != SHADING_MODEL_UNLIT && \
        internal_material.opacity < 1-1E-6)
    {
        discard;
    }

    // 几何信息
    view_pos_and_alpha.xyz = view_pos;
    view_pos_and_alpha.a = internal_material.opacity;
    view_normal_and_emission_r.xyz = view_normal;
    view_normal_and_emission_r.a = internal_material.emission.r;

    // 输出光照信息
    if (internal_material.shading_model == SHADING_MODEL_COOK_TORRANCE || \
        internal_material.shading_model == SHADING_MODEL_PBR)
    {
        ambient_or_arm_and_emission_g.r = internal_material.ambient_occlusion;
        ambient_or_arm_and_emission_g.g = internal_material.roughness;
        ambient_or_arm_and_emission_g.b = internal_material.metallic;
        diffuse_or_base_color_and_emission_b.rgb = internal_material.base_color;
    }
    else
    {
        ambient_or_arm_and_emission_g.rgb = internal_material.ambient;
        diffuse_or_base_color_and_emission_b.rgb = internal_material.diffuse;
    }
    ambient_or_arm_and_emission_g.a = internal_material.emission.g;
    diffuse_or_base_color_and_emission_b.a = internal_material.emission.b;

    if (internal_material.shading_model == SHADING_MODEL_FLAT)
    {
        specular_or_prelight_and_shininess.rgb = (gl_FrontFacing ? pre_shading_colors.Flat_color : pre_shading_colors.Flat_back_color);
    }
    else if(internal_material.shading_model == SHADING_MODEL_GOURAND)
    {
        specular_or_prelight_and_shininess.rgb = (gl_FrontFacing ? pre_shading_colors.Gouraud_color : pre_shading_colors.Gouraud_back_color);
    }
    else
    {
        specular_or_prelight_and_shininess.rgb = internal_material.specular;
    }
    specular_or_prelight_and_shininess.a = internal_material.shininess;

    reflection = internal_material.reflection;
    vec3 env_center = transform_apply(fs_in.affine_transform, mesh_center);
    env_center_and_refractive_index.rgb = env_center;
    env_center_and_refractive_index.a = internal_material.refractive_index;

    mix_uint.x = env_map_handle.x;
    mix_uint.y = env_map_handle.y;
    mix_uint.z = uint(
        (internal_material.shading_model << 3) |
        (uint(internal_material.fog) << 2) |
        (uint(internal_material.recv_shadows) << 1) |
        uint(is_sphere));
}

#endif