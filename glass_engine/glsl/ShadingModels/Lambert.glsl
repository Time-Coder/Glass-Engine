#ifndef _LAMBERT_GLSL__
#define _LAMBERT_GLSL__

float Lambert_diffuse(vec3 to_light, vec3 normal)
{
    return max(dot(to_light, normal), 0.0);
}

#endif