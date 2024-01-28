#version 430 core

in vec2 tex_coord;
out vec4 frag_color;

uniform sampler2D screen_image;
uniform float threshold;
uniform int mip_level;

#include "../include/math.glsl"
#include "../include/soft.glsl"

vec4 textureFirst(sampler2D image, vec2 tex_coord)
{
    vec4 color = textureLod(image, tex_coord, 0);
    float luma = luminance(color.rgb);
    float cutoff = soft_step(luma - threshold, 0.1);
    float max_value = 10;
    float weight = 1;
    if (luma > 1)
    {
        weight = (1 + max_value*tanh((luma-1)/max_value))/luma;
    }
    return vec4(cutoff * weight * color.rgb, clamp(color.a, 0.0, 1.0));
}

vec4 textureOther(sampler2D image, vec2 tex_coord)
{
    vec4 color = textureLod(image, tex_coord, 0);
    return vec4(max(color.rgb, 0.0), clamp(color.a, 0.0, 1.0));
}

#define textureAll(image, tex_coord) (mip_level == 0 ? textureFirst(image, tex_coord) : textureOther(image, tex_coord))

void main()
{
    vec2 tex_offset = 1.0 / textureSize(screen_image, 0);
    float dx = tex_offset.x;
    float dy = tex_offset.y;

    // Take 13 samples around current texel:
    // a - b - c
    // - j - k -
    // d - e - f
    // - l - m -
    // g - h - i
    // === ('e' is the current texel) ===
    vec4 a = textureAll(screen_image, vec2(tex_coord.x - 2*dx, tex_coord.y + 2*dy));
    vec4 b = textureAll(screen_image, vec2(tex_coord.x,        tex_coord.y + 2*dy));
    vec4 c = textureAll(screen_image, vec2(tex_coord.x + 2*dx, tex_coord.y + 2*dy));

    vec4 d = textureAll(screen_image, vec2(tex_coord.x - 2*dx, tex_coord.y));
    vec4 e = textureAll(screen_image, vec2(tex_coord.x,        tex_coord.y));
    vec4 f = textureAll(screen_image, vec2(tex_coord.x + 2*dx, tex_coord.y));

    vec4 g = textureAll(screen_image, vec2(tex_coord.x - 2*dx, tex_coord.y - 2*dy));
    vec4 h = textureAll(screen_image, vec2(tex_coord.x,        tex_coord.y - 2*dy));
    vec4 i = textureAll(screen_image, vec2(tex_coord.x + 2*dx, tex_coord.y - 2*dy));

    vec4 j = textureAll(screen_image, vec2(tex_coord.x - dx, tex_coord.y + dy));
    vec4 k = textureAll(screen_image, vec2(tex_coord.x + dx, tex_coord.y + dy));
    vec4 l = textureAll(screen_image, vec2(tex_coord.x - dx, tex_coord.y - dy));
    vec4 m = textureAll(screen_image, vec2(tex_coord.x + dx, tex_coord.y - dy));

    frag_color = e*0.125;
    frag_color += (a+c+g+i)*0.03125;
    frag_color += (b+d+f+h)*0.0625;
    frag_color += (j+k+l+m)*0.125;
}