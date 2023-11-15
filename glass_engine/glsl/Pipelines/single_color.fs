#version 430 core

layout(location=0) out vec4 out_color;
layout(location=1) out vec4 accum;
layout(location=2) out float reveal;

#include "../include/OIT.glsl"

uniform vec4 color;

void main()
{
    out_color = color;
    if (out_color.a < 1)
        get_OIT_info(out_color, accum, reveal);
}