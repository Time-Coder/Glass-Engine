#version 430 core

#if USE_BINDLESS_TEXTURE
#extension GL_ARB_bindless_texture : require
#endif
#extension GL_EXT_texture_array : require

layout (triangles) in;
layout (triangle_strip, max_vertices = 3) out;

in VertexOut
{
    mat4 affine_transform;
    mat3 world_TBN;
    vec3 tex_coord;
    vec3 back_tex_coord;
    vec4 color;
    vec4 back_color;

#if USE_BINDLESS_TEXTURE && USE_DYNAMIC_ENV_MAPPING
    flat uvec2 env_map_handle;
#endif

    flat int visible;
} gs_in[];

out GeometryOut
{
    mat4 affine_transform;
    vec3 world_pos;
    mat3 world_TBN;
    vec3 tex_coord;
    vec3 back_tex_coord;
    vec4 color;
    vec4 back_color;
    flat int visible;
} gs_out;

#if USE_BINDLESS_TEXTURE && USE_DYNAMIC_ENV_MAPPING
out flat uvec2 env_map_handle;
#endif

#include "../../include/random.glsl"
#include "../../include/Camera.glsl"
#include "../../include/InternalMaterial.glsl"
#include "../../Lights/Lights_lighting.glsl"
#include "../../include/sampling.glsl"
#include "../../include/limits.glsl"
#include "../../include/transform.glsl"

uniform Camera camera;
uniform Material material;
uniform Material back_material;

mat3 choose_good_TBN(int index, mat3 backup_TBN)
{
    if (!hasnan(gs_in[index].world_TBN) &&
        length(gs_in[index].world_TBN[0]) > 1E-6 &&
        length(gs_in[index].world_TBN[1]) > 1E-6 &&
        length(gs_in[index].world_TBN[2]) > 1E-6)
    {
        return gs_in[index].world_TBN;
    }

    for (int i = 0; i < 3; i++)
    {
        if (i != index &&
            !hasnan(gs_in[i].world_TBN) &&
            length(gs_in[i].world_TBN[0]) > 1E-6 &&
            length(gs_in[i].world_TBN[1]) > 1E-6 &&
            length(gs_in[i].world_TBN[2]) > 1E-6)
        {
            return gs_in[i].world_TBN;
        }
    }

    return backup_TBN;
}

void main()
{
    vec3 v01 = gl_in[1].gl_Position.xyz - gl_in[0].gl_Position.xyz;
    vec3 v02 = gl_in[2].gl_Position.xyz - gl_in[0].gl_Position.xyz;
    vec3 face_world_normal = normalize(cross(v01, v02));
    vec2 face_tex_coord = (gs_in[0].tex_coord.xy + gs_in[1].tex_coord.xy + gs_in[2].tex_coord.xy)/3;
    vec3 face_world_pos = (gl_in[0].gl_Position.xyz + gl_in[1].gl_Position.xyz + gl_in[2].gl_Position.xyz)/3;
    vec4 face_color = (gs_in[0].color + gs_in[1].color + gs_in[2].color)/3;
    vec4 face_back_color = (gs_in[0].back_color + gs_in[1].back_color + gs_in[2].back_color)/3;
    vec2 st01 = gs_in[1].tex_coord.st - gs_in[0].tex_coord.st;
    vec2 st02 = gs_in[2].tex_coord.st - gs_in[0].tex_coord.st;
    float det = st01.s * st02.t - st02.s * st01.t;
    vec3 face_world_tangent = st02.t*v01 - st01.t*v02;
    vec3 face_world_bitangent = st01.s*v02 - st02.s*v01;
    if (abs(det) > 1E-6)
    {
        face_world_tangent /= det;
        face_world_bitangent /= det;
    }
    else
    {
        face_world_tangent = vec3(0);
        face_world_bitangent = vec3(0);
    }

    for (int i = 0; i < 3; i++)
    {
        gs_out.affine_transform = gs_in[i].affine_transform;
        gs_out.world_pos = gl_in[i].gl_Position.xyz;
        mat3 backup_world_TBN = mat3(face_world_tangent, face_world_bitangent, face_world_normal);

#if USE_SHADING_MODEL_FLAT
        if (material.shading_model == SHADING_MODEL_FLAT)
        {
            gs_out.world_TBN = backup_world_TBN;
        }
        else
        {
#endif
            gs_out.world_TBN = choose_good_TBN(i, backup_world_TBN);
#if USE_SHADING_MODEL_FLAT
        }
#endif
        gs_out.tex_coord = gs_in[i].tex_coord;
        gs_out.back_tex_coord = gs_in[i].back_tex_coord;
        gs_out.color = gs_in[i].color;
        gs_out.back_color = gs_in[i].back_color;
        gs_out.visible = gs_in[i].visible;

#if USE_BINDLESS_TEXTURE && USE_DYNAMIC_ENV_MAPPING
        env_map_handle = gs_in[i].env_map_handle;
#endif

#if USE_SHADING_MODEL_FLAT
        if (material.shading_model == SHADING_MODEL_FLAT)
        {
            InternalMaterial internal_material = fetch_internal_material(face_color, material, face_tex_coord);
            gs_out.color = vec4(lighting(internal_material, camera, camera.abs_position, face_world_pos, face_world_normal), 1.0);
        }

        if (back_material.shading_model == SHADING_MODEL_FLAT)
        {
            InternalMaterial internal_material = fetch_internal_material(face_back_color, back_material, face_tex_coord);
            gs_out.back_color = vec4(lighting(internal_material, camera, camera.abs_position, face_world_pos, -face_world_normal), 1.0);
        }
#endif

#if USE_SHADING_MODEL_GOURAUD
        if (material.shading_model == SHADING_MODEL_GOURAUD ||
            back_material.shading_model == SHADING_MODEL_GOURAUD)
        {
            if (material.shading_model == SHADING_MODEL_GOURAUD)
            {
                InternalMaterial internal_material = fetch_internal_material(gs_out.color, material, gs_out.tex_coord.xy);
                gs_out.color = vec4(lighting(internal_material, camera, camera.abs_position, gs_out.world_pos, gs_out.world_TBN[2]), 1.0);
            }
            if (back_material.shading_model == SHADING_MODEL_GOURAUD)
            {
                InternalMaterial internal_material = fetch_internal_material(gs_out.back_color, back_material, gs_out.tex_coord.xy);
                gs_out.back_color = vec4(lighting(internal_material, camera, camera.abs_position, gs_out.world_pos, -gs_out.world_TBN[2]), 1.0);
            }
        }
#endif

        gl_Position = Camera_project(camera, gs_out.world_pos);
        EmitVertex();
    }
    EndPrimitive();
}