#version 460 core

#extension GL_ARB_gpu_shader_int64 : require
#extension GL_EXT_texture_array : require

layout (location = 0) in vec3 position;

// instance
layout (location = 1) in vec3 abs_position;
layout (location = 2) in vec4 abs_orientation;
layout (location = 3) in vec3 abs_scale;
layout (location = 4) in int visible;

out VertexOut
{
    vec3 world_pos;
    int visible;
} vs_out;

#include "../../Lights/DirLight.glsl"
#include "../../include/Transform.glsl"

uniform DirLight dir_light;

void main()
{
    Transform transform;
    transform.abs_position = abs_position;
    transform.abs_orientation = vec4_to_quat(abs_orientation);
    transform.abs_scale = abs_scale;

    vs_out.world_pos = transform_apply(transform, position);
    gl_Position = vec4(vs_out.world_pos, 1);

    vs_out.visible = visible;
}