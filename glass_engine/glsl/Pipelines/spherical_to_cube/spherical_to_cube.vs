#version 460 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 tex_coord;

out VertexOut
{
    vec3 world_pos;
    vec2 tex_coord;
} vs_out;

void main()
{
    vs_out.tex_coord = tex_coord;
    vs_out.world_pos = position;
    gl_Position = vec4(position, 1);
}