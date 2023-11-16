#include "PointLight.glsl"
#include "DirLight.glsl"
#include "SpotLight.glsl"

buffer PointLights
{
    int n_point_lights;
    PointLight point_lights[];
};

buffer DirLights
{
    int n_dir_lights;
    DirLight dir_lights[];
};

buffer SpotLights
{
    int n_spot_lights;
    SpotLight spot_lights[];
};