#version 430 core

in vec2 tex_coord;
out vec4 frag_color;

uniform sampler2D screen_image;
uniform sampler2D bloom_image;

void main()
{ 
    vec4 src_color = max(texture(screen_image, tex_coord), 0.0);
    vec4 bloom_color = max(texture(bloom_image, tex_coord), 0.0);
    frag_color = mix(bloom_color, src_color, 0.9);
}