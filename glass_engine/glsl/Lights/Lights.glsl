#include "DirLight.glsl"
#include "PointLight.glsl"
#include "SpotLight.glsl"

uniform DirLights
{
    int n_dir_lights;
    DirLight dir_lights[32];
};

uniform PointLights
{
    int n_point_lights;
    PointLight point_lights[32];
};

uniform SpotLights
{
    int n_spot_lights;
    SpotLight spot_lights[32];
};
