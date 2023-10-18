#ifndef _MINNAERT_GLSL__
#define _MINNAERT_GLSL__

#include "rim.glsl"
#include "../include/Material.glsl"

// refer to https://www.researchgate.net/publication/247923568_The_Lambertian_Assumption_and_Landsat_Data
// Smith J A , Lin T L , Ranson K J .The Lambertian Assumption and Landsat Data[J].Photogrammetric Engineering & Remote Sensing, 1980, 46(9).DOI: https://doi.org/10.1016/0031-0182(80)90065-6.
float Minnaert_diffuse(vec3 to_light, vec3 to_camera, vec3 normal, float roughness)
{
    float cos_to_light = dot(to_light, normal);
    float cos_to_camera = dot(to_camera, normal);

    return max(cos_to_light * pow(cos_to_light*cos_to_camera, roughness), 0.0);
}

vec3 Minnaert_lighting(
    vec3 to_light, vec3 to_camera, vec3 normal,
    InternalMaterial material)
{
    vec3 diffuse_color = material.diffuse * Minnaert_diffuse(to_light, to_camera, normal, material.roughness);
    vec3 rim_color = material.diffuse * rim(to_light, to_camera, normal, material.light_rim_power, material.rim_power);
    return material.shadow_visibility * diffuse_color + rim_color;
}

#endif