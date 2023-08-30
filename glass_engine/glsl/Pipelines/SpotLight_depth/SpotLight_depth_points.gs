#version 460 core

#extension GL_ARB_bindless_texture : enable

layout (points, invocations=6) in;
layout (points, max_vertices=1) out;

in flat int vertex_visible[];
out flat int visible;
out vec3 world_pos;

#include "../../include/Camera.glsl"
#include "../../Lights/SpotLight.glsl"

uniform SpotLight spot_light;

void main()
{
    gl_Layer = gl_InvocationID;
    Camera camera = cube_camera(gl_InvocationID, spot_light.abs_position, 0.1, spot_light.coverage);
    world_pos = gl_in[0].gl_Position.xyz;
    visible = vertex_visible[0];

    gl_Position = Camera_project(camera, world_pos);
    EmitVertex();
    EndPrimitive();
}