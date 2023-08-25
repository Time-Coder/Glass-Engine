#ifndef _FOG_GLSL__
#define _FOG_GLSL__

#include "math.glsl"

#define FOG_MODE_LINEAR 9729
#define FOG_MODE_EXP 2048
#define FOG_MODE_EXP2 2049

struct Fog
{
    uint mode;
    vec3 color;
    float extinction_density;
    float inscattering_density;
};

vec3 fog_apply(Fog fog, vec3 color, vec3 camera_pos, vec3 frag_pos)
{
    if (fog.extinction_density < 1E-6 && fog.inscattering_density < 1E-6)
    {
        return color;
    }

    float d = length(frag_pos - camera_pos);
    float extinction = 1;
    float inscattering = 1;
    if (fog.mode == FOG_MODE_LINEAR)
    {
        extinction = max(0, 1 - fog.extinction_density*d);
        inscattering = max(0, 1 - fog.inscattering_density*d);
    }
    else if (fog.mode == FOG_MODE_EXP)
    {
        extinction = exp(-fog.extinction_density*d);
        inscattering = exp(-fog.inscattering_density*d);
    }
    else if (fog.mode == FOG_MODE_EXP2)
    {
        extinction = exp(-fog.extinction_density*d*d);
        inscattering = exp(-fog.inscattering_density*d*d);
    }
    return color*extinction + fog.color * (1 - inscattering);
}

#endif