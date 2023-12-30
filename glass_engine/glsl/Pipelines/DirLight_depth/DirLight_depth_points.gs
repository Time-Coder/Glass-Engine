#version 430 core

#if USE_BINDLESS_TEXTURE
#extension GL_ARB_bindless_texture : require
#endif
#extension GL_EXT_texture_array : require

layout (points, invocations=CSM_LEVELS) in;
layout (points, max_vertices=1) out;

in VertexOut
{
    vec4 color;
    vec4 back_color;
    vec3 tex_coord;
    flat int visible;
} gs_in[];

out VertexOut
{
    vec4 color;
    vec4 back_color;
    vec3 tex_coord;
    flat int visible;
} gs_out;

#include "../../include/Camera.glsl"
#include "../../Lights/DirLight_shadow_mapping.glsl"

uniform DirLight dir_light;
uniform Camera camera;

void main()
{
    gl_Layer = gl_InvocationID;

    gs_out.visible = gs_in[0].visible;
    gs_out.color = gs_in[0].color;
    gs_out.back_color = gs_in[0].back_color;
    gs_out.tex_coord = gs_in[0].tex_coord;
    
    gl_Position = world_to_lightNDC(dir_light, camera, gl_InvocationID, gl_in[0].gl_Position.xyz);
    EmitVertex();
    EndPrimitive();
}