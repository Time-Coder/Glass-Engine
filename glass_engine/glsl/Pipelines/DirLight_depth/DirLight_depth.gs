#version 460 core

#extension GL_EXT_texture_array : require
#extension GL_ARB_bindless_texture : require

layout (triangles, invocations={CSM_levels}) in;
layout (triangle_strip, max_vertices=3) out;

in VertexOut
{
    vec3 world_pos;
    flat int visible;
} gs_in[];

out flat int visible;

#include "../../Lights/DirLight.glsl"

uniform DirLight dir_light;
uniform Camera camera;
uniform float explode_distance;

void main()
{
    vec3 v1 = gs_in[1].world_pos - gs_in[0].world_pos;
    vec3 v2 = gs_in[2].world_pos - gs_in[0].world_pos;
    vec3 face_world_normal = normalize(cross(v1, v2));

    gl_Layer = gl_InvocationID;
    for (int i = 0; i < 3; i++)
    {
        vec3 world_pos = gs_in[i].world_pos + explode_distance * face_world_normal;
        visible = gs_in[i].visible;
        
        gl_Position = world_to_lightNDC(dir_light, camera, gl_InvocationID, world_pos);
        EmitVertex();
    }
    
    EndPrimitive();
}