#ifndef _SPOT_LIGHT_GLSL__
#define _SPOT_LIGHT_GLSL__

#include "../include/Material.glsl"
#include "../include/Camera.glsl"
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
    uvec2 depth_map_handle;

    // 外参数
    vec3 abs_position;
    vec3 direction;
};

#include "SpotLight_shadow_mapping.glsl"

vec3 ambient_diffuse_factor(
    SpotLight light, bool recv_shadows,
    vec3 frag_pos, vec3 frag_normal)
{
    vec3 to_light = light.abs_position - frag_pos;
    float d2 = dot(to_light, to_light);
    if(d2 > light.coverage*light.coverage)
    {
        return vec3(0, 0, 0);
    }
    float d = sqrt(d2);
    to_light = to_light / d;

    float theta = acos(dot(normalize(light.direction), -to_light));
    float cutoff = soft_step(light.half_span_angle_rad+light.half_softness_rad-theta, light.half_softness_rad);
    vec3 diffuse_factor = Lambert_diffuse(to_light, frag_normal) + 0.1*light.ambient;
    float attenuation = 1.0 / (1 + light.K1 * d +  light.K2 * d2);
    float shadow_visibility = 1;
    if (light.generate_shadows && recv_shadows &&
        (light.depth_map_handle.x > 0 || light.depth_map_handle.y > 0))
    {
        shadow_visibility = PCF(light, frag_pos, frag_normal);
    }

    return shadow_visibility * diffuse_factor * light.brightness * light.color * attenuation;
}

vec3 Phong_specular(
    SpotLight light, InternalMaterial material, Camera CSM_camera,
    vec3 view_dir, vec3 frag_pos, vec3 frag_normal)
{
    vec3 to_light = light.abs_position - frag_pos;
    float d2 = dot(to_light, to_light);
    if(d2 > light.coverage*light.coverage)
    {
        return vec3(0, 0, 0);
    }
    float d = sqrt(d2);
    to_light = to_light / d;
    vec3 to_camera = normalize(reflect(-view_dir, frag_normal));

    float theta = acos(dot(normalize(light.direction), -to_light));
    float cutoff = soft_step(light.half_span_angle_rad+light.half_softness_rad-theta, light.half_softness_rad);
    float specular_factor = Phong_specular(to_light, to_camera, frag_normal, material.shininess);
    float attenuation = 1.0 / (1 + light.K1 * d +  light.K2 * d2);
    float shadow_visibility = 1;
    if (light.generate_shadows && material.recv_shadows &&
        (light.depth_map_handle.x > 0 || light.depth_map_handle.y > 0))
    {
        shadow_visibility = PCF(light, frag_pos, frag_normal);
    }
    
    return shadow_visibility * specular_factor * light.brightness * light.color * attenuation;
}

vec3 Phong_lighting(
    SpotLight light, InternalMaterial material,
    vec3 camera_pos, vec3 frag_pos, vec3 frag_normal)
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
    vec3 to_camera = normalize(camera_pos - frag_pos);

    // 光照参数
    material.ambient = light.ambient * material.ambient;
    material.diffuse = cutoff * light.aggregate_coeff * light.diffuse * material.diffuse.rgb;
    material.specular = cutoff * light.aggregate_coeff * light.specular * material.specular;

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
    SpotLight light, InternalMaterial material, Camera CSM_camera,
    vec3 camera_pos, vec3 frag_pos, vec3 frag_normal)
{
    return Phong_lighting(light, material, camera_pos, frag_pos, frag_normal);
}

vec3 PhongBlinn_specular(
    SpotLight light, InternalMaterial material, Camera CSM_camera,
    vec3 view_dir, vec3 frag_pos, vec3 frag_normal)
{
    vec3 to_light = light.abs_position - frag_pos;
    float d2 = dot(to_light, to_light);
    if(d2 > light.coverage*light.coverage)
    {
        return vec3(0, 0, 0);
    }
    float d = sqrt(d2);
    to_light = to_light / d;
    vec3 to_camera = normalize(reflect(-view_dir, frag_normal));

    float theta = acos(dot(normalize(light.direction), -to_light));
    float cutoff = soft_step(light.half_span_angle_rad+light.half_softness_rad-theta, light.half_softness_rad);
    float specular_factor = PhongBlinn_specular(to_light, to_camera, frag_normal, material.shininess);
    float attenuation = 1.0 / (1 + light.K1 * d +  light.K2 * d2);
    float shadow_visibility = 1;
    if (light.generate_shadows && material.recv_shadows &&
        (light.depth_map_handle.x > 0 || light.depth_map_handle.y > 0))
    {
        shadow_visibility = PCF(light, frag_pos, frag_normal);
    }

    return shadow_visibility * specular_factor * light.brightness * light.color * attenuation;
}

vec3 PhongBlinn_lighting(
    SpotLight light, InternalMaterial material,
    vec3 camera_pos, vec3 frag_pos, vec3 frag_normal)
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
    
    vec3 to_camera = normalize(camera_pos - frag_pos);

    // 光照参数
    material.ambient = light.ambient * material.ambient;
    material.diffuse = cutoff * light.aggregate_coeff * light.diffuse * material.diffuse.rgb;
    material.specular = cutoff * light.aggregate_coeff * light.specular * material.specular;

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
    SpotLight light, InternalMaterial material, Camera CSM_camera,
    vec3 camera_pos, vec3 frag_pos, vec3 frag_normal)
{
    return PhongBlinn_lighting(light, material, camera_pos, frag_pos, frag_normal);
}

vec3 Flat_lighting(
    SpotLight light, InternalMaterial material,
    vec3 face_pos, vec3 face_normal)
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

vec3 Flat_lighting(
    SpotLight light, InternalMaterial material, Camera CSM_camera,
    vec3 camera_pos, vec3 face_pos, vec3 face_normal)
{
    return Flat_lighting(light, material, face_pos, face_normal);
}

vec3 Gouraud_lighting(
    SpotLight light, InternalMaterial material,
    vec3 camera_pos, vec3 vertex_pos, vec3 vertex_normal)
{
    return Phong_lighting(light, material, camera_pos, vertex_pos, vertex_normal);
}

vec3 Gouraud_lighting(
    SpotLight light, InternalMaterial material, Camera CSM_camera,
    vec3 camera_pos, vec3 vertex_pos, vec3 vertex_normal)
{
    return Phong_lighting(light, material, camera_pos, vertex_pos, vertex_normal);
}

vec3 CookTorrance_lighting(
    SpotLight light, InternalMaterial material,
    vec3 camera_pos, vec3 frag_pos, vec3 frag_normal)
{
    // 基础向量
    vec3 to_light = light.abs_position - frag_pos;
    float d2 = dot(to_light, to_light);

    // 角度限制
    float theta = acos(dot(light.direction, -to_light));
    float cutoff = soft_step(light.half_span_angle_rad+light.half_softness_rad-theta, light.half_softness_rad);

    float d = sqrt(d2);
    to_light = to_light / d;
    vec3 to_camera = normalize(camera_pos - frag_pos);

    // 光照颜色
    vec3 lighting_color = CookTorrance_lighting(to_light, to_camera, frag_normal, material);

    // 衰减
    float attenuation = 1.0 / d2;

    // 最终颜色
    vec3 final_color = light.ambient * material.ambient +
        cutoff * light.aggregate_coeff * light.brightness * light.color * attenuation * lighting_color;
    
    if (light.generate_shadows && material.recv_shadows && (light.depth_map_handle.x > 0 || light.depth_map_handle.y > 0))
    {
        float shadow_visibility = PCF(light, frag_pos, frag_normal);
        final_color *= max(1, shadow_visibility);
    }

    return final_color;
}

vec3 CookTorrance_lighting(
    SpotLight light, InternalMaterial material, Camera CSM_camera,
    vec3 camera_pos, vec3 frag_pos, vec3 frag_normal)
{
    return CookTorrance_lighting(light, material, camera_pos, frag_pos, frag_normal);
}

#endif