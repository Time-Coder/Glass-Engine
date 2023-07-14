#ifndef _FLAT_GLSL__
#define _FLAT_GLSL__

#include "Phong.glsl"

vec3 Flat_lighting(
    vec3 to_light, vec3 normal,
    InternalMaterial material)
{
    vec3 diffuse_color = material.diffuse * Phong_diffuse(to_light, normal);
    return material.ambient + diffuse_color;
}

#endif