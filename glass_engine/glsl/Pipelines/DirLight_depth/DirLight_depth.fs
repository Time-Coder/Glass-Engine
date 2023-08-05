#version 460 core

in flat int visible;
layout(location=0) out vec4 moments;

#include "../../include/math.glsl"

void main()
{
    if (visible == 0)
    {
        discard;
    }

    float depth = 2*gl_FragCoord.z-1;
    moments[0] = legendre_eval(depth, 1);
    moments[1] = legendre_eval(depth, 2);
    moments[2] = legendre_eval(depth, 3);
    moments[3] = legendre_eval(depth, 4);
}