#include "../include/quat.glsl"

struct DirLight
{
    vec3 color;
    bool generate_shadows;
    uvec2 depth_map_handle;
    float max_back_offset;
    float rim_power;
    vec3 direction;
    quat abs_orientation;
};