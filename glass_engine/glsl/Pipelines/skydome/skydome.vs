#version 430 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 tex_coord;

out vec2 frag_tex_coord;
out vec3 view_dir;

#include "../../include/Camera.glsl"

uniform Camera camera;

void main()
{
    frag_tex_coord = tex_coord;
    view_dir = world_dir_to_view(camera, position);
	vec4 NDC = view_to_NDC(camera, view_dir, CAMERA_PROJECTION_PERSPECTIVE);
    
    gl_Position = NDC.xyww;
}