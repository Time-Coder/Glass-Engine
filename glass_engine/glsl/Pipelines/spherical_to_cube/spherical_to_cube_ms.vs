#version 460 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 tex_coord;

out vec2 frag_tex_coord;

#include "../../include/Camera.glsl"

uniform Camera cameras[6];
uniform int camera_index;

void main()
{
    frag_tex_coord = tex_coord;
    gl_Position = Camera_project_skydome(cameras[camera_index], position);
}