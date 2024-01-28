#version 430 core

#extension GL_EXT_texture_array : require

in vec2 tex_coord;
out vec4 frag_color;

uniform sampler2D screen_image;
uniform sampler2DArray screen_image_array;
uniform int layer;
uniform int index;
uniform bool gray;
uniform bool invert;

void main()
{ 
    if (layer < 0)
        frag_color = max(texture(screen_image, tex_coord), 0.0);
    else
        frag_color = max(texture(screen_image_array, vec3(tex_coord, layer)), 0.0);
    
    if (gray)
        frag_color = vec4(vec3(frag_color[index]), 1);
    if (invert)
        frag_color.rgb = 1 - frag_color.rgb;
}