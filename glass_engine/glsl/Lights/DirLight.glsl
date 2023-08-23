#ifndef _DIR_LIGHT_GLSL__
#define _DIR_LIGHT_GLSL__

#include "../include/Material.glsl"
#include "../include/math.glsl"
#include "../include/Camera.glsl"
#include "../ShadingModels/Phong.glsl"
#include "../ShadingModels/PhongBlinn.glsl"
#include "../ShadingModels/Gouraud.glsl"
#include "../ShadingModels/Flat.glsl"
#include "../ShadingModels/CookTorrance.glsl"

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

    // 外参数
    vec3 direction;
    quat abs_orientation;
};

#include "DirLight_shadow_mapping.glsl"

vec3 ambient_diffuse_factor(
    DirLight light, bool recv_shadows, Camera CSM_camera,
    vec3 frag_pos, vec3 frag_normal)
{
    vec3 to_light = -normalize(light.direction);
    vec3 diffuse_factor = Lambert_diffuse(to_light, frag_normal) + 0.1*light.ambient;
    float shadow_visibility = 1;
    if (light.generate_shadows && recv_shadows &&
        (light.depth_map_handle.x > 0 || light.depth_map_handle.y > 0))
    {
        shadow_visibility = PCF(light, CSM_camera, frag_pos, frag_normal);
    }

    return shadow_visibility * diffuse_factor * light.brightness * light.color;
}

vec3 PhongBlinn_specular(
    DirLight light, InternalMaterial material, Camera CSM_camera,
    vec3 view_dir, vec3 frag_pos, vec3 frag_normal)
{
    vec3 to_light = -normalize(light.direction);
    vec3 to_camera = normalize(reflect(-view_dir, frag_normal));
    float specular_factor = PhongBlinn_specular(to_light, to_camera, frag_normal, material.shininess);
    float shadow_visibility = 1;
    if (light.generate_shadows && material.recv_shadows &&
        (light.depth_map_handle.x > 0 || light.depth_map_handle.y > 0))
    {
        shadow_visibility = PCF(light, CSM_camera, frag_pos, frag_normal);
    }
    
    return shadow_visibility * specular_factor * light.brightness * light.color;
}

vec3 PhongBlinn_lighting(
    DirLight light, InternalMaterial material, Camera CSM_camera,
    vec3 camera_pos, vec3 frag_pos, vec3 frag_normal)
{
    // 基础向量
    vec3 to_light = -normalize(light.direction);
    vec3 to_camera = normalize(camera_pos - frag_pos);

    // 光照参数
    material.ambient = light.ambient * material.ambient;
    material.diffuse = light.diffuse * material.diffuse;
    material.specular = light.specular * material.specular;

    if (light.generate_shadows && material.recv_shadows && (light.depth_map_handle.x > 0 || light.depth_map_handle.y > 0))
    {
        float shadow_visibility = PCF(light, CSM_camera, frag_pos, frag_normal);
        material.diffuse *= shadow_visibility;
        material.specular *= shadow_visibility;
    }

    // 光照颜色
    vec3 lighting_color = PhongBlinn_lighting(to_light, to_camera, frag_normal, material);

    // 最终颜色
    vec3 final_color = light.brightness * light.color * lighting_color;
    
    return final_color;
}

vec3 Phong_specular(
    DirLight light, InternalMaterial material, Camera CSM_camera,
    vec3 view_dir, vec3 frag_pos, vec3 frag_normal)
{
    vec3 to_light = -normalize(light.direction);
    vec3 to_camera = normalize(reflect(-view_dir, frag_normal));
    float specular_factor = Phong_specular(to_light, to_camera, frag_normal, material.shininess);
    float shadow_visibility = 1;
    if (light.generate_shadows && material.recv_shadows &&
        (light.depth_map_handle.x > 0 || light.depth_map_handle.y > 0))
    {
        shadow_visibility = PCF(light, CSM_camera, frag_pos, frag_normal);
    }

    return shadow_visibility * specular_factor * light.brightness * light.color;
}

vec3 Phong_lighting(
    DirLight light, InternalMaterial material, Camera CSM_camera,
    vec3 camera_pos, vec3 frag_pos, vec3 frag_normal)
{
    // 基础向量
    vec3 to_light = -normalize(light.direction);
    vec3 to_camera = normalize(camera_pos - frag_pos);

    // 光照参数
    material.ambient = light.ambient * material.ambient;
    material.diffuse = light.diffuse * material.diffuse;
    material.specular = light.specular * material.specular;

    if (light.generate_shadows && material.recv_shadows && (light.depth_map_handle.x > 0 || light.depth_map_handle.y > 0))
    {
        float shadow_visibility = PCF(light, CSM_camera, frag_pos, frag_normal);
        material.diffuse *= shadow_visibility;
        material.specular *= shadow_visibility;
    }

    // 光照颜色
    vec3 lighting_color = Phong_lighting(to_light, to_camera, frag_normal, material);

    // 最终颜色
    vec3 final_color = light.brightness * light.color * lighting_color;
    
    return final_color;
}

vec3 Gouraud_lighting(
    DirLight light, InternalMaterial material, Camera CSM_camera,
    vec3 camera_pos, vec3 frag_pos, vec3 frag_normal)
{
    return Phong_lighting(light, material, CSM_camera, camera_pos, frag_pos, frag_normal);
}

vec3 Flat_lighting(
    DirLight light, InternalMaterial material,
    vec3 face_pos, vec3 face_normal)
{
    vec3 to_light = -normalize(light.direction);
    
    // 光照参数
    material.ambient = light.ambient * material.ambient;
    material.diffuse = light.diffuse * material.diffuse;
    material.specular = light.specular * material.specular;

    // 光照颜色
    vec3 lighting_color = Flat_lighting(to_light, face_normal, material);

    // 最终颜色
    vec3 final_color = light.brightness * light.color * lighting_color;

    return final_color;
}

vec3 Flat_lighting(
    DirLight light, InternalMaterial material, Camera CSM_camera,
    vec3 camera_pos, vec3 face_pos, vec3 face_normal)
{
    return Flat_lighting(light, material, face_pos, face_normal);
}

vec3 CookTorrance_lighting(
    DirLight light, InternalMaterial material, Camera CSM_camera,
    vec3 camera_pos, vec3 frag_pos, vec3 frag_normal)
{
    // 基础向量
    vec3 to_light = -normalize(light.direction);
    vec3 to_camera = normalize(camera_pos - frag_pos);

    // 光照颜色
    vec3 lighting_color = CookTorrance_lighting(to_light, to_camera, frag_normal, material);

    // 最终颜色
    vec3 final_color = light.brightness * light.color * lighting_color;
    
    if (light.generate_shadows && material.recv_shadows && (light.depth_map_handle.x > 0 || light.depth_map_handle.y > 0))
    {
        float shadow_visibility = PCF(light, CSM_camera, frag_pos, frag_normal);
        final_color *= max(shadow_visibility, 0.1);
    }
    
    return final_color;
}

#endif