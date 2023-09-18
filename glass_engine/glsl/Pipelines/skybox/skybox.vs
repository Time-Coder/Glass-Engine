#version 460 core
layout (location = 0) in vec3 position;

out vec3 tex_coord;

#include "../../include/Camera.glsl"

uniform Camera camera;

void main()
{
    tex_coord = position;
    vec4 pos = Camera_project_skybox(camera, position);    
    gl_Position = pos.xyww;
}