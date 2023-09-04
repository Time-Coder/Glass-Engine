#ifndef _SHADING_ALL_GLSL__
#define _SHADING_ALL_GLSL__

#include "Camera.glsl"
#include "sampling.glsl"
#include "Material.glsl"
#include "parallax_mapping.glsl"
#include "transform.glsl"
#include "ShadingInfo.glsl"
#include "fog.glsl"
#include "env_mapping.glsl"
#include "../Lights/Lights.glsl"

vec4 post_shading_all(Camera camera, Camera CSM_camera, PostShadingInfo shading_info)
{
    if (shading_info.material.shading_model == SHADING_MODEL_UNLIT)
    {
        vec4 final_color = vec4(shading_info.material.emission, shading_info.material.opacity);
        if (shading_info.material.fog)
        {
            final_color.rgb = fog_apply(shading_info.fog, final_color.rgb, camera.abs_position, shading_info.world_pos);
        }
        return final_color;
    }

    // 环境映射
    vec3 view_dir = normalize(shading_info.world_pos - camera.abs_position);
    vec4 env_color = vec4(0, 0, 0, 0);
    if (shading_info.is_sphere)
    {
        env_color = sphere_reflect_refract_color(
            shading_info.material, CSM_camera,

            shading_info.env_center, view_dir,
            shading_info.world_pos, shading_info.world_normal,

            shading_info.use_skybox_map, shading_info.skybox_map,
            shading_info.use_skydome_map, shading_info.skydome_map,
            shading_info.use_env_map, shading_info.env_map
        );
    }
    else
    {
        env_color = reflect_refract_color(
            shading_info.material, CSM_camera,

            shading_info.env_center, view_dir,
            shading_info.world_pos, shading_info.world_normal,

            shading_info.use_skybox_map, shading_info.skybox_map,
            shading_info.use_skydome_map, shading_info.skydome_map,
            shading_info.use_env_map, shading_info.env_map
        );
    }
    if (env_color.a >= 1-1E-6)
    {
        vec4 final_color = vec4(env_color.rgb+shading_info.material.emission, shading_info.material.opacity);
        if (shading_info.material.fog)
        {
            final_color.rgb = fog_apply(shading_info.fog, final_color.rgb, camera.abs_position, shading_info.world_pos);
        }
        return final_color;
    }

    vec3 out_color3;
    if (shading_info.material.shading_model == SHADING_MODEL_FLAT ||
        shading_info.material.shading_model == SHADING_MODEL_GOURAUD)
    {
        out_color3 = shading_info.material.preshading_color;
    }
    else
    {
        out_color3 = lighting(shading_info.material, CSM_camera, camera.abs_position, shading_info.world_pos, shading_info.world_normal);
    }
    
    // SSAO
    float ssao_factor = textureColor(shading_info.SSAO_map, shading_info.screen_tex_coord).r;
    out_color3 *= (1-ssao_factor);

    // AO map
    out_color3 *= shading_info.material.ao;

    // 自发光
    out_color3 += shading_info.material.emission;
    out_color3 = mix(out_color3, env_color.rgb, env_color.a);

    // 雾
    if (shading_info.material.fog)
    {
        out_color3 = fog_apply(shading_info.fog, out_color3, camera.abs_position, shading_info.world_pos);
    }

    // 最终颜色
    return vec4(out_color3, shading_info.material.opacity);
}

vec4 shading_all(Camera camera, Camera CSM_camera, ShadingInfo shading_info)
{
    // 高度贴图和法线贴图改变几何信息
    change_geometry(shading_info.material, shading_info.tex_coord, shading_info.view_TBN, shading_info.view_pos);
    if (hasnan(shading_info.view_TBN[2]) || length(shading_info.view_TBN[2]) < 1E-6)
    {
        discard;
    }

    // 实际使用的材质
    InternalMaterial internal_material = fetch_internal_material(
        shading_info.color, shading_info.material, shading_info.tex_coord
    );

    // 透明度过低丢弃
    if (internal_material.opacity < 1E-6)
    {
        discard;
    }

    if (shading_info.is_opaque_pass)
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

    vec3 world_pos = view_to_world(camera, shading_info.view_pos);
    vec3 world_normal = view_dir_to_world(camera, shading_info.view_TBN[2]);
    vec3 env_center = transform_apply(shading_info.affine_transform, shading_info.mesh_center);
    vec2 screen_tex_coord = (shading_info.NDC.xy / shading_info.NDC.w + 1)/2;
    internal_material.preshading_color = shading_info.preshading_color;

    PostShadingInfo post_shading_info = PostShadingInfo(
        internal_material,

        shading_info.use_skybox_map,
        shading_info.skybox_map,
        shading_info.use_skydome_map,
        shading_info.skydome_map,
        shading_info.use_env_map,
        shading_info.env_map,
        shading_info.SSAO_map,
        shading_info.is_sphere,
        shading_info.fog,

        world_pos,
        world_normal,
        env_center,
        screen_tex_coord
    );

    return post_shading_all(camera, CSM_camera, post_shading_info);
}

vec4 shading_all(Camera camera, ShadingInfo shading_info)
{
    return shading_all(camera, camera, shading_info);
}

#endif