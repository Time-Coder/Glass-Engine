#version 460 core

in TexCoord
{
    vec2 tex_coord;
} fs_in;

out vec4 frag_color;

#include "../include/Camera.glsl"

uniform sampler2D screen_image;
uniform sampler2D view_pos_map;
uniform Camera camera;
uniform bool horizontal;
uniform float fps;

buffer CurrentFocus
{
    float current_focus;
};

void main()
{
    vec3 view_pos = texture(view_pos_map, fs_in.tex_coord).xyz;
    float target_focus = camera.focus;
    if (camera.auto_focus)
    {
        vec3 clear_view_pos = texture(view_pos_map, camera.focus_tex_coord).xyz;
        float clear_distance = clear_view_pos.y;
        if (length(clear_view_pos) > 1E-6)
        {
            target_focus = 1/(1/camera.near + 1/clear_distance);
        }
        else
        {
            target_focus = camera.near;
        }
    }
    float focus = target_focus;
    float _current_focus = current_focus;
    if(_current_focus != 0)
    {
        float sgn = sign(target_focus - _current_focus);
        focus = _current_focus + sgn * camera.focus_change_speed / fps;
        if (sgn == sign(focus - target_focus))
        {
            focus = target_focus;
        }
    }
    ivec2 frag_coord = ivec2(gl_FragCoord.xy);
    if (frag_coord.x == 0 && frag_coord.y == 0)
    {
        current_focus = focus;
        memoryBarrier();
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
    float coc_in_pixel = dpi * abs(camera.aperture*(1-camera.near*factor));
    if (coc_in_pixel <= 1)
    {
        frag_color = texture(screen_image, fs_in.tex_coord);
        return;
    }

    float sigma = 0.3 * ((coc_in_pixel-1)*0.5 - 1) + 0.8;
    
    float double_sigma2 = 2*sigma*sigma;
    if(horizontal)
    {
        float t = fs_in.tex_coord.t;
        float weight_sum = 0;
        for(int j = 0; j < coc_in_pixel; j++)
        {
            float d = (j - 0.5*(coc_in_pixel-1))*tex_offset.x;
            float s = fs_in.tex_coord.s + d;
            float weight = exp(-d*d/double_sigma2);
            frag_color += weight * texture(screen_image, vec2(s, t));
            weight_sum += weight;
        }
        frag_color = frag_color / weight_sum;
    }
    else
    {
        float s = fs_in.tex_coord.s;
        float weight_sum = 0;
        for(int i = 0; i < coc_in_pixel; i++)
        {
            float d = (i - 0.5*(coc_in_pixel-1))*tex_offset.y;
            float t = fs_in.tex_coord.t + d;
            float weight = exp(-d*d/double_sigma2);
            frag_color += weight * texture(screen_image, vec2(s, t));
            weight_sum += weight;
        }
        frag_color = frag_color / weight_sum;
    }
}