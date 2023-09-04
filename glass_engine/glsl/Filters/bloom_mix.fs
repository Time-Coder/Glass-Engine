#version 460 core

in TexCoord
{
    vec2 tex_coord;
} fs_in;

out vec4 frag_color;

#include "../include/sampling.glsl"

uniform sampler2D screen_image;
uniform sampler2D bloom_image;

void main()
{ 
    vec4 src_color = textureColor(screen_image, fs_in.tex_coord);
    vec4 bloom_color = textureColor(bloom_image, fs_in.tex_coord);
    frag_color = mix(bloom_color, src_color, 0.9);
}