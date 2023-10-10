#version 430 core

layout (location = 0) in vec2 position;

out vec2 tex_coord;

void main()
{
    gl_Position = vec4(position.x, position.y, 0.0, 1.0); 
    tex_coord = 0.5*(1 + position);
}