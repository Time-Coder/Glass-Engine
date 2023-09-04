#version 460 core

#extension GL_EXT_texture_array : require

in TexCoord
{
    vec2 tex_coord;
} fs_in;

out vec4 frag_color;

#include "../include/sampling.glsl"

uniform sampler2D screen_image;
uniform sampler2DArray screen_image_array;
uniform int layer;
uniform int index;

uniform bool gray;
uniform bool invert;

void main()
{ 
    if (layer < 0)
    {
        frag_color = textureColor(screen_image, fs_in.tex_coord);
    }
    else
    {
        frag_color = textureColor(screen_image_array, vec3(fs_in.tex_coord, layer));
    }
    
    if (gray)
    {
        frag_color = vec4(vec3(frag_color[index]), 1);
    }
    if (invert)
    {
        frag_color.rgb = 1 - frag_color.rgb;
    }
}