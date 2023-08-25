#version 460 core
layout (location = 0) in vec3 position;

out vec3 tex_coord;
out vec3 world_coord;

#include "../../include/Camera.glsl"

uniform Camera camera;

void main()
{
    tex_coord = position;
    vec4 pos = Camera_project_skybox(camera, position);
    world_coord = camera.far * quat_apply(quat(cos45, -sin45, 0, 0), position);
    
    gl_Position = pos.xyww;
}