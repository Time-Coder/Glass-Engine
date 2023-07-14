#ifndef _PHONG_GLSL__
#define _PHONG_GLSL__

#include "Material.glsl"

float Phong_diffuse(vec3 to_light, vec3 normal)
{
    return max(dot(to_light, normal), 0.0);
}

float Phong_specular(vec3 to_light, vec3 to_camera, vec3 normal, float shininess)
{
    vec3 reflect_dir = reflect(-to_light, normal);
    float cos_out = max(dot(reflect_dir, to_camera), 0.0);
    return pow(cos_out, shininess*128);
}

vec3 Phong_lighting(
    vec3 to_light, vec3 to_camera, vec3 normal,
    InternalMaterial material)
{
    vec3 diffuse_color = material.diffuse * Phong_diffuse(to_light, normal);
    vec3 specular_color = material.specular * Phong_specular(to_light, to_camera, normal, material.shininess);
    return material.ambient + diffuse_color + specular_color;
}

#endif