struct SpotLight
{
    vec3 color;
    float rim_power;
    float half_span_angle_rad;
    float half_softness_rad;
    float aggregate_coeff;
    float K1;
    float K2;
    float coverage;
    bool generate_shadows;
    uvec2 depth_map_handle;
    vec3 abs_position;
    vec3 direction;
};