#version 460 core

#extension GL_EXT_texture_array : require

layout (location = 0) in vec3 position;

// instance
layout (location = 1) in vec4 col0;
layout (location = 2) in vec4 col1;
layout (location = 3) in vec4 col2;
layout (location = 4) in vec4 col3;
layout (location = 5) in int visible;

out flat int vertex_visible;

#include "../../include/Transform.glsl"

void main()
{
    mat4 transform = mat4(col0, col1, col2, col3);
    
    vec3 world_pos = transform_apply(transform, position);
    gl_Position = vec4(world_pos, 1);

    vertex_visible = visible;
}