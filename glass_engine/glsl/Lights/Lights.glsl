#ifndef _LIGHTS_GLSL__
#define _LIGHTS_GLSL__

#include "PointLight.glsl"
#include "DirLight.glsl"
#include "SpotLight.glsl"

buffer PointLights
{
    int n_point_lights;
    PointLight point_lights[];
};

buffer DirLights
{
    int n_dir_lights;
    DirLight dir_lights[];
};

buffer SpotLights
{
    int n_spot_lights;
    SpotLight spot_lights[];
};

vec3 get_ambient_diffuse(bool recv_shadows, Camera CSM_camera, vec3 frag_pos, vec3 frag_normal)
{
    vec3 factor = vec3(0.2);

    // 点光源
    for(int i = 0; i < n_point_lights; i++)
    {
        factor += get_ambient_diffuse(point_lights[i], recv_shadows, frag_pos, frag_normal);
    }

    // 平行光
    for(int i = 0; i < n_dir_lights; i++)
    {
        factor += get_ambient_diffuse(dir_lights[i], recv_shadows, CSM_camera, frag_pos, frag_normal);
    }

    // 聚光
    for(int i = 0; i < n_spot_lights; i++)
    {
        factor += get_ambient_diffuse(spot_lights[i], recv_shadows, frag_pos, frag_normal);
    }

    return soft_min(2*factor, vec3(1,1,1), 0.1);
}

vec3 get_specular(InternalMaterial internal_material, Camera CSM_camera, vec3 view_dir, vec3 frag_pos, vec3 frag_normal)
{
    vec3 specular_color = vec3(0);

    // 平行光
    for(int i = 0; i < n_dir_lights; i++)
    {
        specular_color += get_specular(
            dir_lights[i], internal_material, CSM_camera,
            view_dir, frag_pos, frag_normal
        );
    }

    // 点光源
    for(int i = 0; i < n_point_lights; i++)
    {
        specular_color += get_specular(
            point_lights[i], internal_material,
            view_dir, frag_pos, frag_normal
        );
    }

    // 聚光
    for(int i = 0; i < n_spot_lights; i++)
    {
        specular_color += get_specular(
            spot_lights[i], internal_material,
            view_dir, frag_pos, frag_normal
        );
    }

    return 3*specular_color;
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