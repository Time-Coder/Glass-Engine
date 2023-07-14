#version 460 core

in vec2 tex_coord;
out vec4 frag_color;

uniform float filter_radius;
uniform sampler2D original_image;
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
    vec4 a = texture(screen_image, vec2(tex_coord.x - dx, tex_coord.y + dy));
    vec4 b = texture(screen_image, vec2(tex_coord.x,      tex_coord.y + dy));
    vec4 c = texture(screen_image, vec2(tex_coord.x + dx, tex_coord.y + dy));

    vec4 d = texture(screen_image, vec2(tex_coord.x - dx, tex_coord.y));
    vec4 e = texture(screen_image, vec2(tex_coord.x,      tex_coord.y));
    vec4 f = texture(screen_image, vec2(tex_coord.x + dx, tex_coord.y));

    vec4 g = texture(screen_image, vec2(tex_coord.x - dx, tex_coord.y - dy));
    vec4 h = texture(screen_image, vec2(tex_coord.x,      tex_coord.y - dy));
    vec4 i = texture(screen_image, vec2(tex_coord.x + dx, tex_coord.y - dy));

    // Apply weighted distribution, by using a 3x3 tent filter:
    //  1   | 1 2 1 |
    // -- * | 2 4 2 |
    // 16   | 1 2 1 |
    frag_color = e*4.0;
    frag_color += (b+d+f+h)*2.0;
    frag_color += (a+c+g+i);
    frag_color *= 1.0 / 16.0;

    vec4 original_color = texture(original_image, tex_coord);
    frag_color += original_color;
    frag_color.a = 1;
}