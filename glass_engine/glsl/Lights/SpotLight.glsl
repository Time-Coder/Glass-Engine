#ifndef _SPOT_LIGHT_GLSL__
#define _SPOT_LIGHT_GLSL__

#include "../include/Material.glsl"
#include "../include/math.glsl"
#include "../ShadingModels/Phong.glsl"
#include "../ShadingModels/PhongBlinn.glsl"
#include "../ShadingModels/Gouraud.glsl"
#include "../ShadingModels/Flat.glsl"
#include "../ShadingModels/CookTorrance.glsl"

struct SpotLight
{
    // 内参数
    vec3 color;
    float brightness;
    vec3 ambient;
    vec3 diffuse;
    vec3 specular;

    float half_span_angle_rad;
    float half_softness_rad;
    float aggregate_coeff;
    
    float K1; // 一次衰减系数
    float K2; // 二次衰减系数
    float coverage; // 覆盖范围
    bool generate_shadows; // 是否产生阴影

    // 外参数
    vec3 abs_position;
    vec3 direction;
};

vec3 Phong_lighting(
    SpotLight light, InternalMaterial material,
    Camera camera, vec3 frag_pos, vec3 normal)
{
    // 基础向量
    vec3 to_light = light.abs_position - frag_pos;
    float d2 = dot(to_light, to_light);
    if(d2 > light.coverage*light.coverage)
    {
        return vec3(0, 0, 0);
    }
    float d = sqrt(d2);
    to_light = to_light / d;

    // 角度限制
    float theta = acos(dot(normalize(light.direction), -to_light));
    float cutoff = soft_step(light.half_span_angle_rad+light.half_softness_rad-theta, light.half_softness_rad);
    vec3 to_camera = normalize(camera.abs_position - frag_pos);

    // 光照参数
    material.ambient = light.ambient * material.ambient;
    material.diffuse = cutoff * light.aggregate_coeff * light.diffuse * material.diffuse.rgb;
    material.specular = cutoff * light.aggregate_coeff * light.specular * material.specular;

    // 光照颜色
    vec3 lighting_color = Phong_lighting(to_light, to_camera, normal, material);

    // 衰减
    float attenuation = 1.0 / (1 + light.K1 * d +  light.K2 * d2);

    // 最终颜色
    vec3 final_color = light.brightness * light.color * attenuation * lighting_color;
    
    return final_color;
}

vec3 PhongBlinn_lighting(
    SpotLight light, InternalMaterial material,
    Camera camera, vec3 frag_pos, vec3 normal)
{
    // 基础向量
    vec3 to_light = light.abs_position - frag_pos;
    float d2 = dot(to_light, to_light);
    if(d2 > light.coverage*light.coverage)
    {
        return vec3(0, 0, 0);
    }
    float d = sqrt(d2);
    to_light = to_light / d;

    // 角度限制
    float theta = acos(dot(normalize(light.direction), -to_light));
    float cutoff = soft_step(light.half_span_angle_rad+light.half_softness_rad-theta, light.half_softness_rad);
    
    vec3 to_camera = normalize(camera.abs_position - frag_pos);

    // 光照参数
    material.ambient = light.ambient * material.ambient;
    material.diffuse = cutoff * light.aggregate_coeff * light.diffuse * material.diffuse.rgb;
    material.specular = cutoff * light.aggregate_coeff * light.specular * material.specular;

    // 光照颜色
    vec3 lighting_color = PhongBlinn_lighting(to_light, to_camera, normal, material);

    // 衰减
    float attenuation = 1.0 / (1 + light.K1 * d +  light.K2 * d2);

    // 最终颜色
    vec3 final_color = light.brightness * light.color * attenuation * lighting_color;
    
    return final_color;
}

vec3 Flat_lighting(
    SpotLight light, InternalMaterial material,
    Camera camera, vec3 face_pos, vec3 face_normal)
{
    // 基础向量
    vec3 to_light = normalize(light.abs_position - face_pos);

    // 角度限制
    float theta = acos(dot(normalize(light.direction), -to_light));
    float cutoff = soft_step(light.half_span_angle_rad+light.half_softness_rad-theta, light.half_softness_rad);

    // 光照参数
    material.ambient = light.ambient * material.ambient;
    material.diffuse = cutoff * light.aggregate_coeff * light.diffuse * material.diffuse.rgb;
    material.specular = cutoff * light.aggregate_coeff * light.specular * material.specular;

    // 光照颜色
    vec3 lighting_color = Flat_lighting(to_light, face_normal, material);

    // 最终颜色
    vec3 final_color = light.brightness * light.color * lighting_color;

    return final_color;
}

vec3 Gouraud_lighting(
    SpotLight light, InternalMaterial material,
    Camera camera, vec3 frag_pos, vec3 normal)
{
    return Phong_lighting(light, material, camera, frag_pos, normal);
}

vec3 CookTorrance_lighting(
    SpotLight light, InternalMaterial material,
    Camera camera, vec3 frag_pos, vec3 normal)
{
    // 基础向量
    vec3 to_light = light.abs_position - frag_pos;
    float d2 = dot(to_light, to_light);
    if(d2 > 100)
    {
        return vec3(0, 0, 0);
    }

    // 角度限制
    float theta = acos(dot(light.direction, -to_light));
    float cutoff = soft_step(light.half_span_angle_rad+light.half_softness_rad-theta, light.half_softness_rad);

    float d = sqrt(d2);
    to_light = to_light / d;
    vec3 to_camera = normalize(camera.abs_position - frag_pos);

    // 光照颜色
    vec3 lighting_color = CookTorrance_lighting(to_light, to_camera, normal, material);

    // 衰减
    float attenuation = 1.0 / d2;

    // 最终颜色
    vec3 final_color = light.ambient * material.ambient +
        cutoff * light.aggregate_coeff * light.brightness * light.color * attenuation * lighting_color;
    
    return final_color;
}

#endif