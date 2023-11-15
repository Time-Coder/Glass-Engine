#version 430 core

in TexCoord
{
    vec2 tex_coord;
} fs_in;

out vec4 frag_color;

#include "../include/sampling.glsl"

uniform samplerCube screen_image;
uniform bool horizontal;

uniform uvec2 kernel_shape;
uniform vec2 sigma;
uniform int channels;

void main()
{
    vec2 tex_offset = 1.0 / textureSize(screen_image, 0).xy;
    frag_color = vec4(0);
    
    if (horizontal)
    {
        float double_sigma_x2 = 2*sigma.x*sigma.x;
        float t = fs_in.tex_coord.t;
        float weight_sum = 0;
        for(int j = 0; j < kernel_shape.x; j++)
        {
            float d = (j - 0.5*(kernel_shape.x-1))*tex_offset.x;
            float s = fs_in.tex_coord.s + d;
            float weight = exp(-d*d/double_sigma_x2);
            vec4 current_value = max(textureCubeFace(screen_image, vec2(s, t), gl_Layer), 0.0);
            if (channels == 1)
            {
                current_value.gb = current_value.rr;
                current_value.a = 1;
            }
            frag_color += weight * current_value;
            weight_sum += weight;
        }
        frag_color = frag_color / weight_sum;
    }
    else
    {
        float double_sigma_y2 = 2*sigma.y*sigma.y;
        float s = fs_in.tex_coord.s;
        float weight_sum = 0;
        for(int i = 0; i < kernel_shape.y; i++)
        {
            float d = (i - 0.5*(kernel_shape.y-1))*tex_offset.y;
            float t = fs_in.tex_coord.t + d;
            float weight = exp(-d*d/double_sigma_y2);
            vec4 current_value = max(textureCubeFace(screen_image, vec2(s, t), gl_Layer), 0.0);
            if (channels == 1)
            {
                current_value.gb = current_value.rr;
                current_value.a = 1;
            }
            frag_color += weight * current_value;
            weight_sum += weight;
        }
        frag_color = frag_color / weight_sum;
    }
}