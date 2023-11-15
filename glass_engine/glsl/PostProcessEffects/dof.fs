#version 430 core

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
    vec3 view_pos = textureLod(view_pos_map, fs_in.tex_coord, 0).xyz;
    float target_focus = camera.lens.focus;
    if (camera.lens.auto_focus)
    {
        vec3 clear_view_pos = textureLod(view_pos_map, camera.lens.focus_tex_coord, 0).xyz;
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
    if (!horizontal)
    {
        focus = _current_focus;
    }
    else if (abs(target_focus - _current_focus) > 1E-6)
    {
        if (_current_focus != 0 && camera.lens.focus_change_time > 1E-6)
        {
            float sgn = sign(target_focus - _current_focus);
            float a = 0.02/camera.lens.focus_change_time;
            focus = _current_focus + a * sgn / fps;
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
    }

    float factor = 1 / focus;
    if (length(view_pos) > 1E-6)
    {
        factor -= 1 / view_pos.y;
    }

    vec2 tex_size = textureSize(screen_image, 0);
    vec2 tex_offset = 1.0 / tex_size;
    frag_color = vec4(0);
    
    float pixel_per_meter = 0.5 * tex_size.y / (camera.near*camera.tan_half_fov);
    float coc_in_pixel = pixel_per_meter * abs(camera.lens.aperture*(1-camera.near*factor));
    if (coc_in_pixel <= 1)
    {
        frag_color = max(texture(screen_image, fs_in.tex_coord), 0.0);
        return;
    }

    float sigma = ((coc_in_pixel-1)*0.5 - 1)/3.0;
    
    float double_sigma2 = 2*sigma*sigma;
    if (horizontal)
    {
        float t = fs_in.tex_coord.t;
        float weight_sum = 0;
        for(int j = 0; j < coc_in_pixel; j++)
        {
            float dj = j - 0.5*(coc_in_pixel-1);
            float ds = dj*tex_offset.x;
            float s = fs_in.tex_coord.s + ds;
            float weight = exp(-dj*dj/double_sigma2);
            frag_color += weight * max(texture(screen_image, vec2(s, t)), 0.0);
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
            float di = i - 0.5*(coc_in_pixel-1);
            float dt = di*tex_offset.t;
            float t = fs_in.tex_coord.t + dt;
            float weight = exp(-di*di/double_sigma2);
            frag_color += weight * max(texture(screen_image, vec2(s, t)), 0.0);
            weight_sum += weight;
        }
        frag_color = frag_color / weight_sum;
    }
}