#include "../include/sampling.glsl"

float triWave(float x)
{
    return(abs(mod(x-10.0, 20.0)-10.0)+1.0);
}

vec4 getColor(sampler2D screen_image, vec2 tex_coord)
{
    vec2 uv = 2.0*(tex_coord-0.5);

    vec2 uvR = uv*(1.0-length(uv)/(triWave(iTime*5.0)));
    vec2 uvG = uv*(1.0-length(uv)/(triWave(iTime*5.0+0.1)));
    vec2 uvB = uv*(1.0-length(uv)/(triWave(iTime*5.0+0.2)));

    uvR = uvR/2.0 + 0.5;
    uvG = uvG/2.0 + 0.5;
    uvB = uvB/2.0 + 0.5;

    float R = textureColor(screen_image, uvR).r;
    float G = textureColor(screen_image, uvG).g;
    float B = textureColor(screen_image, uvB).b;

    return vec4(R, G, B, 1.0);
}