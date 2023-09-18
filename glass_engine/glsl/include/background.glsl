#ifndef _BACKGROUND_GLSL__
#define _BACKGROUND_GLSL__

struct Background
{
    samplerCube skybox_map;
    sampler2D skydome_map;
    vec4 color;
    float distance;
};

#endif