#ifndef _BACKGROUND_GLSL_
#define _BACKGROUND_GLSL_

struct Background
{
    samplerCube skybox_map;
    sampler2D skydome_map;
    vec4 color;
    float distance;
};

#endif