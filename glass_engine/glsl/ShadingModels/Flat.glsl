#ifndef _FLAT_GLSL_
#define _FLAT_GLSL_

#include "../include/Material.glsl"

vec3 Flat_lighting(vec3 to_light, vec3 to_camera, vec3 normal, InternalMaterial material)
{
    vec3 diffuse_color = material.base_color * Lambert_diffuse(to_light, normal);
    vec3 rim_color = material.base_color * rim(to_light, to_camera, normal, material.light_rim_power, material.rim_power);
    return material.shadow_visibility*diffuse_color + rim_color;
}

#endif