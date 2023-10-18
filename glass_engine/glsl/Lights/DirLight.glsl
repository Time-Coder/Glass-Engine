#ifndef _DIR_LIGHT_GLSL__
#define _DIR_LIGHT_GLSL__

#include "../include/quat.glsl"

struct DirLight
{
    // 内参数
    vec3 color;
    bool generate_shadows; // 是否产生阴影
    uvec2 depth_map_handle;
    float max_back_offset;
    float rim_power;

    // 外参数
    vec3 direction;
    quat abs_orientation;
};

#endif