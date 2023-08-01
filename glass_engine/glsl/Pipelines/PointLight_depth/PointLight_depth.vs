#version 460 core

#extension GL_EXT_texture_array : require

layout (location = 0) in vec3 position;

// instance
layout (location = 1) in vec3 abs_position;
layout (location = 2) in vec4 abs_orientation;
layout (location = 3) in vec3 abs_scale;
layout (location = 4) in int visible;

out flat int vertex_visible;

#include "../../include/Transform.glsl"

void main()
{
    Transform transform;
    transform.abs_position = abs_position;
    transform.abs_orientation = vec4_to_quat(abs_orientation);
    transform.abs_scale = abs_scale;

    vec3 world_pos = transform_apply(transform, position);
    gl_Position = vec4(world_pos, 1);

    vertex_visible = visible;
}