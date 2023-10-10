#version 430 core
layout (location = 0) in vec3 position;

out vec3 tex_coord;
out vec3 view_dir;

#include "../../include/Camera.glsl"

uniform Camera camera;

void main()
{
    tex_coord = position;
    vec3 world_dir = quat_apply(quat(cos45, -sin45, 0, 0), position);
	view_dir = world_dir_to_view(camera, world_dir);
    vec4 NDC = view_to_NDC(camera, view_dir, CAMERA_PROJECTION_PERSPECTIVE);
    
    gl_Position = NDC.xyww;
}