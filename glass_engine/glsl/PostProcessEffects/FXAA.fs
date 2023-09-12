#version 460 core

#extension GL_EXT_texture_array : require

in TexCoord
{
    vec2 tex_coord;
} fs_in;

out vec4 frag_color;

#include "../include/FXAA.glsl"

uniform sampler2D screen_image;

void main()
{
    frag_color = textureColorFXAA(screen_image, fs_in.tex_coord);
}