#version 460 core

in vec2 tex_coord;
out vec4 frag_color;

uniform sampler2D screen_image;
uniform bool gray;
uniform bool invert;

void main()
{ 
    frag_color = texture(screen_image, tex_coord);
    if (gray)
    {
        frag_color = vec4(frag_color.r, frag_color.r, frag_color.r, 1);
    }
    if (invert)
    {
        frag_color.rgb = 1 - frag_color.rgb;
    }
}