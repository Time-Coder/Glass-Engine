#version 460 core

in vec2 tex_coord;
out vec4 frag_color;

#include "../include/math.glsl"

uniform sampler2D screen_image;
uniform sampler2D bloom_image;

void main()
{ 
    vec4 src_color = texture(screen_image, tex_coord);
    vec4 bloom_color = texture(bloom_image, tex_coord);
    frag_color = mix(bloom_color, src_color, 0.9);
}