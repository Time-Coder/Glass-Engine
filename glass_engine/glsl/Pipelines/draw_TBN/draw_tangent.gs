#version 430 core

layout (triangles) in;
layout (line_strip, max_vertices = 6) out;

in VertexOut
{
    vec3 view_pos;
    vec3 view_normal;
} gs_in[];

#include "../../include/Camera.glsl"

uniform float tangent_scale;
uniform float explode_distance;
uniform Camera camera;

void main()
{
    vec3 v1 = gs_in[1].view_pos - gs_in[0].view_pos;
    vec3 v2 = gs_in[2].view_pos - gs_in[0].view_pos;
    vec3 face_view_normal = normalize(cross(v1, v2));

    for (int i = 0; i < 3; i++)
    {
        gl_Position = view_to_NDC(camera, gs_in[i].view_pos + explode_distance*face_view_normal);
        EmitVertex();

        vec3 view_tangent = gs_in[i].view_TBN[0];
        gl_Position = view_to_NDC(camera, gs_in[i].view_pos + explode_distance*face_view_normal + tangent_scale*view_tangent);
        EmitVertex();
        EndPrimitive();
    }
}