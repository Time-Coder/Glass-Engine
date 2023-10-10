#version 430 core

layout (triangles, invocations={layers}) in;
layout (triangle_strip, max_vertices=3) out;

in TexCoord
{
    vec2 tex_coord;
} gs_in[];

out TexCoord
{
    vec2 tex_coord;
} gs_out;

void main()
{
    gl_Layer = gl_InvocationID;
    for (int i = 0; i < 3; i++)
    {
        gl_Position = gl_in[i].gl_Position;
        gs_out.tex_coord = gs_in[i].tex_coord;
        EmitVertex();
    }
    
    EndPrimitive();
}