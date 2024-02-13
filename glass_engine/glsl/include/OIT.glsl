#include "limits.glsl"

float blend_weight1(float abs_z)
{
    return clamp(10/(1E-5 + pow(abs_z/5, 2) + pow(abs_z/200, 6)), 1E-2, 3E3);
}

float blend_weight2(float abs_z)
{
    return clamp(10/(1E-5 + pow(abs_z/5, 3) + pow(abs_z/200, 6)), 1E-2, 3E3);
}

float blend_weight3(float abs_z)
{
    return clamp(10/(1E-5 + pow(abs_z/200, 4)), 1E-2, 3E3);
}

float blend_weight4(float dz)
{
    return max(1E-2, 3E3*pow(1 - dz, 3));
}

void get_OIT_info(vec4 out_color, float abs_z, out vec4 accum, out float reveal)
{
    float weight = out_color.a * blend_weight2(abs_z);
    accum = vec4(out_color.rgb*out_color.a, out_color.a) * weight;
    reveal = log(1 - out_color.a);
}

vec4 blend_composite(vec4 accum, float reveal)
{
    if (hasinf(accum.rgb))
    {
        accum.rgb = vec3(accum.a);
    }
    vec3 average_color = accum.rgb / max(accum.a, 1E-6);
    return vec4(average_color, exp(reveal));
}