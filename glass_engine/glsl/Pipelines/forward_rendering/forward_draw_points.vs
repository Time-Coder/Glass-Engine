#version 430 core

#if USE_BINDLESS_TEXTURE
#extension GL_ARB_bindless_texture : require
#endif
#extension GL_EXT_texture_array : enable

// vertex
layout (location = 0) in vec3 position;
layout (location = 1) in vec3 tex_coord;
layout (location = 2) in vec4 color;

// instance
layout (location = 3) in vec4 affine_transform_row0;
layout (location = 4) in vec4 affine_transform_row1;
layout (location = 5) in vec4 affine_transform_row2;
layout (location = 6) in uvec2 env_map_handle;
layout (location = 7) in int visible;

out VertexOut
{
    mat4 affine_transform;
    vec3 view_pos;
    mat3 view_TBN;
    vec3 tex_coord;
    vec4 color;
    flat int visible;
    vec3 preshading_color;
    flat uvec2 env_map_handle;
} vs_out;

#include "../../include/transform.glsl"
#include "../../include/Camera.glsl"
#include "../../include/InternalMaterial.glsl"
#include "../../Lights/Lights_lighting.glsl"

uniform Camera camera;
uniform Material material;

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
    vs_out.tex_coord = tex_coord;
    vec3 world_pos = transform_apply(transform, position);
    vec3 world_normal = normalize(camera.abs_position - world_pos);
    vs_out.view_pos = world_to_view(camera, world_pos);
    vs_out.view_TBN = mat3(vec3(1,0,0), vec3(0,0,1), normalize(-vs_out.view_pos));
    vs_out.env_map_handle = env_map_handle;
    vs_out.visible = visible;
    gl_Position = view_to_NDC(camera, vs_out.view_pos);

#if USE_SHADING_MODEL_FLAT || USE_SHADING_MODEL_GOURAUD
    if (material.shading_model == SHADING_MODEL_FLAT ||
        material.shading_model == SHADING_MODEL_GOURAUD)
    {
        InternalMaterial internal_material = fetch_internal_material(color, material, tex_coord.st);
        vs_out.preshading_color = lighting(internal_material, camera, camera.abs_position, world_pos, world_normal);
    }
#endif
}