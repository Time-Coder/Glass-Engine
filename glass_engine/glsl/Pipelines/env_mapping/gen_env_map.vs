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
layout (location = 10) in uvec2 env_map_handle;
layout (location = 11) in int visible;

out VertexOut
{
    mat4 affine_transform;
    mat3 world_TBN;
    vec3 tex_coord;
    vec4 color;
    vec4 back_color;
    flat uvec2 env_map_handle;
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
    
    vs_out.affine_transform = transform;
    vs_out.color = color;
    vs_out.back_color = back_color;
    vs_out.tex_coord = tex_coord;
    mat3 TBN = mat3(tangent, bitangent, normal);
    vs_out.world_TBN = transform_apply_to_TBN(transform, TBN);
    vs_out.env_map_handle = env_map_handle;
    vs_out.visible = visible;
}