#version 430 core

layout (location = 0) in vec2 position;

out TexCoord
{
    vec2 tex_coord;
} vs_out;

void main()
{
    gl_Position = vec4(position.x, position.y, 0.0, 1.0); 
    vs_out.tex_coord = 0.5*(1 + position);
}