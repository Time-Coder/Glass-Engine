struct PointLight
{
    vec3 color;
    float rim_power;
    float K1;
    float K2;
    float coverage;
    bool generate_shadows;
    uvec2 depth_map_handle;
    vec3 abs_position;
};