#version 460 core

in TexCoord
{
    vec2 tex_coord;
} fs_in;

out vec4 frag_color;

uniform sampler2D screen_image;
uniform vec4 background_color;

void main()
{ 
    frag_color = texture(screen_image, fs_in.tex_coord);
    frag_color = mix(background_color.a*background_color, frag_color, frag_color.a);
}