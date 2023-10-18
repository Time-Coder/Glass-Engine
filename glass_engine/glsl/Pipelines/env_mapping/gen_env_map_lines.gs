#version 430 core

#ifdef USE_BINDLESS_TEXTURE
#extension GL_ARB_bindless_texture : require
#endif

#extension GL_EXT_texture_array : require

layout (lines, invocations=6) in;
layout (line_strip, max_vertices=2) out;

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
    vec3 world_bitangent = normalize(gl_in[1].gl_Position.xyz - gl_in[0].gl_Position.xyz);
    
    for (int i = 0; i < 2; i++)
    {
        gs_out.affine_transform = gs_in[i].affine_transform;
        vec3 world_pos = gl_in[i].gl_Position.xyz;
        vec3 to_camera = normalize(camera.abs_position - world_pos);
        vec3 world_tangent = normalize(cross(world_bitangent, to_camera));
        vec3 world_normal = normalize(cross(world_tangent, world_bitangent));

        gs_out.view_pos = world_to_view(camera, world_pos);
        gs_out.view_TBN = world_TBN_to_view(camera, mat3(world_tangent, world_bitangent, world_normal));
        gs_out.tex_coord = gs_in[i].tex_coord;
        gs_out.color = gs_in[i].color;
        gs_out.visible = gs_in[i].visible;
        env_map_handle = gs_in[i].env_map_handle;
        preshading_color = vec3(0);

        // pre shading
        if (material.shading_model == SHADING_MODEL_FLAT ||
            material.shading_model == SHADING_MODEL_GOURAUD)
        {
            InternalMaterial internal_material = fetch_internal_material(gs_in[i].color, material, gs_in[i].tex_coord.st);
            preshading_color = lighting(internal_material, CSM_camera, camera.abs_position, world_pos, world_normal);
        }
        
        gl_Position = view_to_NDC(camera, gs_out.view_pos);
        EmitVertex();
    }
    EndPrimitive();
}