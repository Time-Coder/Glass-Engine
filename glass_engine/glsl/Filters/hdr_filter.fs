#version 460 core

in vec2 tex_coord;
out vec4 frag_color;

uniform sampler2D screen_image;
uniform sampler2D luminance_image;

void main()
{
    vec3 frag_color3 = texture(screen_image, tex_coord).rgb;
    float luminance = dot(texture(luminance_image, tex_coord).rgb, vec3(0.2126, 0.7152, 0.0722));

    frag_color3 = vec3(1.0) - exp(-frag_color3 / (0.5+sqrt(luminance)/2));
    // frag_color3 = pow(frag_color3, vec3(0.8));
    frag_color3 = sin(0.5*acos(-1)*frag_color3);

    frag_color = vec4(frag_color3, 1);
}