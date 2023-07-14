#version 460 core

in vec2 frag_tex_coord;
out vec4 frag_color;

#include "../../include/math.glsl"

uniform sampler2D skydome_map;

void main()
{
    frag_color = textureLod(skydome_map, frag_tex_coord, 0);
}