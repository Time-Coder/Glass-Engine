#version 430 core

in TexCoord
{
    vec2 tex_coord;
} fs_in;

out vec4 frag_color;

#include "../include/OIT.glsl"

uniform sampler2D accum_map;
uniform sampler2D reveal_map;

void main()
{
    vec4 accum = texture(accum_map, fs_in.tex_coord);
    float reveal = texture(reveal_map, fs_in.tex_coord).r;
    frag_color = blend_composite(accum, reveal);
}