#version 430 core

#if USE_BINDLESS_TEXTURE
#extension GL_ARB_bindless_texture : require
#endif
#extension GL_EXT_texture_array : require

in GeometryOut
{
    mat4 affine_transform;
    vec3 view_pos;
    mat3 view_TBN;
    vec3 tex_coord;
    vec4 color;
    vec4 back_color;
    flat int visible;
} fs_in;

in vec3 preshading_color;
in vec3 preshading_back_color;
in flat uvec2 env_map_handle;

layout(location=0) out vec4 out_color;
layout(location=1) out vec4 accum;
layout(location=2) out float reveal;
layout(location=3) out vec3 view_pos;
layout(location=4) out vec3 view_normal;

#include "../../include/OIT.glsl"
#include "../../include/shading_all.glsl"

uniform Material material;
uniform Material back_material;
uniform Camera camera;
uniform bool is_opaque_pass;
uniform bool is_sphere;
uniform vec3 mesh_center;

#if USE_FOG
uniform Fog fog;
#endif

uniform Background background;

#define CURRENT_MATERIAL (gl_FrontFacing ? material : back_material)

void main()
{
    if (fs_in.visible == 0)
    {
        discard;
    }

    ShadingInfo shading_info = ShadingInfo(
        (gl_FrontFacing ? fs_in.color : fs_in.back_color),
        (gl_FrontFacing ? preshading_color : preshading_back_color)
#if USE_DYNAMIC_ENV_MAPPING
        , sampler2D(env_map_handle)
#endif
        , is_opaque_pass, is_sphere, fs_in.view_TBN,
        fs_in.view_pos, fs_in.tex_coord.st, fs_in.affine_transform, mesh_center);
    
    out_color = shading_all(camera, background, CURRENT_MATERIAL
#if USE_FOG
    , fog
#endif
    , shading_info);

    if (is_opaque_pass)
    {
        view_pos = shading_info.view_pos;
        view_normal = shading_info.view_TBN[2];
    }

    if (!is_opaque_pass && out_color.a < 1)
    {
        get_OIT_info(out_color, accum, reveal);
        out_color = vec4(0);
    }
}