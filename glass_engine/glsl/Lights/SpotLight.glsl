#ifndef _SPOT_LIGHT_GLSL__
#define _SPOT_LIGHT_GLSL__

struct SpotLight
{
    // 内参数
    vec3 color;
    float rim_power;

    float half_span_angle_rad;
    float half_softness_rad;
    float aggregate_coeff;
    
    float K1; // 一次衰减系数
    float K2; // 二次衰减系数
    float coverage; // 覆盖范围
    bool generate_shadows; // 是否产生阴影
    uvec2 depth_map_handle;

    // 外参数
    vec3 abs_position;
    vec3 direction;
};

#endif