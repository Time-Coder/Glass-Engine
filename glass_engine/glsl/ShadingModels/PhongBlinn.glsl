#ifndef _PHONG_BLINN_GLSL__
#define _PHONG_BLINN_GLSL__

#include "Material.glsl"
#include "Phong.glsl"

float PhongBlinn_specular(vec3 to_light, vec3 to_camera, vec3 normal, float shininess)
{
    vec3 halfway_vec = normalize(to_light + to_camera);
    float cos_out = max(dot(halfway_vec, normal), 0.0);
    return pow(cos_out, shininess*128);
}

vec3 PhongBlinn_lighting(
    vec3 to_light, vec3 to_camera, vec3 normal,
    InternalMaterial material)
{
    vec3 diffuse_color = material.diffuse * Phong_diffuse(to_light, normal);
    vec3 specular_color = material.specular * PhongBlinn_specular(to_light, to_camera, normal, material.shininess);
    return material.ambient + diffuse_color + specular_color;
}

#endif