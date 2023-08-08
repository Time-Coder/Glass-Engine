#version 460 core

#extension GL_EXT_texture_array : require

in TexCoord
{
    vec2 tex_coord;
} fs_in;

out vec4 frag_color;

#include "../include/FXAA.glsl"

uniform sampler2D screen_image;

vec4 medianBlur(sampler2D screen_image, vec2 tex_coord)
{
    int half_window = 7 / 2;
    
    vec3 values[49]; // Assuming window_size is always 5

    int index = 0;

    vec2 tex_offset = 1.0/textureSize(screen_image, 0);
    for (int y = -half_window; y <= half_window; ++y) {
        for (int x = -half_window; x <= half_window; ++x) {
            vec2 offset = vec2(x, y) * tex_offset;
            vec4 color = texture(screen_image, tex_coord + offset);
            values[index] = color.rgb;
            ++index;
        }
    }
    
    // Sort the values using insertion sort
    for (int i = 1; i < 49; ++i) {
        vec3 temp = values[i];
        int j = i - 1;
        while (j >= 0 && length(temp - values[j]) < length(values[j]) - length(values[i])) {
            values[j + 1] = values[j];
            --j;
        }
        values[j + 1] = temp;
    }
    
    return vec4(values[24], 1.0);
}

void main()
{
    frag_color = medianBlur(screen_image, fs_in.tex_coord);
}