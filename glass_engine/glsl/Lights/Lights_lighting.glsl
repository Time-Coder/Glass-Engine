#ifndef _LIGHTS_LIGHTING_GLSL__
#define _LIGHTS_LIGHTING_GLSL__

#include "Lights.glsl"
#include "DirLight_lighting.glsl"
#include "PointLight_lighting.glsl"
#include "SpotLight_lighting.glsl"

vec3 get_diffuse_color(InternalMaterial internal_material, Camera CSM_camera, vec3 view_dir, vec3 frag_pos, vec3 frag_normal)
{
    vec3 diffuse_color = vec3(0.2);

    // 点光源
    for(int i = 0; i < n_point_lights; i++)
    {
        diffuse_color += get_diffuse_color(point_lights[i], internal_material, view_dir, frag_pos, frag_normal);
    }

    // 平行光
    for(int i = 0; i < n_dir_lights; i++)
    {
        diffuse_color += get_diffuse_color(dir_lights[i], internal_material, CSM_camera, view_dir, frag_pos, frag_normal);
    }

    // 聚光
    for(int i = 0; i < n_spot_lights; i++)
    {
        diffuse_color += get_diffuse_color(spot_lights[i], internal_material, view_dir, frag_pos, frag_normal);
    }

    return soft_min(2*diffuse_color, vec3(1), 0.1);
}

vec3 get_specular_color(InternalMaterial internal_material, Camera CSM_camera, vec3 out_dir, vec3 frag_pos, vec3 frag_normal)
{
    vec3 specular_color = vec3(0);

    // 平行光
    for(int i = 0; i < n_dir_lights; i++)
    {
        specular_color += get_specular_color(
            dir_lights[i], internal_material, CSM_camera,
            out_dir, frag_pos, frag_normal
        );
    }

    // 点光源
    for(int i = 0; i < n_point_lights; i++)
    {
        specular_color += get_specular_color(
            point_lights[i], internal_material,
            out_dir, frag_pos, frag_normal
        );
    }

    // 聚光
    for(int i = 0; i < n_spot_lights; i++)
    {
        specular_color += get_specular_color(
            spot_lights[i], internal_material,
            out_dir, frag_pos, frag_normal
        );
    }

    return specular_color;
}

vec3 lighting(InternalMaterial internal_material, Camera CSM_camera, vec3 camera_pos, vec3 frag_pos, vec3 frag_normal)
{
    vec3 out_color3 = internal_material.ambient;

    // 平行光
    for(int i = 0; i < n_dir_lights; i++)
    {
        out_color3 += lighting(
            dir_lights[i], internal_material, CSM_camera,
            camera_pos, frag_pos, frag_normal
        );
    }

    // 点光源
    for(int i = 0; i < n_point_lights; i++)
    {
        out_color3 += lighting(
            point_lights[i], internal_material,
            camera_pos, frag_pos, frag_normal
        );
    }

    // 聚光
    for(int i = 0; i < n_spot_lights; i++)
    {
        out_color3 += lighting(
            spot_lights[i], internal_material,
            camera_pos, frag_pos, frag_normal
        );
    }

    return out_color3;
}

#endif