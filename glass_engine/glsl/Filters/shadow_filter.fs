#version 460 core

in TexCoord
{
    vec2 tex_coord;
} fs_in;

out vec2 frag_value;

uniform sampler2D screen_image;
uniform bool horizontal;

void main()
{
    vec2 center_value = texture(screen_image, fs_in.tex_coord).xy;
    float dev = center_value.y;
    float kernel_width = 20*min(dev, 1);
    if (kernel_width < 1)
    {
        frag_value = center_value;
        return;
    }
    float sigma = 0.3 * ((kernel_width-1)*0.5 - 1) + 0.8;
    float double_sigma2 = 2*sigma*sigma;

    vec2 tex_offset = 1.0 / textureSize(screen_image, 0);
    frag_value = vec2(0, dev);
    if(horizontal)
    {
        float t = fs_in.tex_coord.t;
        float weight_sum = 0;
        for(int j = 0; j < kernel_width; j++)
        {
            float d = (j - 0.5*(kernel_width-1))*tex_offset.x;
            float s = fs_in.tex_coord.s + d;
            float weight = exp(-d*d/double_sigma2);
            frag_value.x += weight * texture(screen_image, vec2(s, t)).r;
            weight_sum += weight;
        }
        frag_value.x /= weight_sum;
    }
    else
    {
        float s = fs_in.tex_coord.s;
        float weight_sum = 0;
        for(int i = 0; i < kernel_width; i++)
        {
            float d = (i - 0.5*(kernel_width-1))*tex_offset.y;
            float t = fs_in.tex_coord.t + d;
            float weight = exp(-d*d/double_sigma2);
            frag_value.x += weight * texture(screen_image, vec2(s, t)).r;
            weight_sum += weight;
        }
        frag_value.x /= weight_sum;
    }
}