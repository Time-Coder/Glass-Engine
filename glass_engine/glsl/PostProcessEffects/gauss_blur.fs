#version 430 core

in vec2 tex_coord;
out vec4 frag_color;

uniform sampler2D screen_image;
uniform bool horizontal;

uniform uvec2 kernel_shape;
uniform vec2 sigma;
uniform int channels;

void main()
{
    vec2 tex_offset = 1.0 / textureSize(screen_image, 0);
    frag_color = vec4(0);
    
    if (horizontal)
    {
        float double_sigma_x2 = 2*sigma.x*sigma.x;
        float t = tex_coord.t;
        float weight_sum = 0;
        for(int j = 0; j < kernel_shape.x; j++)
        {
            float dj = j - 0.5*(kernel_shape.x-1);
            float ds = dj*tex_offset.x;
            float s = tex_coord.s + ds;
            float weight = exp(-dj*dj/double_sigma_x2);
            vec4 current_value = max(textureLod(screen_image, vec2(s, t), 0), 0.0);
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
        float s = tex_coord.s;
        float weight_sum = 0;
        for(int i = 0; i < kernel_shape.y; i++)
        {
            float di = i - 0.5*(kernel_shape.y-1);
            float dt = di*tex_offset.y;
            float t = tex_coord.t + dt;
            float weight = exp(-di*di/double_sigma_y2);
            vec4 current_value = max(textureLod(screen_image, vec2(s, t), 0), 0.0);
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