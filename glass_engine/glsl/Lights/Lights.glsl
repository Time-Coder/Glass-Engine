#include "DirLight.glsl"
#include "PointLight.glsl"
#include "SpotLight.glsl"

#if USE_SHADER_STORAGE_BLOCK

buffer DirLights
{
    int n_dir_lights;
    DirLight dir_lights[];
};

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

#else

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

#endif
