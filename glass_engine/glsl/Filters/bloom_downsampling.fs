#version 460 core

in vec2 tex_coord;
out vec4 frag_color;

uniform sampler2D screen_image;
uniform int mip_level;

#include "../include/math.glsl"

float first_weight(vec4 color, float max_value)
{
    float factor = max_value-1;
    float luma = dot(color.rgb, vec3(0.2126, 0.7152, 0.0722)) * 0.25;
    float weight = luma;
    if (luma > 1)
    {
        weight = 1 + factor*tanh((luma-1)/factor);
    }
    return weight/luma;
}

void main()
{
    vec2 tex_offset = 1.0 / textureSize(screen_image, 0);
    float dx = tex_offset.x;
    float dy = tex_offset.y;

    // Take 13 samples around current texel:
    // a - b - c
    // - j - k -
    // d - e - f
    // - l - m -
    // g - h - i
    // === ('e' is the current texel) ===
    vec4 a = texture(screen_image, vec2(tex_coord.x - 2*dx, tex_coord.y + 2*dy));
    vec4 b = texture(screen_image, vec2(tex_coord.x,        tex_coord.y + 2*dy));
    vec4 c = texture(screen_image, vec2(tex_coord.x + 2*dx, tex_coord.y + 2*dy));

    vec4 d = texture(screen_image, vec2(tex_coord.x - 2*dx, tex_coord.y));
    vec4 e = texture(screen_image, vec2(tex_coord.x,        tex_coord.y));
    vec4 f = texture(screen_image, vec2(tex_coord.x + 2*dx, tex_coord.y));

    vec4 g = texture(screen_image, vec2(tex_coord.x - 2*dx, tex_coord.y - 2*dy));
    vec4 h = texture(screen_image, vec2(tex_coord.x,        tex_coord.y - 2*dy));
    vec4 i = texture(screen_image, vec2(tex_coord.x + 2*dx, tex_coord.y - 2*dy));

    vec4 j = texture(screen_image, vec2(tex_coord.x - dx, tex_coord.y + dy));
    vec4 k = texture(screen_image, vec2(tex_coord.x + dx, tex_coord.y + dy));
    vec4 l = texture(screen_image, vec2(tex_coord.x - dx, tex_coord.y - dy));
    vec4 m = texture(screen_image, vec2(tex_coord.x + dx, tex_coord.y - dy));

    if (mip_level == 0)
    {
        float w_a = first_weight(a, 10);
        float w_b = first_weight(b, 10);
        float w_c = first_weight(c, 10);
        float w_d = first_weight(d, 10);
        float w_e = first_weight(e, 10);
        float w_f = first_weight(f, 10);
        float w_g = first_weight(g, 10);
        float w_h = first_weight(h, 10);
        float w_i = first_weight(i, 10);
        float w_j = first_weight(j, 10);
        float w_k = first_weight(k, 10);
        float w_l = first_weight(l, 10);
        float w_m = first_weight(m, 10);

        frag_color = w_e*e*0.125;
        frag_color += (w_a*a+w_c*c+w_g*g+w_i*i)*0.03125;
        frag_color += (w_b*b+w_d*d+w_f*f+w_h*h)*0.0625;
        frag_color += (w_j*j+w_k*k+w_l*l+w_m*m)*0.125;

        float weight_sum = w_e*0.125;
        weight_sum += (w_a+w_c+w_g+w_i)*0.03125;
        weight_sum += (w_b+w_d+w_f+w_h)*0.0625;
        weight_sum += (w_j+w_k+w_l+w_m)*0.125;

        frag_color = frag_color / weight_sum;
        frag_color = max(frag_color, 0.0001);
    }
    else
    {
        frag_color = e*0.125;
        frag_color += (a+c+g+i)*0.03125;
        frag_color += (b+d+f+h)*0.0625;
        frag_color += (j+k+l+m)*0.125;
    }

    frag_color.a = 1;
}