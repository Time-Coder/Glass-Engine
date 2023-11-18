#version 430 core

#if USE_BINDLESS_TEXTURE
#extension GL_ARB_bindless_texture : require
#endif
#extension GL_EXT_texture_array : require

layout (location = 0) in vec3 position;
layout (location = 1) in vec3 tex_coord;
layout (location = 2) in vec4 color;
layout (location = 3) in vec4 back_color;
layout (location = 4) in vec4 affine_transform_row0;
layout (location = 5) in vec4 affine_transform_row1;
layout (location = 6) in vec4 affine_transform_row2;
layout (location = 7) in int visible;

out VertexOut
{
    vec4 color;
    vec4 back_color;
    vec3 tex_coord;
    flat int visible;
} vs_out;

#include "../../include/transform.glsl"

void main()
{
    mat4 transform = transpose(mat4(
        affine_transform_row0,
        affine_transform_row1,
        affine_transform_row2,
        vec4(0, 0, 0, 1)
    ));

    vec3 world_pos = transform_apply(transform, position);
    gl_Position = vec4(world_pos, 1);

    vs_out.visible = visible;
    vs_out.color = color;
    vs_out.back_color = back_color;
    vs_out.tex_coord = tex_coord;
}