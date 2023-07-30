#version 460 core

in TexCoord
{
    vec2 tex_coord;
} fs_in;

out float frag_value;

uniform sampler2D screen_image;
uniform bool horizontal;

uniform uvec2 kernel_shape;
uniform vec2 sigma;

void main()
{
    float center_value = texture(screen_image, fs_in.tex_coord).r;
    if (center_value > 0.99)
    {
        frag_value = center_value;
        return;
    }

    vec2 tex_offset = 1.0 / textureSize(screen_image, 0);
    frag_value = 0;
    
    if(horizontal)
    {
        float double_sigma_x2 = 2*sigma.x*sigma.x;
        float t = fs_in.tex_coord.t;
        float weight_sum = 0;
        for(int j = 0; j < kernel_shape.x; j++)
        {
            float d = (j - 0.5*(kernel_shape.x-1))*tex_offset.x;
            float s = fs_in.tex_coord.s + d;
            float weight = exp(-d*d/double_sigma_x2);
            frag_value += weight * texture(screen_image, vec2(s, t)).r;
            weight_sum += weight;
        }
        frag_value /= weight_sum;
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
            frag_value += weight * texture(screen_image, vec2(s, t)).r;
            weight_sum += weight;
        }
        frag_value /= weight_sum;
    }
}