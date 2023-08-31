#version 460 core

#extension GL_EXT_texture_array : require
#extension GL_ARB_bindless_texture : require

layout (lines, invocations={CSM_levels}) in;
layout (line_strip, max_vertices=2) out;

in flat int vertex_visible[];
out flat int visible;

#include "../../Lights/DirLight.glsl"

uniform DirLight dir_light;
uniform Camera camera;

void main()
{
    gl_Layer = gl_InvocationID;
    for (int i = 0; i < 2; i++)
    {
        visible = vertex_visible[i];
        
        gl_Position = world_to_lightNDC(dir_light, camera, gl_InvocationID, gl_in[i].gl_Position.xyz);
        EmitVertex();
    }
    EndPrimitive();
}