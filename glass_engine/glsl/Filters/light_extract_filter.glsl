#include "../include/sampling.glsl"

uniform float threshold;

vec4 getColor(sampler2D screen_image, vec2 tex_coord)
{
    vec4 frag_color = textureColor(screen_image, tex_coord);
    float luminance = dot(vec3(0.2126, 0.7152, 0.0722), frag_color.rgb);
    float cutoff = soft_step(luminance - threshold, 0.1);
    frag_color = cutoff*frag_color;
    frag_color.a = 1;

    return frag_color;
}