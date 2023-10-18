#version 430 core

#extension GL_EXT_texture_array : require

in TexCoord
{
    vec2 tex_coord;
} fs_in;

out vec4 frag_color;

#include "../include/FXAA.glsl"

uniform sampler2DArray screen_image;

void main()
{
    frag_color = textureFXAA(screen_image, vec3(fs_in.tex_coord, gl_Layer));
}