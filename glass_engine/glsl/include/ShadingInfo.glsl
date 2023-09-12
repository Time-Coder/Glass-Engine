#ifndef _SHADING_INFO_GLSL__
#define _SHADING_INFO_GLSL__

#include "Material.glsl"
#include "Fog.glsl"

struct ShadingInfo
{
    vec4 color;
    vec3 preshading_color;
    Material material;

    samplerCube skybox_map;
    sampler2D skydome_map;
    sampler2D env_map;
    bool is_opaque_pass;
    bool is_sphere;
    Fog fog;

    mat3 view_TBN;
    vec3 view_pos;
    vec2 tex_coord;
    mat4 affine_transform;
    vec3 mesh_center;
};

struct PostShadingInfo
{
    InternalMaterial material;

    samplerCube skybox_map;
    sampler2D skydome_map;
    sampler2D env_map;
    bool is_sphere;
    Fog fog;

    vec3 world_pos;
    vec3 world_normal;
    vec3 env_center;
};

PostShadingInfo PostShadingInfo_create()
{
    InternalMaterial _internal_material;
    Fog _fog;

    return PostShadingInfo(
        _internal_material,

        samplerCube(uvec2(0)),
        sampler2D(uvec2(0)),
        sampler2D(uvec2(0)),
        false,
        _fog,

        vec3(0),
        vec3(0),
        vec3(0)
    );
}

#endif