#version 430 core

in TexCoord
{
    vec2 tex_coord;
} fs_in;

out vec4 frag_color;

uniform sampler2D screen_image;
uniform sampler2D bloom_image;

void main()
{ 
    vec4 src_color = max(texture(screen_image, fs_in.tex_coord), 0.0);
    vec4 bloom_color = max(texture(bloom_image, fs_in.tex_coord), 0.0);
    frag_color = mix(bloom_color, src_color, 0.9);
}