#version 430 core

#if USE_BINDLESS_TEXTURE
#extension GL_ARB_bindless_texture : require
#endif
#extension GL_EXT_texture_array : require

in GeometryOut
{
    mat4 affine_transform;
    vec3 world_pos;
    mat3 world_TBN;
    vec3 tex_coord;
    vec3 back_tex_coord;
    vec4 color;
    vec4 back_color;
    flat int visible;
} fs_in;

#if USE_BINDLESS_TEXTURE && USE_DYNAMIC_ENV_MAPPING
in flat uvec2 env_map_handle;
#endif

layout(location=0) out vec4 out_color;
layout(location=1) out vec4 accum;
layout(location=2) out float reveal;
layout(location=3) out vec3 world_pos;
layout(location=4) out vec3 world_normal;

#include "../../include/random.glsl"
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

void main()
{
    if (fs_in.visible == 0)
    {
        discard;
    }

    ShadingInfo shading_info;
    shading_info.color = (gl_FrontFacing ? fs_in.color : fs_in.back_color);
#if USE_DYNAMIC_ENV_MAPPING
    shading_info.env_map_handle = env_map_handle;
#endif
    shading_info.is_opaque_pass = is_opaque_pass;
    shading_info.is_sphere = is_sphere;
    shading_info.world_TBN = fs_in.world_TBN;
    shading_info.world_pos = fs_in.world_pos;
    shading_info.tex_coord = (gl_FrontFacing ? fs_in.tex_coord.st : fs_in.back_tex_coord.st);
    shading_info.affine_transform = fs_in.affine_transform;
    shading_info.mesh_center = mesh_center;

    if (gl_FrontFacing)
    {
        out_color = shading_all(camera, background, material
#if USE_FOG
        , fog
#endif
        , shading_info);
    }
    else
    {
        out_color = shading_all(camera, background, back_material
#if USE_FOG
        , fog
#endif
        , shading_info);
    }

    if (is_opaque_pass)
    {
        world_pos = shading_info.world_pos;
        world_normal = shading_info.world_TBN[2];
    }
    else if (out_color.a < 1 - 1E-6)
    {
        vec3 view_pos = world_to_view(camera, fs_in.world_pos);
        get_OIT_info(out_color, view_pos.y, accum, reveal);
        out_color = vec4(0);
    }
}