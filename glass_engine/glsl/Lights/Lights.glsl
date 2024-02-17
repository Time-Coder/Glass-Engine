#include "DirLight.glsl"
#include "PointLight.glsl"
#include "SpotLight.glsl"

buffer DirLights
{
    int n_dir_lights;
    DirLight dir_lights[];
}all_dir_lights;

buffer PointLights
{
    int n_point_lights;
    PointLight point_lights[];
};

buffer SpotLights
{
    int n_spot_lights;
    SpotLight spot_lights[];
};