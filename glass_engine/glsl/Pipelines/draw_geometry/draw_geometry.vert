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
    mat3 world_TBN;
    vec3 tex_coord;
    vec3 back_tex_coord;
    vec4 color;
    vec4 back_color;
    flat int visible;
} vs_out;

#include "../../include/transform.glsl"
#include "../../include/tex_coord.glsl"
#include "../../include/Camera.glsl"
#include "../../include/Material.glsl"

uniform Camera camera;
uniform Material material;
uniform Material back_material;

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
    vs_out.visible = visible;
    vs_out.world_TBN = transform_apply_to_TBN(transform, mat3(tangent, bitangent, normal));
    transform_tex_coord(material, back_material, tex_coord, vs_out.tex_coord, vs_out.back_tex_coord);

    gl_Position = vec4(transform_apply(transform, position), 1);
}