#version 460 core

#extension GL_ARB_bindless_texture : enable

layout (points, invocations=6) in;
layout (points, max_vertices=1) out;

in flat int vertex_visible[];
out flat int visible;
out vec3 world_pos;

#include "../../include/Camera.glsl"
#include "../../Lights/PointLight.glsl"

uniform PointLight point_light;

void main()
{
    gl_Layer = gl_InvocationID;
    Camera camera = cube_camera(gl_InvocationID, point_light.abs_position, 0.1, point_light.coverage);
    world_pos = gl_in[i].gl_Position.xyz;
    visible = vertex_visible[i];

    gl_Position = Camera_project(camera, world_pos);
    EmitVertex();
    EndPrimitive();
}