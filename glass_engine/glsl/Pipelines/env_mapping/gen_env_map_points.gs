#version 430 core

#if USE_BINDLESS_TEXTURE
#extension GL_ARB_bindless_texture : require
#endif
#extension GL_EXT_texture_array : require

layout (points, invocations=6) in;
layout (points, max_vertices=1) out;

in VertexOut
{
    mat4 affine_transform;
    vec3 tex_coord;
    vec4 color;
    flat uvec2 env_map_handle;
    flat int visible;
} gs_in[];

out GeometryOut
{
    mat4 affine_transform;
    vec3 view_pos;
    mat3 view_TBN;
    vec3 tex_coord;
    vec4 color;
    flat int visible;
} gs_out;

out vec3 preshading_color;
out flat uvec2 env_map_handle;

#include "../../include/transform.glsl"
#include "../../include/Camera.glsl"
#include "../../include/InternalMaterial.glsl"
#include "../../Lights/Lights_lighting.glsl"

uniform vec3 view_center;
uniform Material material;
uniform Camera CSM_camera;

void main()
{
    gl_Layer = gl_InvocationID;
    Camera camera = cube_camera(gl_InvocationID, view_center);
    
    gs_out.affine_transform = gs_in[0].affine_transform;
    vec3 world_pos = gl_in[0].gl_Position.xyz;
    vec3 world_normal = normalize(camera.abs_position - world_pos);
    gs_out.view_pos = world_to_view(camera, world_pos);
    gs_out.view_TBN = mat3(vec3(1,0,0), vec3(0,0,1), normalize(-gs_out.view_pos));
    gs_out.tex_coord = gs_in[0].tex_coord;
    gs_out.color = gs_in[0].color;
    gs_out.visible = gs_in[0].visible;
    env_map_handle = gs_in[0].env_map_handle;
    preshading_color = vec3(0);

#if USE_SHADING_MODEL_FLAT || USE_SHADING_MODEL_GOURAUD
    if (material.shading_model == SHADING_MODEL_FLAT ||
        material.shading_model == SHADING_MODEL_GOURAUD)
    {
        InternalMaterial internal_material = fetch_internal_material(gs_in[0].color, material, gs_in[0].tex_coord.st);
        preshading_color = lighting(internal_material, CSM_camera, camera.abs_position, world_pos, world_normal);
    }
#endif

    gl_Position = view_to_NDC(camera, gs_out.view_pos);
    EmitVertex();
    EndPrimitive();
}