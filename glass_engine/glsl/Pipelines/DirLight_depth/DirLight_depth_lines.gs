#version 460 core

#extension GL_EXT_texture_array : require
#extension GL_ARB_bindless_texture : require

layout (lines, invocations={CSM_levels}) in;
layout (line_strip, max_vertices=2) out;

in VertexOut
{
    vec4 color;
    vec4 back_color;
    vec3 tex_coord;
    flat bool visible;
} gs_in[];

out GeometryOut
{
    vec4 color;
    vec4 back_color;
    vec3 tex_coord;
    flat bool visible;
} gs_out;

#include "../../Lights/DirLight.glsl"

uniform DirLight dir_light;
uniform Camera camera;

void main()
{
    gl_Layer = gl_InvocationID;
    for (int i = 0; i < 2; i++)
    {
        gs_out.visible = gs_in[i].visible;
        gs_out.color = gs_in[i].color;
        gs_out.back_color = gs_in[i].back_color;
        gs_out.tex_coord = gs_in[i].tex_coord;
        
        gl_Position = world_to_lightNDC(dir_light, camera, gl_InvocationID, gl_in[i].gl_Position.xyz);
        EmitVertex();
    }
    EndPrimitive();
}