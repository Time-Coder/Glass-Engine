#ifndef _SAMPLING_FS_GLSL__
#define _SAMPLING_FS_GLSL__

#include "sampling.glsl"

vec2 textureQueryLodSeamless(sampler2D image, vec2 tex_coord)
{
    ivec2 texture_size = textureSize(image, 0);
    float ds_dx = dFdx(tex_coord.s);
    if (ds_dx >= 0.9) ds_dx -= 1;
    if (ds_dx <= -0.9) ds_dx += 1;

    float ds_dy = dFdy(tex_coord.s);
    if (ds_dy >= 0.9) ds_dy -= 1;
    if (ds_dy <= -0.9) ds_dy += 1;

    float dt_dx = dFdx(tex_coord.t);
    if (dt_dx >= 0.9) dt_dx -= 1;
    if (dt_dx <= -0.9) dt_dx += 1;

    float dt_dy = dFdy(tex_coord.t);
    if (dt_dy >= 0.9) dt_dy -= 1;
    if (dt_dy <= -0.9) dt_dy += 1;

    vec2 dx = texture_size*vec2(ds_dx, dt_dx);
    vec2 dy = texture_size*vec2(ds_dy, dt_dy);

    float d = max( dot( dx, dx ), dot( dy, dy ) );
    float lod = 0.5 * log2(d);
    
    vec2 result = textureQueryLod(image, tex_coord);
    result.x = lod;

    return result;
}

vec4 textureSeamless(sampler2D image, vec2 tex_coord)
{
    float lod = textureQueryLodSeamless(image, tex_coord).x;
    return textureLod(image, tex_coord, lod);
}

vec4 textureSphere(sampler2D image, vec3 sphecial_tex_coord)
{
    float len = length(sphecial_tex_coord);
    if (len < 1E-6)
    {
        return vec4(0, 0, 0, 0);
    }
    sphecial_tex_coord /= len;

    vec2 tex_coord;
    tex_coord.x = 0.5*(atan(sphecial_tex_coord.x, sphecial_tex_coord.y)/PI + 1);
    tex_coord.y = asin(sphecial_tex_coord.z) / PI + 0.5;

    float cos_phi = length(sphecial_tex_coord.xy);
    float lod_factor = 1 - 0.99*pow(1-cos_phi, 20);
    float texture_lod = lod_factor * textureQueryLodSeamless(image, tex_coord).x;

    return textureLod(image, tex_coord, texture_lod);
}

#endif