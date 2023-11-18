#include "math.glsl"

#if USE_FOG

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

vec3 fog_apply(Fog fog, vec3 color, float distance)
{
    if (fog.extinction_density < 1E-6 && fog.inscattering_density < 1E-6)
        return color;

    float extinction = 1;
    float inscattering = 1;
    if (fog.mode == FOG_MODE_LINEAR)
    {
        extinction = max(0, 1 - fog.extinction_density*distance);
        inscattering = max(0, 1 - fog.inscattering_density*distance);
    }
    else if (fog.mode == FOG_MODE_EXP)
    {
        extinction = exp(-fog.extinction_density*distance);
        inscattering = exp(-fog.inscattering_density*distance);
    }
    else if (fog.mode == FOG_MODE_EXP2)
    {
        float d2 = distance*distance;
        extinction = exp(-fog.extinction_density*d2);
        inscattering = exp(-fog.inscattering_density*d2);
    }
    return color*extinction + fog.color * (1 - inscattering);
}

#endif