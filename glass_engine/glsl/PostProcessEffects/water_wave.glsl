#include "../include/sampling.glsl"

vec4 post_process(sampler2D screen_image, vec2 tex_coord)
{
    vec2 uv = tex_coord * 0.8 + 0.1;
    uv += cos(iTime*vec2(6.0, 7.0) + uv*10.0)*0.02;

    return textureColor(screen_image, uv);
}