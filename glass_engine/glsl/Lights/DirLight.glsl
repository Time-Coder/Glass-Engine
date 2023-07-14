#ifndef _DIR_LIGHT_GLSL__
#define _DIR_LIGHT_GLSL__

#include "../include/Material.glsl"
#include "../include/math.glsl"
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

    // 外参数
    vec3 direction;
};

vec3 Phong_lighting(
    DirLight light, InternalMaterial material,
    vec3 camera_pos, vec3 frag_pos, vec3 normal)
{
    // 基础向量
    vec3 to_light = -normalize(light.direction);
    vec3 to_camera = normalize(camera_pos - frag_pos);

    // 光照参数
    material.ambient = light.ambient * material.ambient;
    material.diffuse = light.diffuse * material.diffuse;
    material.specular = light.specular * material.specular;

    // 光照颜色
    vec3 lighting_color = Phong_lighting(to_light, to_camera, normal, material);

    // 最终颜色
    vec3 final_color = light.brightness * light.color * lighting_color;
    
    return final_color;
}

vec3 PhongBlinn_lighting(
    DirLight light, InternalMaterial material,
    vec3 camera_pos, vec3 frag_pos, vec3 normal)
{
    // 基础向量
    vec3 to_light = -normalize(light.direction);
    vec3 to_camera = normalize(camera_pos - frag_pos);

    // 光照参数
    material.ambient = light.ambient * material.ambient;
    material.diffuse = light.diffuse * material.diffuse;
    material.specular = light.specular * material.specular;

    // 光照颜色
    vec3 lighting_color = PhongBlinn_lighting(to_light, to_camera, normal, material);

    // 最终颜色
    vec3 final_color = light.brightness * light.color * lighting_color;
    
    return final_color;
}

vec3 Gouraud_lighting(
    DirLight light, InternalMaterial material,
    vec3 camera_pos, vec3 frag_pos, vec3 normal)
{
    return Phong_lighting(light, material, camera_pos, frag_pos, normal);
}

vec3 Flat_lighting(DirLight light, InternalMaterial material, vec3 to_light, vec3 face_normal)
{
    to_light = -normalize(light.direction);
    
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
    DirLight light, InternalMaterial material,
    vec3 camera_pos, vec3 frag_pos, vec3 normal)
{
    // 基础向量
    vec3 to_light = -normalize(light.direction);
    vec3 to_camera = normalize(camera_pos - frag_pos);

    // 光照颜色
    vec3 lighting_color = CookTorrance_lighting(to_light, to_camera, normal, material);

    // 最终颜色
    vec3 final_color = light.brightness * light.color * lighting_color;
    
    return final_color;
}

#endif