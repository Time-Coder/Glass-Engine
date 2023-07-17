#version 460 core

#extension GL_ARB_bindless_texture : require

layout (triangles) in;
layout (triangle_strip, max_vertices = 3) out;

in VertexOut
{
    vec3 view_pos;
    mat3 view_TBN;
    vec3 tex_coord;
    vec4 color;
    vec4 back_color;
    flat int env_map_index;
    flat bool visible;
} gs_in[];

out GeometryOut
{
    vec3 view_pos;
    mat3 view_TBN;
    vec3 tex_coord;
    vec4 color;
    vec4 back_color;
    flat bool visible;
} gs_out;

out PreShadingColors
{
    vec3 Gouraud_color;
    vec3 Gouraud_back_color;
    flat vec3 Flat_color;
    flat vec3 Flat_back_color;
} pre_shading_colors;

out flat int env_map_index;
out vec4 NDC;

#include "../../include/Camera.glsl"
#include "../../include/Material.glsl"
#include "../../Lights/Lights.glsl"
#include "../../include/sampling.glsl"

uniform float explode_distance;
uniform Camera camera;
uniform Material material;
uniform Material back_material;
uniform bool is_filled;
uniform bool use_skydome_map;
uniform sampler2D skydome_map;

buffer BindlessSampler2Ds
{
    int n_bindless_sampler2Ds;
    sampler2D bindless_sampler2Ds[];
};

void main()
{
    vec3 v1 = gs_in[1].view_pos - gs_in[0].view_pos;
    vec3 v2 = gs_in[2].view_pos - gs_in[0].view_pos;
    vec3 face_view_normal = normalize(cross(v1, v2));
    vec3 face_world_normal = view_dir_to_world(camera, face_view_normal);

    vec2 face_tex_coord = (gs_in[0].tex_coord.xy + gs_in[1].tex_coord.xy + gs_in[2].tex_coord.xy)/3;
    vec3 face_view_pos = (gs_in[0].view_pos + gs_in[1].view_pos + gs_in[2].view_pos)/3 + explode_distance * face_view_normal;
    vec3 face_world_pos = view_to_world(camera, face_view_pos);
    vec4 face_color = (gs_in[0].color + gs_in[1].color + gs_in[2].color)/3;
    vec4 face_back_color = (gs_in[0].back_color + gs_in[1].back_color + gs_in[2].back_color)/3;

    for (int i = 0; i < 3; i++)
    {
        gs_out.view_pos = gs_in[i].view_pos + explode_distance * face_view_normal;
        gs_out.view_TBN = gs_in[i].view_TBN;
        gs_out.color = gs_in[i].color;
        gs_out.back_color = gs_in[i].back_color;
        gs_out.tex_coord = gs_in[i].tex_coord;
        gs_out.visible = gs_in[i].visible;

        env_map_index = gs_in[i].env_map_index;

        pre_shading_colors.Gouraud_color = vec3(0, 0, 0);
        pre_shading_colors.Gouraud_back_color = vec3(0, 0, 0);
        pre_shading_colors.Flat_color = vec3(0, 0, 0);
        pre_shading_colors.Flat_back_color = vec3(0, 0, 0);

        // pre lighting
        if (is_filled)
        {
            if (material.shading_model == 1) // Flat
            {
                InternalMaterial internal_material = fetch_internal_material(face_color, material, face_tex_coord);
                FLAT_LIGHTING(pre_shading_colors.Flat_color, internal_material, face_world_pos, face_world_normal);
            }

            if (material.shading_model == 2) // Gouraud
            {
                vec3 vertex_world_pos = view_to_world(camera, gs_out.view_pos);
                vec3 vertex_world_normal = view_dir_to_world(camera, gs_out.view_TBN[2]);
                InternalMaterial internal_material = fetch_internal_material(gs_out.color, material, gs_out.tex_coord.xy);
                GOURAUD_LIGHTING(pre_shading_colors.Gouraud_color, internal_material, camera.abs_position, vertex_world_pos, vertex_world_normal);
            }

            if (back_material.shading_model == 1) // Flat
            {
                InternalMaterial internal_material = fetch_internal_material(face_back_color, back_material, face_tex_coord);
                FLAT_LIGHTING(pre_shading_colors.Flat_back_color, internal_material, face_world_pos, -face_world_normal);
            }

            if (back_material.shading_model == 2) // Gouraud
            {
                vec3 vertex_world_pos = view_to_world(camera, gs_out.view_pos);
                vec3 vertex_world_normal = view_dir_to_world(camera, gs_out.view_TBN[2]);
                InternalMaterial internal_material = fetch_internal_material(gs_out.back_color, back_material, gs_out.tex_coord.xy);
                GOURAUD_LIGHTING(pre_shading_colors.Gouraud_back_color, internal_material, camera.abs_position, vertex_world_pos, -vertex_world_normal);
            }
        }

        NDC = view_to_NDC(camera, gs_out.view_pos);
        gl_Position = NDC;
        EmitVertex();
    }

    EndPrimitive();
}