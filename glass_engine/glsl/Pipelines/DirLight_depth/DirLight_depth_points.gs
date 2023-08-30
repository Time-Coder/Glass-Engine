#version 460 core

#extension GL_EXT_texture_array : require
#extension GL_ARB_bindless_texture : require

layout (points, invocations={CSM_levels}) in;
layout (points, max_vertices=1) out;

in flat int vertex_visible[];
out flat int visible;

#include "../../Lights/DirLight.glsl"

uniform DirLight dir_light;
uniform Camera camera;

void main()
{
    gl_Layer = gl_InvocationID;
    visible = vertex_visible[0];
    
    gl_Position = world_to_lightNDC(dir_light, camera, gl_InvocationID, gl_in[0].gl_Position.xyz);
    EmitVertex();
    EndPrimitive();
}