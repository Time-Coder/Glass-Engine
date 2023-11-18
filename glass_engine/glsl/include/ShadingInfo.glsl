#include "Material.glsl"
#include "background.glsl"

struct ShadingInfo
{
    vec4 color;
    vec3 preshading_color;
#if USE_DYNAMIC_ENV_MAPPING
    sampler2D env_map;
#endif
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
#if USE_DYNAMIC_ENV_MAPPING
    sampler2D env_map;
#endif
    bool is_sphere;
    vec3 world_pos;
    vec3 world_normal;
    vec3 env_center;
};

PostShadingInfo PostShadingInfo_create()
{
    InternalMaterial _internal_material;
    return PostShadingInfo(_internal_material
#if USE_DYNAMIC_ENV_MAPPING
    , sampler2D(uvec2(0))
#endif
    , false, vec3(0), vec3(0), vec3(0));
}