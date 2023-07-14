#ifndef _CUSTOM_SAMPLER_CUBE__
#define _CUSTOM_SAMPLER_CUBE__

#include "math.glsl"

struct CustomSamplerCube
{
    sampler2D left;
    sampler2D right;
    sampler2D back;
    sampler2D front;
    sampler2D bottom;
    sampler2D top;
};

vec4 textureCutom(CustomSamplerCube cube_map, vec3 tex_coord)
{
    if (dot(tex_coord, tex_coord) < 1E-6)
    {
        return vec4(0, 0, 0, 0);
    }

    tex_coord = quat_apply(quat(cos45, -sin45, 0, 0), tex_coord);

    vec2 tex_coord2;
    float x = tex_coord.x;
    float y = tex_coord.y;
    float z = tex_coord.z;
    float abs_x = abs(x);
    float abs_y = abs(y);
    float abs_z = abs(z);

    // left right
    if (abs_y <= abs_x && abs_z <= abs_x)
    {
        tex_coord2.s = 0.5*(1 - (x > 0 ? 1 : -1)*y/abs_x);
        tex_coord2.t = 0.5*(1 + z/abs_x);
        return texture((x > 0 ? cube_map.right : cube_map.left), tex_coord2);
    }

    // back front
    if (abs_x <= abs_y && abs_z <= abs_y)
    {
        tex_coord2.s = 0.5*(1 + (y > 0 ? 1 : -1)*x/abs_y);
        tex_coord2.t = 0.5*(1 + z/abs_y);
        return texture((y > 0 ? cube_map.front : cube_map.back), tex_coord2);
    }

    // bottom top
    if (abs_x <= abs_z && abs_y <= abs_z)
    {
        tex_coord2.s = 0.5*(1 + x/abs_z);
        tex_coord2.t = 0.5*(1 - (z > 0 ? 1 : -1)*y/abs_z);
        return texture((z > 0 ? cube_map.top : cube_map.bottom), tex_coord2);
    }

    return vec4(0, 0, 0, 0);
}

#endif