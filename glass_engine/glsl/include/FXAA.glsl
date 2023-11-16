#include "sampling.glsl"

#define FXAA_SPAN_MAX 8.0
#define FXAA_REDUCE_MUL   (1.0/FXAA_SPAN_MAX)
#define FXAA_REDUCE_MIN   (1.0/128.0)
#define FXAA_SUBPIX_SHIFT (1.0/4.0)

vec4 textureFXAA(sampler2D screen_image, vec2 tex_coord)
{
    vec2 rcpFrame = 1.0 / textureSize(screen_image, 0);
    vec4 uv = vec4(tex_coord, tex_coord - (rcpFrame * (0.5 + FXAA_SUBPIX_SHIFT)));

    vec4 rgbNW = max(texture(screen_image, uv.zw), 0.0);
    vec4 rgbNE = max(texture(screen_image, uv.zw + vec2(1,0)*rcpFrame.xy), 0.0);
    vec4 rgbSW = max(texture(screen_image, uv.zw + vec2(0,1)*rcpFrame.xy), 0.0);
    vec4 rgbSE = max(texture(screen_image, uv.zw + vec2(1,1)*rcpFrame.xy), 0.0);
    vec4 rgbM  = max(texture(screen_image, uv.xy), 0.0);

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
        max(texture(screen_image, uv.xy + dir * (1.0/3.0 - 0.5)), 0.0) +
        max(texture(screen_image, uv.xy + dir * (2.0/3.0 - 0.5)), 0.0));
    vec4 rgbB = rgbA * (1.0/2.0) + (1.0/4.0) * (
        max(texture(screen_image, uv.xy + dir * (0.0/3.0 - 0.5)), 0.0) +
        max(texture(screen_image, uv.xy + dir * (3.0/3.0 - 0.5)), 0.0));
    
    float lumaB = luminance(rgbB);

    return ((lumaB < lumaMin || lumaB > lumaMax) ? rgbA : rgbB);
}

vec4 textureCubeFaceFXAA(samplerCube screen_image, vec2 tex_coord, int face_id)
{
    vec2 rcpFrame = 1.0 / textureSize(screen_image, 0);
    vec4 uv = vec4(tex_coord, tex_coord - (rcpFrame * (0.5 + FXAA_SUBPIX_SHIFT)));

    vec4 rgbNW = textureCubeFace(screen_image, uv.zw, face_id);
    vec4 rgbNE = textureCubeFace(screen_image, uv.zw + vec2(1,0)*rcpFrame.xy, face_id);
    vec4 rgbSW = textureCubeFace(screen_image, uv.zw + vec2(0,1)*rcpFrame.xy, face_id);
    vec4 rgbSE = textureCubeFace(screen_image, uv.zw + vec2(1,1)*rcpFrame.xy, face_id);
    vec4 rgbM  = textureCubeFace(screen_image, uv.xy, face_id);

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
        textureCubeFace(screen_image, uv.xy + dir * (1.0/3.0 - 0.5), face_id) +
        textureCubeFace(screen_image, uv.xy + dir * (2.0/3.0 - 0.5), face_id)
    );

    vec4 rgbB = rgbA * (1.0/2.0) + (1.0/4.0) * (
        textureCubeFace(screen_image, uv.xy + dir * (0.0/3.0 - 0.5), face_id) +
        textureCubeFace(screen_image, uv.xy + dir * (3.0/3.0 - 0.5), face_id)
    );
    
    float lumaB = luminance(rgbB);

    return ((lumaB < lumaMin || lumaB > lumaMax) ? rgbA : rgbB);
}

vec4 textureFXAA(sampler2DArray screen_image, vec3 tex_coord)
{
    vec2 rcpFrame = 1.0 / textureSize(screen_image, 0).xy;
    vec4 uv = vec4(tex_coord.st, tex_coord.st - (rcpFrame * (0.5 + FXAA_SUBPIX_SHIFT)));
    float layer = tex_coord[2];
    
    vec4 rgbNW = max(texture(screen_image, vec3(uv.zw, layer)), 0.0);
    vec4 rgbNE = max(texture(screen_image, vec3(uv.zw + vec2(1,0)*rcpFrame.xy, layer)), 0.0);
    vec4 rgbSW = max(texture(screen_image, vec3(uv.zw + vec2(0,1)*rcpFrame.xy, layer)), 0.0);
    vec4 rgbSE = max(texture(screen_image, vec3(uv.zw + vec2(1,1)*rcpFrame.xy, layer)), 0.0);
    vec4 rgbM  = max(texture(screen_image, vec3(uv.xy, layer)), 0.0);

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
        max(texture(screen_image, vec3(uv.xy + dir * (1.0/3.0 - 0.5), layer)), 0.0) +
        max(texture(screen_image, vec3(uv.xy + dir * (2.0/3.0 - 0.5), layer)), 0.0)
    );

    vec4 rgbB = rgbA * (1.0/2.0) + (1.0/4.0) * (
        max(texture(screen_image, vec3(uv.xy + dir * (0.0/3.0 - 0.5), layer)), 0.0) +
        max(texture(screen_image, vec3(uv.xy + dir * (3.0/3.0 - 0.5), layer)), 0.0)
    );
    
    float lumaB = luminance(rgbB);

    return ((lumaB < lumaMin || lumaB > lumaMax) ? rgbA : rgbB);
}
