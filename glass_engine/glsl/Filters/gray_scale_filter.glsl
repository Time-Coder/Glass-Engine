uniform vec3 weight;

#include "../include/sampling.glsl"

vec4 getColor(sampler2D screen_image, vec2 tex_coord)
{
    vec4 frag_color = textureColor(screen_image, tex_coord);
    float average = weight.x * frag_color.r + weight.y * frag_color.g + weight.z * frag_color.b;
    return vec4(average, average, average, frag_color.a);
}