#version 430 core

#if USE_BINDLESS_TEXTURE
#extension GL_ARB_bindless_texture : require
#endif

layout (points, invocations=6) in;
layout (points, max_vertices=1) out;

in VertexOut
{
    vec4 color;
    vec4 back_color;
    vec3 tex_coord;
    flat int visible;
} gs_in[];

out GeometryOut
{
    vec3 world_pos;
    vec4 color;
    vec4 back_color;
    vec3 tex_coord;
    flat int visible;
} gs_out;

#include "../../Lights/SpotLight.glsl"
#include "../../include/Camera.glsl"

uniform SpotLight spot_light;

void main()
{
    gl_Layer = gl_InvocationID;
    Camera camera = cube_camera(gl_InvocationID, spot_light.abs_position, 0.1, spot_light.coverage);
    gs_out.world_pos = gl_in[0].gl_Position.xyz;
    gs_out.visible = gs_in[0].visible;
    gs_out.color = gs_in[0].color;
    gs_out.back_color = gs_in[0].back_color;
    gs_out.tex_coord = gs_in[0].tex_coord;

    gl_Position = Camera_project(camera, gs_out.world_pos);
    EmitVertex();
    EndPrimitive();
}