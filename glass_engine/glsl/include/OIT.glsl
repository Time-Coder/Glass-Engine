#include "limits.glsl"

float blend_weight1(float depth, float alpha)
{
    return alpha * max(1E-2, min(3E3, 10/(1E-5 + pow(abs(depth)/5, 2) + pow(abs(depth)/200, 6))));
}

float blend_weight2(float depth, float alpha)
{
    return alpha * max(1E-2, min(3E3, 10/(1E-5 + pow(abs(depth)/5, 3) + pow(abs(depth)/200, 6))));
}

float blend_weight3(float depth, float alpha)
{
    return alpha * max(1E-2, min(3E3, 10/(1E-5 + pow(abs(depth)/200, 4))));
}

float blend_weight4(float depth, float alpha)
{
    return alpha * max(1E-2, 3E3*pow(1-abs(depth), 3));
}

void get_OIT_info(vec4 out_color, out vec4 accum, out float reveal)
{
    float weight = blend_weight2(gl_FragCoord.z, out_color.a);
    accum = vec4(out_color.rgb * out_color.a, out_color.a) * weight;
    reveal = log(1-out_color.a);
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