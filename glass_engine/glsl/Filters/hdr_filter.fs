#version 460 core

in TexCoord
{
    vec2 tex_coord;
} fs_in;

out vec4 frag_color;

#include "../include/Camera.glsl"

uniform sampler2D screen_image;
uniform Camera camera;
uniform float fps;

buffer CurrentLuma
{
    float current_luma;
};

// filmic tone mapping
vec3 _Uncharted(vec3 x)
{
    const float A = 0.15;
    const float B = 0.50;
    const float C = 0.10;
    const float D = 0.20;
    const float E = 0.02;
    const float F = 0.30;
    const float W = 11.2;
    return ((x*(A*x+C*B)+D*E)/(x*(A*x+B)+D*F))-E/F;
}

void main()
{
    float target_luma = luminance(textureLod(screen_image, camera.focus_tex_coord, 7).rgb);
    float luma = target_luma;
    float _current_luma = current_luma;
    if(_current_luma != 0)
    {
        float sgn = sign(target_luma - _current_luma);
        luma = _current_luma + sgn * 100 * camera.focus_change_speed / fps;
        if (sgn == sign(luma - target_luma))
        {
            luma = target_luma;
        }
    }
    ivec2 frag_coord = ivec2(gl_FragCoord.xy);
    if (frag_coord.x == 0 && frag_coord.y == 0)
    {
        current_luma = luma;
        memoryBarrier();
    }
        
	frag_color = texture(screen_image, fs_in.tex_coord);
	// frag_color.rgb = vec3(1.0) - exp(-frag_color.rgb / (0.5+pow(luma, 1.0/3.0)));

    luma = 0.5*(0.5+pow(luma, 1.0/3.0));
    frag_color.rgb = _Uncharted(frag_color.rgb / luma) / _Uncharted(vec3(11.2));
    frag_color.rgb = sin(PI/2*frag_color.rgb);
}
