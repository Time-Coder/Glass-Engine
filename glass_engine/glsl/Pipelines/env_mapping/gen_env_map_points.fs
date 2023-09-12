#version 460 core

#extension GL_ARB_bindless_texture : require
#extension GL_EXT_texture_array : require

in GeometryOut
{
    mat4 affine_transform;
    vec3 view_pos;
    mat3 view_TBN;
    vec3 tex_coord;
    vec4 color;
    flat bool visible;
} fs_in;

in vec3 preshading_color;
in flat uvec2 env_map_handle;

layout(location=0) out vec4 out_color;
layout(location=1) out vec4 accum;
layout(location=2) out float reveal;

#include "../../include/Camera.glsl"
#include "../../include/Material.glsl"
#include "../../include/OIT.glsl"
#include "../../include/fog.glsl"
#include "../../include/shading_all.glsl"

uniform vec3 view_center;
uniform vec3 mesh_center;
uniform Material material;
uniform bool is_opaque_pass;
uniform Camera CSM_camera;
uniform Fog fog;
uniform samplerCube skybox_map;
uniform sampler2D skydome_map;

void main()
{
    if (!fs_in.visible)
    {
        discard;
    }

    Camera camera = cube_camera(gl_Layer, view_center);
    ShadingInfo shading_info = ShadingInfo(
        fs_in.color,
        preshading_color,
        material,
        
        skybox_map,
        skydome_map,
        (env_map_handle.x > 0 || env_map_handle.y > 0),
        sampler2D(env_map_handle),
        is_opaque_pass,
        false,

        fog,
        fs_in.view_TBN,
        fs_in.view_pos,
        fs_in.tex_coord.st,
        fs_in.affine_transform,
        mesh_center
    );
    out_color = shading_all(camera, CSM_camera, shading_info);
    
    // OIT
    if (!is_opaque_pass && out_color.a < 1)
    {
        get_OIT_info(out_color, accum, reveal);
        out_color = vec4(0);
    }
}