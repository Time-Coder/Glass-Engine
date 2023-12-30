#version 430 core

#if USE_BINDLESS_TEXTURE
#extension GL_ARB_bindless_texture : require
#endif
#extension GL_EXT_texture_array : require

in VertexOut
{
    mat4 affine_transform;
    vec3 view_pos;
    mat3 view_TBN;
    vec3 tex_coord;
    vec4 color;
    flat int visible;
#if USE_BINDLESS_TEXTURE && USE_DYNAMIC_ENV_MAPPING
    flat uvec2 env_map_handle;
#endif

} fs_in;

layout(location=0) out vec4 out_color;
layout(location=1) out vec4 accum;
layout(location=2) out float reveal;
layout(location=3) out vec3 view_pos;
layout(location=4) out vec3 view_normal;

#include "../../include/Material.glsl"
#include "../../include/OIT.glsl"
#include "../../include/fog.glsl"
#include "../../include/shading_all.glsl"

uniform Material material;
uniform Camera camera;
uniform bool is_opaque_pass;
uniform vec3 mesh_center;

#if USE_FOG
uniform Fog fog;
#endif

uniform Background background;

void main()
{
    if (fs_in.visible == 0)
    {
        discard;
    }

    ShadingInfo shading_info;
    shading_info.color = fs_in.color;
#if USE_DYNAMIC_ENV_MAPPING
    shading_info.env_map_handle = fs_in.env_map_handle;
#endif
    shading_info.is_opaque_pass = is_opaque_pass;
    shading_info.is_sphere = false;
    shading_info.view_TBN = fs_in.view_TBN;
    shading_info.view_pos = fs_in.view_pos;
    shading_info.tex_coord = fs_in.tex_coord.st;
    shading_info.affine_transform = fs_in.affine_transform;
    shading_info.mesh_center = mesh_center;

    out_color = shading_all(camera, background, material
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