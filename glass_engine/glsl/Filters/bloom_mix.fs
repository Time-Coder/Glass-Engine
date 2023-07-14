#version 460 core

in vec2 tex_coord;
out vec4 frag_color;

#include "../include/math.glsl"

uniform sampler2D screen_image;
uniform sampler2D bloom_image;
uniform sampler2D luminance_image;

uniform bool enable_bloom;
uniform bool enable_HDR;

void main()
{ 
    vec4 src_color = texture(screen_image, tex_coord);
    vec4 bloom_color = texture(bloom_image, tex_coord);

    frag_color = src_color;
    if (enable_bloom)
    {
        frag_color = mix(bloom_color, src_color, 0.9);
    }

    if (enable_HDR)
    {
        vec4 luminance_color = texture(luminance_image, tex_coord);
        float luma = luminance(luminance_color.rgb);
        frag_color = vec4(1.0) - exp(-frag_color / (0.5+sqrt(luma)/2));
        frag_color = sin(0.5*PI*frag_color);
    }
    
    frag_color.a = 1;
}