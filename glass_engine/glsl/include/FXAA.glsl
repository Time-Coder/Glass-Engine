// FXAA code from: http://www.geeks3d.com/20110405/fxaa-fast-approximate-anti-aliasing-demo-glsl-opengl-test-radeon-geforce/3/

#include "math.glsl"

#define FXAA_SPAN_MAX 8.0
#define FXAA_REDUCE_MUL   (1.0/FXAA_SPAN_MAX)
#define FXAA_REDUCE_MIN   (1.0/128.0)
#define FXAA_SUBPIX_SHIFT (1.0/4.0)

vec4 textureFXAA(sampler2D screen_image, vec2 tex_coord)
{
    vec2 rcpFrame = 1.0 / textureSize(screen_image, 0);
    vec4 uv = vec4(tex_coord, tex_coord - (rcpFrame * (0.5 + FXAA_SUBPIX_SHIFT)));

    vec4 rgbNW = texture(screen_image, uv.zw);
    vec4 rgbNE = texture(screen_image, uv.zw + vec2(1,0)*rcpFrame.xy);
    vec4 rgbSW = texture(screen_image, uv.zw + vec2(0,1)*rcpFrame.xy);
    vec4 rgbSE = texture(screen_image, uv.zw + vec2(1,1)*rcpFrame.xy);
    vec4 rgbM  = texture(screen_image, uv.xy);

    float lumaNW = luminance(rgbNW);
    float lumaNE = luminance(rgbNE);
    float lumaSW = luminance(rgbSW);
    float lumaSE = luminance(rgbSE);
    float lumaM  = luminance(rgbM);

    float lumaMin = min(lumaM, min(min(lumaNW, lumaNE), min(lumaSW, lumaSE)));
    float lumaMax = max(lumaM, max(max(lumaNW, lumaNE), max(lumaSW, lumaSE)));

    vec2 dir;
    dir.x = -((lumaNW + lumaNE) - (lumaSW + lumaSE));
    dir.y =  ((lumaNW + lumaSW) - (lumaNE + lumaSE));

    float dirReduce = max(
        (lumaNW + lumaNE + lumaSW + lumaSE) * (0.25 * FXAA_REDUCE_MUL),
        FXAA_REDUCE_MIN);
    float rcpDirMin = 1.0/(min(abs(dir.x), abs(dir.y)) + dirReduce);
    
    dir = min(vec2( FXAA_SPAN_MAX,  FXAA_SPAN_MAX),
          max(vec2(-FXAA_SPAN_MAX, -FXAA_SPAN_MAX),
          dir * rcpDirMin)) * rcpFrame.xy;

    vec4 rgbA = (1.0/2.0) * (
        texture(screen_image, uv.xy + dir * (1.0/3.0 - 0.5)) +
        texture(screen_image, uv.xy + dir * (2.0/3.0 - 0.5)));
    vec4 rgbB = rgbA * (1.0/2.0) + (1.0/4.0) * (
        texture(screen_image, uv.xy + dir * (0.0/3.0 - 0.5)) +
        texture(screen_image, uv.xy + dir * (3.0/3.0 - 0.5)));
    
    float lumaB = luminance(rgbB);

    return ((lumaB < lumaMin || lumaB > lumaMax) ? rgbA : rgbB);
}

// vec4 textureFXAA(sampler2D screen_image, vec2 tex_coord) {
//     vec4 color;
//     vec2 inverse_resolution = 1.0 / vec2(textureSize(screen_image, 0));
//     vec3 rgbNW = texture(screen_image, tex_coord + vec2(-1.0, -1.0) * inverse_resolution).xyz;
//     vec3 rgbNE = texture(screen_image, tex_coord + vec2(1.0, -1.0) * inverse_resolution).xyz;
//     vec3 rgbSW = texture(screen_image, tex_coord + vec2(-1.0, 1.0) * inverse_resolution).xyz;
//     vec3 rgbSE = texture(screen_image, tex_coord + vec2(1.0, 1.0) * inverse_resolution).xyz;
//     vec3 rgbM = texture(screen_image, tex_coord).xyz;

//     vec3 luma = vec3(0.299, 0.587, 0.114);
//     float lumaNW = dot(rgbNW, luma);
//     float lumaNE = dot(rgbNE, luma);
//     float lumaSW = dot(rgbSW, luma);
//     float lumaSE = dot(rgbSE, luma);
//     float lumaM = dot(rgbM, luma);

//     float lumaMin = min(lumaM, min(min(lumaNW, lumaNE), min(lumaSW, lumaSE)));
//     float lumaMax = max(lumaM, max(max(lumaNW, lumaNE), max(lumaSW, lumaSE)));

//     vec2 dir;
//     dir.x = -((lumaNW + lumaNE) - (lumaSW + lumaSE));
//     dir.y = ((lumaNW + lumaSW) - (lumaNE + lumaSE));

//     float dirReduce = max((lumaNW + lumaNE + lumaSW + lumaSE) * (0.25 * 0.5), 0.0001);
//     float rcpDirMin = 1.0 / (min(abs(dir.x), abs(dir.y)) + dirReduce);

//     dir = min(vec2(0.5, 0.5) / inverse_resolution, max(vec2(-0.5, -0.5) / inverse_resolution, dir * rcpDirMin)) * inverse_resolution;

//     vec3 rgbA = 0.5 * (texture(screen_image, tex_coord.xy + dir * (1.0 / 3.0 - 0.5)).xyz + texture(screen_image, tex_coord.xy + dir * (2.0 / 3.0 - 0.5)).xyz);
//     vec3 rgbB = rgbA * 0.5 + 0.25 * (texture(screen_image, tex_coord.xy + dir * -0.5).xyz + texture(screen_image, tex_coord.xy + dir * 0.5).xyz);

//     float lumaB = dot(rgbB, luma);
//     if ((lumaB < lumaMin) || (lumaB > lumaMax)) {
//         color = vec4(rgbA, 1.0);
//     } else {
//         color = vec4(rgbB, 1.0);
//     }

//     return color;
// }