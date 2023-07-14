#version 460 core

layout (triangles) in;
layout (triangle_strip, max_vertices=18) out;

in VertexOut
{
    vec3 world_pos;
    vec2 tex_coord;
} gs_in[];

out vec2 frag_tex_coord;

#include "../../include/Camera.glsl"
uniform Camera cameras[6];

void main()
{
    for(int face = 0; face < 6; face++)
    {
        gl_Layer = face;
        for(int i = 0; i < 3; i++)
        {
            frag_tex_coord = gs_in[i].tex_coord;
            gl_Position = Camera_project_skydome(cameras[face], gs_in[i].world_pos);

            EmitVertex();
        }
        EndPrimitive();
    }
}