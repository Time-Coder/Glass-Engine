#ifndef _LAMBERT_GLSL__
#define _LAMBERT_GLSL__

#include "rim.glsl"

float Lambert_diffuse(vec3 to_light, vec3 normal)
{
    return max(dot(to_light, normal), 0.0);
}

vec3 Lambert_lighting(
    vec3 to_light, vec3 to_camera, vec3 normal,
    InternalMaterial material)
{
    vec3 diffuse_color = material.diffuse * Lambert_diffuse(to_light, normal);
    vec3 rim_color = material.diffuse * rim(to_light, to_camera, normal, material.light_rim_power, material.rim_power);
    return material.shadow_visibility * diffuse_color + rim_color;
}

#endif