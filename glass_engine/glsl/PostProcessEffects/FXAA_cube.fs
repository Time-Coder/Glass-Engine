#version 430 core

#extension GL_EXT_texture_array : require

in vec2 tex_coord;
out vec4 frag_color;

#include "../include/FXAA.glsl"

uniform samplerCube screen_image;

void main()
{
    frag_color = textureCubeFaceFXAA(screen_image, tex_coord, gl_Layer);
}