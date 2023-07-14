#version 460 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 tex_coord;

out vec2 frag_tex_coord;
out vec3 frag_pos;

#include "../../include/Camera.glsl"

uniform Camera camera;

void main()
{
    frag_tex_coord = tex_coord;
    
    vec4 pos = Camera_project_skydome(camera, position);
    gl_Position = pos.xyww;
}