#ifndef _POINT_LIGHT_GLSL__
#define _POINT_LIGHT_GLSL__

#include "../include/Material.glsl"
#include "../include/math.glsl"
#include "../include/Camera.glsl"
#include "../ShadingModels/Phong.glsl"
#include "../ShadingModels/PhongBlinn.glsl"
#include "../ShadingModels/Gouraud.glsl"
#include "../ShadingModels/Flat.glsl"
#include "../ShadingModels/CookTorrance.glsl"

struct PointLight
{
    // 内参数
    vec3 color;
    float brightness;
    vec3 ambient;
    vec3 diffuse;
    vec3 specular;

    float K1; // 一次衰减系数
    float K2; // 二次衰减系数
    float coverage; // 覆盖范围
    bool generate_shadows; // 是否产生阴影
    uvec2 depth_map_handle;

    // 外参数
    vec3 abs_position;
};

#include "PointLight_shadow_mapping.glsl"

vec3 PhongBlinn_lighting(
    PointLight light, InternalMaterial material,
    vec3 camera_pos, vec3 frag_pos, vec3 frag_normal)
{
    // 基础向量
    vec3 to_light = light.abs_position - frag_pos;
    float d2 = dot(to_light, to_light);
    if (d2 > light.coverage*light.coverage)
    {
        return vec3(0, 0, 0);
    }
    float d = sqrt(d2);
    to_light = to_light / d;
    vec3 to_camera = normalize(camera_pos - frag_pos);
    
    // 光照参数
    material.ambient = light.ambient * material.ambient;
    material.diffuse = light.diffuse * material.diffuse;
    material.specular = light.specular * material.specular;

    // 阴影
    if (light.generate_shadows && material.recv_shadows && (light.depth_map_handle.x > 0 || light.depth_map_handle.y > 0))
    {
        float shadow_visibility = PCF(light, frag_pos, frag_normal);
        material.diffuse *= shadow_visibility;
        material.specular *= shadow_visibility;
    }

    // 光照颜色
    vec3 lighting_color = PhongBlinn_lighting(to_light, to_camera, frag_normal, material);

    // 衰减
    float attenuation = 1.0 / (1 + light.K1 * d +  light.K2 * d2);

    // 最终颜色
    vec3 final_color = light.brightness * light.color * attenuation * lighting_color;

    return final_color;
}

vec3 PhongBlinn_lighting(
    PointLight light, InternalMaterial material, Camera CSM_camera,
    vec3 camera_pos, vec3 frag_pos, vec3 frag_normal)
{
    return PhongBlinn_lighting(light, material, camera_pos, frag_pos, frag_normal);
}

vec3 Phong_lighting(
    PointLight light, InternalMaterial material,
    vec3 camera_pos, vec3 frag_pos, vec3 frag_normal)
{
    // 基础向量
    vec3 to_light = light.abs_position - frag_pos;
    float d2 = dot(to_light, to_light);
    if (d2 > light.coverage*light.coverage)
    {
        return vec3(0, 0, 0);
    }
    float d = sqrt(d2);
    to_light = to_light / d;
    vec3 to_camera = normalize(camera_pos - frag_pos);
    
    // 光照参数
    material.ambient = light.ambient * material.ambient;
    material.diffuse = light.diffuse * material.diffuse;
    material.specular = light.specular * material.specular;

    // 阴影
    if (light.generate_shadows && material.recv_shadows && (light.depth_map_handle.x > 0 || light.depth_map_handle.y > 0))
    {
        float shadow_visibility = PCF(light, frag_pos, frag_normal);
        material.diffuse *= shadow_visibility;
        material.specular *= shadow_visibility;
    }

    // 光照颜色
    vec3 lighting_color = Phong_lighting(to_light, to_camera, frag_normal, material);

    // 衰减
    float attenuation = 1.0 / (1 + light.K1 * d +  light.K2 * d2);

    // 最终颜色
    vec3 final_color = light.brightness * light.color * attenuation * lighting_color;

    return final_color;
}

vec3 Phong_lighting(
    PointLight light, InternalMaterial material, Camera CSM_camera,
    vec3 camera_pos, vec3 frag_pos, vec3 frag_normal)
{
    return Phong_lighting(light, material, camera_pos, frag_pos, frag_normal);
}

vec3 Gouraud_lighting(
    PointLight light, InternalMaterial material,
    vec3 camera_pos, vec3 frag_pos, vec3 normal)
{
    return Phong_lighting(light, material, camera_pos, frag_pos, normal);
}

vec3 Gouraud_lighting(
    PointLight light, InternalMaterial material, Camera camera_CSM,
    vec3 camera_pos, vec3 frag_pos, vec3 normal)
{
    return Phong_lighting(light, material, camera_pos, frag_pos, normal);
}

vec3 Flat_lighting(
    PointLight light, InternalMaterial material,
    vec3 face_pos, vec3 face_normal)
{
    // 基础向量
    vec3 to_light = normalize(light.abs_position - face_pos);

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
    PointLight light, InternalMaterial material, Camera CSM_camera,
    vec3 camera_pos, vec3 face_pos, vec3 face_normal)
{
    return Flat_lighting(light, material, face_pos, face_normal);
}

vec3 CookTorrance_lighting(
    PointLight light, InternalMaterial material,
    vec3 camera_pos, vec3 frag_pos, vec3 frag_normal)
{
    // 基础向量
    vec3 to_light = light.abs_position - frag_pos;
    float d2 = dot(to_light, to_light);
    float d = sqrt(d2);
    to_light = to_light / d;
    vec3 to_camera = normalize(camera_pos - frag_pos);

    // 光照颜色
    vec3 lighting_color = CookTorrance_lighting(to_light, to_camera, frag_normal, material);

    // 衰减
    float attenuation = 1.0 / d2;

    // 最终颜色
    vec3 final_color = light.ambient * material.ambient + 
        light.brightness * light.color * attenuation * lighting_color;
    if (light.generate_shadows && material.recv_shadows && (light.depth_map_handle.x > 0 || light.depth_map_handle.y > 0))
    {
        float shadow_visibility = PCF(light, frag_pos, frag_normal);
        final_color *= max(1, shadow_visibility);
    }

    return final_color;
}

vec3 CookTorrance_lighting(
    PointLight light, InternalMaterial material, Camera CSM_camera,
    vec3 camera_pos, vec3 frag_pos, vec3 frag_normal)
{
    return CookTorrance_lighting(light, material, camera_pos, frag_pos, frag_normal);
}

#endif