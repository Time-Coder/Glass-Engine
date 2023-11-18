#include "math.glsl"
#include "quat.glsl"

#define textureValid(image) (length(max(textureSize(image, 0)-1, 0)) > 1E-6)
#define textureEmpty(image) (length(max(textureSize(image, 0)-1, 0)) <= 1E-6)

vec3 vec2_to_cube_tex_coord(vec2 tex_coord, int face_id)
{
    tex_coord = clamp(tex_coord, vec2(0), vec2(1));
    vec3 cube_tex_coord = vec3(0);
    tex_coord -= vec2(0.5, 0.5);
    tex_coord *= 2;
    switch (face_id)
    {
    case 0: // right
    {
        cube_tex_coord.x = 1;
        cube_tex_coord.y = -tex_coord.x;
        cube_tex_coord.z = tex_coord.y;
        break;
    }
    case 1: // left
    {
        cube_tex_coord.x = -1;
        cube_tex_coord.y = tex_coord.x;
        cube_tex_coord.z = tex_coord.y;
        break;
    }
    case 2: // bottom
    {
        cube_tex_coord.x = tex_coord.x;
        cube_tex_coord.y = tex_coord.y;
        cube_tex_coord.z = -1;
        break;
    }
    case 3: // top
    {
        cube_tex_coord.x = tex_coord.x;
        cube_tex_coord.y = -tex_coord.y;
        cube_tex_coord.z = 1;
        break;
    }
    case 4: // front
    {
        cube_tex_coord.x = tex_coord.x;
        cube_tex_coord.y = 1;
        cube_tex_coord.z = tex_coord.y;
        break;
    }
    case 5: // back
    {
        cube_tex_coord.x = -tex_coord.x;
        cube_tex_coord.y = -1;
        cube_tex_coord.z = tex_coord.y;
        break;
    }
    }
    cube_tex_coord = normalize(cube_tex_coord);
    cube_tex_coord = quat_apply(quat(cos45, sin45, 0, 0), cube_tex_coord);
    return cube_tex_coord;
}

vec4 textureCubeFace(samplerCube cube_image, vec2 tex_coord, int face_id)
{
    vec3 cube_tex_coord = vec2_to_cube_tex_coord(tex_coord, face_id);
    return texture(cube_image, cube_tex_coord);
}

vec2 textureQueryLodSeamless(sampler2D image, vec2 tex_coord)
{
#ifdef FRAGMENT_SHADER
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
#else
    return vec2(0);
#endif
}

vec4 textureSeamless(sampler2D image, vec2 tex_coord)
{
    float lod = textureQueryLodSeamless(image, tex_coord).x;
    return textureLod(image, tex_coord, lod);
}

vec4 textureSphere(sampler2D image, vec3 sphecial_tex_coord, float bias)
{
    float len = length(sphecial_tex_coord);
    if (len < 1E-6)
    {
        return vec4(0);
    }
    sphecial_tex_coord /= len;
    vec2 tex_coord;
    tex_coord.x = 0.5*(atan(sphecial_tex_coord.x, sphecial_tex_coord.y)/PI + 1);
    tex_coord.y = asin(sphecial_tex_coord.z) / PI + 0.5;
    float cos_phi = length(sphecial_tex_coord.xy);
    float lod_factor = 1 - 0.99*pow(1-cos_phi, 20);
    float texture_lod = lod_factor * textureQueryLodSeamless(image, tex_coord).x;
    return textureLod(image, tex_coord, texture_lod+bias);
}

vec4 textureSphere(sampler2D image, vec3 sphecial_tex_coord)
{
    return textureSphere(image, sphecial_tex_coord, 0);
}