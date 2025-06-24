#ifndef _SHADINGINFO_GLSL_
#define _SHADINGINFO_GLSL_

#include "Material.glsl"
#include "background.glsl"

struct ShadingInfo
{
    vec4 color;
#if USE_DYNAMIC_ENV_MAPPING
    uvec2 env_map_handle;
#endif
    bool is_opaque_pass;
    bool is_sphere;
    mat3 world_TBN;
    vec3 world_pos;
    vec2 tex_coord;
    mat4 affine_transform;
    vec3 mesh_center;
};

struct PostShadingInfo
{
    InternalMaterial material;
#if USE_DYNAMIC_ENV_MAPPING
    uvec2 env_map_handle;
#endif
    bool is_sphere;
    vec3 world_pos;
    vec3 world_normal;
    vec3 env_center;
};


#endif