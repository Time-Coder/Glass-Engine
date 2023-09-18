#ifndef _SHADING_INFO_GLSL__
#define _SHADING_INFO_GLSL__

#include "Material.glsl"
#include "fog.glsl"
#include "background.glsl"

struct ShadingInfo
{
    vec4 color;
    vec3 preshading_color;
    Material material;

    Background background;
    sampler2D env_map;
    Fog fog;
    bool is_opaque_pass;
    bool is_sphere;

    mat3 view_TBN;
    vec3 view_pos;
    vec2 tex_coord;
    mat4 affine_transform;
    vec3 mesh_center;
};

struct PostShadingInfo
{
    InternalMaterial material;

    Background background;
    sampler2D env_map;
    Fog fog;
    bool is_sphere;

    vec3 world_pos;
    vec3 world_normal;
    vec3 env_center;
};

PostShadingInfo PostShadingInfo_create()
{
    InternalMaterial _internal_material;
    Fog _fog;
    Background _background = Background(
        samplerCube(uvec2(0)),
        sampler2D(uvec2(0)),
        vec4(0),
        float(0.0)
    );

    return PostShadingInfo(
        _internal_material,

        _background,
        sampler2D(uvec2(0)),
        _fog,
        false,

        vec3(0),
        vec3(0),
        vec3(0)
    );
}

#endif