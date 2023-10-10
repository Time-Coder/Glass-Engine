#version 430 core

in TexCoord
{
    vec2 tex_coord;
} fs_in;

out vec4 frag_color;

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
    vec4 a = textureLod(screen_image, vec2(fs_in.tex_coord.x - dx, fs_in.tex_coord.y + dy), 0);
    vec4 b = textureLod(screen_image, vec2(fs_in.tex_coord.x,      fs_in.tex_coord.y + dy), 0);
    vec4 c = textureLod(screen_image, vec2(fs_in.tex_coord.x + dx, fs_in.tex_coord.y + dy), 0);

    vec4 d = textureLod(screen_image, vec2(fs_in.tex_coord.x - dx, fs_in.tex_coord.y), 0);
    vec4 e = textureLod(screen_image, vec2(fs_in.tex_coord.x,      fs_in.tex_coord.y), 0);
    vec4 f = textureLod(screen_image, vec2(fs_in.tex_coord.x + dx, fs_in.tex_coord.y), 0);

    vec4 g = textureLod(screen_image, vec2(fs_in.tex_coord.x - dx, fs_in.tex_coord.y - dy), 0);
    vec4 h = textureLod(screen_image, vec2(fs_in.tex_coord.x,      fs_in.tex_coord.y - dy), 0);
    vec4 i = textureLod(screen_image, vec2(fs_in.tex_coord.x + dx, fs_in.tex_coord.y - dy), 0);

    // Apply weighted distribution, by using a 3x3 tent filter:
    //  1   | 1 2 1 |
    // -- * | 2 4 2 |
    // 16   | 1 2 1 |
    frag_color = e*4.0;
    frag_color += (b+d+f+h)*2.0;
    frag_color += (a+c+g+i);
    frag_color *= 1.0 / 16.0;
}