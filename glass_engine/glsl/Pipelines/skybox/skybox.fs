#version 460 core

out vec4 frag_color;
in vec3 tex_coord;

uniform samplerCube skybox_map;

void main()
{
    frag_color = texture(skybox_map, tex_coord);
}