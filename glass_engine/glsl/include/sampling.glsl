#ifndef _SAMPLING_GLSL__
#define _SAMPLING_GLSL__

#include "math.glsl"

vec3 vec2_to_cube_tex_coord(vec2 tex_coord, int camera_index)
{
    vec3 cube_tex_coord = vec3(0, 0, 0);
    tex_coord -= vec2(0.5, 0.5);
    tex_coord *= 2;
    switch (camera_index)
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

vec4 textureHQ(sampler2D image, vec2 tex_coord)
{
    vec2 tex_size = textureSize(image, 0);

    vec2 uv_scaled = tex_coord * tex_size + 0.5;
    vec2 uv_int = floor(uv_scaled);
    vec2 uv_frac = fract(uv_scaled);
    uv_frac = smoothstep(0, 1, uv_frac);
    vec2 uv = (uv_int + uv_frac - 0.5) / tex_size;

    return texture(image, uv);
}

#endif