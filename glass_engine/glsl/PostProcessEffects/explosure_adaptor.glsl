#include "../include/math.glsl"

uniform float fps;

buffer CurrentLuma
{
    float current_luma;
};

vec4 post_process(sampler2D screen_image, vec2 tex_coord)
{
    vec4 color = max(textureLod(screen_image, tex_coord, 0), 0.0);
    ivec2 frag_coord = ivec2(gl_FragCoord.xy);
    if (!camera.lens.auto_explosure)
    {
        if (frag_coord.x == 0 && frag_coord.y == 0)
        {
            current_luma = pow((1.0/camera.lens.explosure) - 0.5, 2.0);
            memoryBarrier();
        }

        color.rgb = camera.lens.explosure * color.rgb;
    }
    else if (!camera.lens.local_explosure)
    {
        float target_luma = luminance(max(textureLod(screen_image, camera.lens.focus_tex_coord, 6).rgb, 0.0));
        float luma = target_luma;
        float _current_luma = current_luma;
        if (abs(target_luma-current_luma) > 1E-6)
        {
            if (_current_luma != 0 && camera.lens.explosure_adapt_time > 1E-6)
            {
                float sgn = sign(target_luma - _current_luma);
                float a = log(10)/camera.lens.explosure_adapt_time;
                luma = _current_luma + a * (target_luma - _current_luma) / fps;
                if (sgn == sign(luma - target_luma))
                {
                    luma = target_luma;
                }
            }
            if (frag_coord.x == 0 && frag_coord.y == 0)
            {
                current_luma = luma;
                memoryBarrier();
            }
        }

        color.rgb = color.rgb / (0.5 + sqrt(luma));
        return color;
    }
    else
    {
        float luma = luminance(max(textureLod(screen_image, tex_coord, 7).rgb, 0.0));
        color.rgb = color.rgb / (0.5 + sqrt(luma));
    }
    return color;
}
