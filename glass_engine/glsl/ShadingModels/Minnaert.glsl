#ifndef _MINNAERT_GLSL__
#define _MINNAERT_GLSL__

#include "rim.glsl"

float Minnaert_diffuse(vec3 to_light, vec3 to_camera, vec3 normal, float roughness)
{
    float cos_to_light = max(0, dot(to_light, normal));
    float cos_to_camera = max(0, dot(to_camera, normal));
    return cos_to_camera * pow(cos_to_light*cos_to_camera, roughness);
}

vec3 Minnaert_lighting(
    vec3 to_light, vec3 to_camera, vec3 normal,
    InternalMaterial material)
{
    vec3 diffuse_color = material.diffuse * Minnaert_diffuse(to_light, to_camera, normal, material.roughness);
    vec3 rim_color = material.diffuse * rim(to_light, to_camera, normal, material.light_rim_power, material.rim_power);
    return material.ambient + material.shadow_visibility * diffuse_color + rim_color;
}

#endif