#version 430 core

#if USE_BINDLESS_TEXTURE
#extension GL_ARB_bindless_texture : require
#endif
#extension GL_EXT_texture_array : require

layout (triangles, invocations={CSM_levels}) in;
layout (triangle_strip, max_vertices=3) out;

in VertexOut
{
    vec4 color;
    vec4 back_color;
    vec3 tex_coord;
    flat int visible;
} gs_in[];

out GeometryOut
{
    vec4 color;
    vec4 back_color;
    vec3 tex_coord;
    flat int visible;
} gs_out;

#include "../../Lights/DirLight_shadow_mapping.glsl"
#include "../../include/Camera.glsl"

uniform DirLight dir_light;
uniform Camera camera;
uniform float explode_distance;

void main()
{
    vec3 v1 = gl_in[1].gl_Position.xyz - gl_in[0].gl_Position.xyz;
    vec3 v2 = gl_in[2].gl_Position.xyz - gl_in[0].gl_Position.xyz;
    vec3 face_world_normal = normalize(cross(v1, v2));

    gl_Layer = gl_InvocationID;
    for (int i = 0; i < 3; i++)
    {
        vec3 world_pos = gl_in[i].gl_Position.xyz + explode_distance * face_world_normal;
        gs_out.visible = gs_in[i].visible;
        gs_out.color = gs_in[i].color;
        gs_out.back_color = gs_in[i].back_color;
        gs_out.tex_coord = gs_in[i].tex_coord;
        
        gl_Position = world_to_lightNDC(dir_light, camera, gl_InvocationID, world_pos);
        EmitVertex();
    }
    
    EndPrimitive();
}