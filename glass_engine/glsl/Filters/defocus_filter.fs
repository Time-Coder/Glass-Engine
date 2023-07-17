#version 460 core

in vec2 tex_coord;
out vec4 frag_color;

#include "../include/Camera.glsl"

uniform sampler2D screen_image;
uniform sampler2D view_pos_map;
uniform Camera camera;
uniform bool horizontal;

void main()
{
    vec3 view_pos = texture(view_pos_map, tex_coord).xyz;
    float focus = camera.focus;
    if (camera.auto_focus)
    {
        vec3 clear_view_pos = texture(view_pos_map, camera.auto_focus_tex_coord).xyz;
        float clear_distance = clear_view_pos.y;
        if (length(clear_view_pos) > 1E-6)
        {
            focus = 1/(1/camera.near + 1/clear_distance);
        }
        else
        {
            focus = camera.near;
        }
    }

    float factor = 1 / focus;
    if (length(view_pos) > 1E-6)
    {
        factor -= 1 / view_pos.y;
    }

    vec2 tex_size = textureSize(screen_image, 0);
    vec2 tex_offset = 1.0 / tex_size;
    frag_color = vec4(0, 0, 0, 0);
    
    float dpi = 0.5 * tex_size.y / (camera.near*camera.tan_half_fov);
    float blur_width = abs(camera.len_diameter*(1-camera.near*factor));
    float blur_pixel_width = dpi * blur_width;
    if (blur_pixel_width <= 1)
    {
        frag_color = texture(screen_image, tex_coord);
        return;
    }

    float sigma = 0.3 * ((blur_pixel_width-1)*0.5 - 1) + 0.8;
    float double_sigma2 = 2*sigma*sigma;  
    if(horizontal)
    {
        float t = tex_coord.t;
        float weight_sum = 0;
        for(int j = 0; j < blur_pixel_width; j++)
        {
            float d = (j - 0.5*(blur_pixel_width-1))*tex_offset.x;
            float s = tex_coord.s + d;
            float weight = exp(-d*d/double_sigma2);
            frag_color += weight * texture(screen_image, vec2(s, t));
            weight_sum += weight;
        }
        frag_color = frag_color / weight_sum;
    }
    else
    {
        float s = tex_coord.s;
        float weight_sum = 0;
        for(int i = 0; i < blur_pixel_width; i++)
        {
            float d = (i - 0.5*(blur_pixel_width-1))*tex_offset.y;
            float t = tex_coord.t + d;
            float weight = exp(-d*d/double_sigma2);
            frag_color += weight * texture(screen_image, vec2(s, t));
            weight_sum += weight;
        }
        frag_color = frag_color / weight_sum;
    }
}