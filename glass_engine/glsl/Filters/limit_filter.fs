#version 460 core

in vec2 tex_coord;
out vec4 frag_color;

uniform sampler2D screen_image;

void main()
{
    vec4 color = texture(screen_image, tex_coord);
    float gray_value = dot(vec3(0.2126, 0.7152, 0.0722), color.rgb);
    if (gray_value > 1)
    {
        gray_value = 1 + tanh(gray_value-1);
    }
    frag_color = vec4(gray_value, gray_value, gray_value, 1);
}