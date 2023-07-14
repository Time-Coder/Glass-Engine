#version 460 core

in vec2 frag_tex_coord;
out vec4 frag_color;

uniform sampler2D spherical_map;

void main()
{
    vec4 frag_color = texture(spherical_map, frag_tex_coord);
}