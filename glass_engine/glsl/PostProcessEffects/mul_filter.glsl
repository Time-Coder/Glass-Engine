uniform sampler2D filter_image;
uniform int filter_channels;

vec4 post_process(sampler2D screen_image, vec2 tex_coord)
{
    vec4 color0 = max(textureLod(screen_image, tex_coord, 0), 0.0);
    vec4 color1 = max(textureLod(filter_image, tex_coord, 0), 0.0);
    if (filter_channels == 1)
    {
        color1.gb = color1.rr;
        color1.a = 1;
    }

    return color0 * color1;
}