#ifndef _DIR_LIGHT_GLSL__
#define _DIR_LIGHT_GLSL__

#include "../include/Material.glsl"
#include "../include/math.glsl"
#include "../include/Camera.glsl"
#include "../ShadingModels/lighting.glsl"

struct DirLight
{
    // 内参数
    vec3 color;
    float brightness;
    vec3 ambient;
    vec3 diffuse;
    vec3 specular;
    bool generate_shadows; // 是否产生阴影
    uvec2 depth_map_handle;
    float max_back_offset;
    float rim_power;

    // 外参数
    vec3 direction;
    quat abs_orientation;
};

#include "DirLight_shadow_mapping.glsl"

vec3 lighting(
    DirLight light, InternalMaterial material, Camera CSM_camera,
    vec3 camera_pos, vec3 frag_pos, vec3 frag_normal)
{
    vec3 to_light = -normalize(light.direction);
    vec3 to_camera = normalize(camera_pos - frag_pos);

    material.ambient = light.ambient * material.ambient;
    material.diffuse = light.diffuse * material.diffuse;
    material.specular = light.specular * material.specular;
    material.light_rim_power = light.rim_power;

    if (light.generate_shadows && material.recv_shadows &&
        (light.depth_map_handle.x > 0 || light.depth_map_handle.y > 0))
    {
        float shadow_visibility = PCF(light, CSM_camera, frag_pos, frag_normal);
        material.diffuse *= shadow_visibility;
        material.specular *= shadow_visibility;
    }

    vec3 lighting_color = lighting(to_light, to_camera, frag_normal, material);
    return light.brightness * light.color * lighting_color;
}

vec3 get_ambient_diffuse(
    DirLight light, bool recv_shadows, Camera CSM_camera,
    vec3 frag_pos, vec3 frag_normal)
{
    vec3 to_light = -normalize(light.direction);
    vec3 factor = Lambert_diffuse(to_light, frag_normal)*light.diffuse + 0.2*light.ambient;
    float shadow_visibility = 1;
    if (light.generate_shadows && recv_shadows &&
        (light.depth_map_handle.x > 0 || light.depth_map_handle.y > 0))
    {
        shadow_visibility = PCF(light, CSM_camera, frag_pos, frag_normal);
    }

    return shadow_visibility * factor * light.brightness * light.color;
}

vec3 get_specular(
    DirLight light, InternalMaterial material, Camera CSM_camera,
    vec3 view_dir, vec3 frag_pos, vec3 frag_normal)
{
    vec3 to_light = -normalize(light.direction);
    vec3 to_camera = normalize(reflect(-view_dir, frag_normal));

    float specular_factor = 0;
    if (material.shading_model == SHADING_MODEL_PHONG)
    {
        specular_factor = Phong_specular(to_light, to_camera, frag_normal, material.shininess);
    }
    else if (material.shading_model == SHADING_MODEL_PHONG_BLINN)
    {
        specular_factor = PhongBlinn_specular(to_light, to_camera, frag_normal, material.shininess);
    }

    float shadow_visibility = 1;
    if (light.generate_shadows && material.recv_shadows &&
        (light.depth_map_handle.x > 0 || light.depth_map_handle.y > 0))
    {
        shadow_visibility = PCF(light, CSM_camera, frag_pos, frag_normal);
    }
    
    return shadow_visibility * specular_factor * light.brightness * light.color * light.specular;
}

#endif