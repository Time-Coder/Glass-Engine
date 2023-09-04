#version 460 core

in TexCoord
{
    vec2 tex_coord;
} fs_in;

out vec4 frag_color;

#include "../include/sampling.glsl"

uniform float filter_radius;
uniform sampler2D screen_image;

void main()
{
    // The filter kernel is applied with a radius, specified in texture
    // coordinates, so that the radius will vary across mip resolutions.
    float dx = filter_radius;
    float dy = filter_radius;

    // Take 9 samples around current texel:
    // a - b - c
    // d - e - f
    // g - h - i
    // === ('e' is the current texel) ===
    vec4 a = textureColor(screen_image, vec2(fs_in.tex_coord.x - dx, fs_in.tex_coord.y + dy));
    vec4 b = textureColor(screen_image, vec2(fs_in.tex_coord.x,      fs_in.tex_coord.y + dy));
    vec4 c = textureColor(screen_image, vec2(fs_in.tex_coord.x + dx, fs_in.tex_coord.y + dy));

    vec4 d = textureColor(screen_image, vec2(fs_in.tex_coord.x - dx, fs_in.tex_coord.y));
    vec4 e = textureColor(screen_image, vec2(fs_in.tex_coord.x,      fs_in.tex_coord.y));
    vec4 f = textureColor(screen_image, vec2(fs_in.tex_coord.x + dx, fs_in.tex_coord.y));

    vec4 g = textureColor(screen_image, vec2(fs_in.tex_coord.x - dx, fs_in.tex_coord.y - dy));
    vec4 h = textureColor(screen_image, vec2(fs_in.tex_coord.x,      fs_in.tex_coord.y - dy));
    vec4 i = textureColor(screen_image, vec2(fs_in.tex_coord.x + dx, fs_in.tex_coord.y - dy));

    // Apply weighted distribution, by using a 3x3 tent filter:
    //  1   | 1 2 1 |
    // -- * | 2 4 2 |
    // 16   | 1 2 1 |
    frag_color = e*4.0;
    frag_color += (b+d+f+h)*2.0;
    frag_color += (a+c+g+i);
    frag_color *= 1.0 / 16.0;
    frag_color.a = 0.1;
}