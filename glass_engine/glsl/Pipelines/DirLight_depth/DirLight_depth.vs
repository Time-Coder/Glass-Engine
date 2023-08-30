#version 460 core

#extension GL_EXT_texture_array : require
#extension GL_ARB_bindless_texture : require

layout (location = 0) in vec3 position;

// instance
layout (location = 1) in dvec4 affine_transform_row0;
layout (location = 2) in dvec4 affine_transform_row1;
layout (location = 3) in dvec4 affine_transform_row2;
layout (location = 4) in int visible;

out flat int vertex_visible;

#include "../../include/transform.glsl"

void main()
{
    dmat4 dtransform = dmat4(affine_transform_row0,
                             affine_transform_row1,
                             affine_transform_row2,
                             dvec4(0, 0, 0, 1));
    mat4 transform = transpose(mat4(dtransform));

    vec3 world_pos = transform_apply(transform, position);
    gl_Position = vec4(world_pos, 1);

    vertex_visible = visible;
}