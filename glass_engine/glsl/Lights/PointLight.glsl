#ifndef _POINT_LIGHT_GLSL__
#define _POINT_LIGHT_GLSL__

#include "../include/Material.glsl"
#include "../include/math.glsl"
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

    // 外参数
    vec3 abs_position;
};

vec3 Phong_lighting(
    PointLight light, InternalMaterial material,
    vec3 camera_pos, vec3 frag_pos, vec3 normal)
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

    // 光照颜色
    vec3 lighting_color = Phong_lighting(to_light, to_camera, normal, material);

    // 衰减
    float attenuation = 1.0 / (1 + light.K1 * d +  light.K2 * d2);

    // 最终颜色
    vec3 final_color = light.brightness * light.color * attenuation * lighting_color;

    return final_color;
}

vec3 PhongBlinn_lighting(
    PointLight light, InternalMaterial material,
    vec3 camera_pos, vec3 frag_pos, vec3 normal)
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

    // 光照颜色
    vec3 lighting_color = PhongBlinn_lighting(to_light, to_camera, normal, material);

    // 衰减
    float attenuation = 1.0 / (1 + light.K1 * d +  light.K2 * d2);

    // 最终颜色
    vec3 final_color = light.brightness * light.color * attenuation * lighting_color;

    return final_color;
}

vec3 Gouraud_lighting(
    PointLight light, InternalMaterial material,
    vec3 camera_pos, vec3 frag_pos, vec3 normal)
{
    return Phong_lighting(light, material, camera_pos, frag_pos, normal);
}

vec3 Flat_lighting(PointLight light, InternalMaterial material, vec3 to_light, vec3 face_normal)
{    
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

vec3 CookTorrance_lighting(
    PointLight light, InternalMaterial material,
    vec3 camera_pos, vec3 frag_pos, vec3 normal
)
{
    // 基础向量
    vec3 to_light = light.abs_position - frag_pos;
    float d2 = dot(to_light, to_light);
    if (d2 > 100)
    {
        return vec3(0, 0, 0);
    }
    float d = sqrt(d2);
    to_light = to_light / d;
    vec3 to_camera = normalize(camera_pos - frag_pos);

    // 光照颜色
    vec3 lighting_color = CookTorrance_lighting(to_light, to_camera, normal, material);

    // 衰减
    float attenuation = 1.0 / d2;

    // 最终颜色
    vec3 final_color = light.ambient * material.ambient + 
        light.brightness * light.color * attenuation * lighting_color;

    return final_color;
}

#endif