#version 430 core

// vertex
layout (location = 0) in vec3 position;
layout (location = 1) in vec3 tangent;
layout (location = 2) in vec3 bitangent;
layout (location = 3) in vec3 normal;
layout (location = 4) in vec3 tex_coord;
layout (location = 5) in vec4 color;
layout (location = 6) in vec4 back_color;

// instance
layout (location = 7) in vec4 affine_transform_row0;
layout (location = 8) in vec4 affine_transform_row1;
layout (location = 9) in vec4 affine_transform_row2;
layout (location = 10) in int visible;

out VertexOut
{
    mat4 affine_transform;
    mat3 view_TBN;
    vec3 tex_coord;
    vec4 color;
    vec4 back_color;
    flat int visible;
} vs_out;

#include "../../include/transform.glsl"
#include "../../include/Camera.glsl"

uniform Camera camera;

void main()
{
    mat4 transform = transpose(mat4(
        affine_transform_row0,
        affine_transform_row1,
        affine_transform_row2,
        vec4(0, 0, 0, 1)
    ));

    vs_out.affine_transform = transform;
    vs_out.color = color;
    vs_out.back_color = back_color;
    vs_out.tex_coord = tex_coord;
    vs_out.visible = visible;
    mat3 world_TBN = mat3(tangent, bitangent, normal);
    world_TBN = transform_apply_to_TBN(transform, world_TBN);
    vs_out.view_TBN = world_TBN_to_view(camera, world_TBN);

    vec3 world_pos = transform_apply(transform, position);
    vec3 view_pos = world_to_view(camera, world_pos);
    gl_Position = vec4(view_pos, 1);
}