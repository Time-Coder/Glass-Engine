#include "../include/Material.glsl"

float Fresnel_diffuse(vec3 to_camera, vec3 normal, float rim_power)
{
    float cos_to_camera = max(0, dot(to_camera, normal));
    return pow(1 - cos_to_camera, 1/(0.001 + rim_power));
}

vec3 Fresnel_lighting(vec3 to_light, vec3 to_camera, vec3 normal, InternalMaterial material)
{
    return material.diffuse * Fresnel_diffuse(to_camera, normal, material.rim_power);
}