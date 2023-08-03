#version 460 core

#extension GL_ARB_bindless_texture : enable

in flat int visible;
in vec3 world_pos;

#include "../../Lights/SpotLight.glsl"

uniform SpotLight spot_light;

void main()
{
    if (visible == 0)
    {
        discard;
    }

    float distance_to_light = length(spot_light.abs_position - world_pos);
    gl_FragDepth = distance_to_light / spot_light.coverage;
}