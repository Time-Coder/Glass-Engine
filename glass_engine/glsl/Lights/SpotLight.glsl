#ifndef _SPOT_LIGHT_GLSL__
#define _SPOT_LIGHT_GLSL__

#include "../include/Material.glsl"
#include "../include/Camera.glsl"
#include "../ShadingModels/lighting.glsl"

struct SpotLight
{
    // 内参数
    vec3 color;
    float brightness;
    vec3 ambient;
    vec3 diffuse;
    vec3 specular;
    float rim_power;

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

vec3 lighting(
    SpotLight light, InternalMaterial material,
    vec3 camera_pos, vec3 frag_pos, vec3 frag_normal)
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
    vec3 to_camera = normalize(camera_pos - frag_pos);

    material.ambient = light.ambient * material.ambient;
    material.diffuse = cutoff * light.aggregate_coeff * light.diffuse * material.diffuse;
    material.specular = cutoff * light.aggregate_coeff * light.specular * material.specular;
    material.light_rim_power = light.rim_power;

    if (light.generate_shadows && material.recv_shadows &&
        (light.depth_map_handle.x > 0 || light.depth_map_handle.y > 0))
    {
        float shadow_visibility = PCF(light, frag_pos, frag_normal);
        material.diffuse *= shadow_visibility;
        material.specular *= shadow_visibility;
    }

    vec3 lighting_color = lighting(to_light, to_camera, frag_normal, material);
    float attenuation = 1.0 / (1 + light.K1 * d +  light.K2 * d2);

    return light.brightness * light.color * attenuation * lighting_color;
}

vec3 get_ambient_diffuse(
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
    vec3 factor = Lambert_diffuse(to_light, frag_normal)*light.diffuse + 0.2*light.ambient;
    float attenuation = 1.0 / (1 + light.K1 * d +  light.K2 * d2);
    float shadow_visibility = 1;
    if (light.generate_shadows && recv_shadows &&
        (light.depth_map_handle.x > 0 || light.depth_map_handle.y > 0))
    {
        shadow_visibility = PCF(light, frag_pos, frag_normal);
    }

    return shadow_visibility * factor * light.brightness * light.color * attenuation;
}

vec3 get_specular(
    SpotLight light, InternalMaterial material,
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
    
    float specular_factor = 0;
    if (material.shading_model == SHADING_MODEL_PHONG)
    {
        specular_factor = Phong_specular(to_light, to_camera, frag_normal, material.shininess);
    }
    else if (material.shading_model == SHADING_MODEL_PHONG_BLINN)
    {
        specular_factor = PhongBlinn_specular(to_light, to_camera, frag_normal, material.shininess);
    }

    float attenuation = 1.0 / (1 + light.K1 * d +  light.K2 * d2);
    float shadow_visibility = 1;
    if (light.generate_shadows && material.recv_shadows &&
        (light.depth_map_handle.x > 0 || light.depth_map_handle.y > 0))
    {
        shadow_visibility = PCF(light, frag_pos, frag_normal);
    }
    
    return shadow_visibility * specular_factor * light.brightness * light.color * light.specular * attenuation;
}

#endif