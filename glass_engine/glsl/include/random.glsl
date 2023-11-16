#include "quat.glsl"

float rand(vec2 focus_point, inout int seed)
{
    float result = fract(sin((seed+1)*dot(focus_point, vec2(12.9898, 78.233)))*43758.5453123);
    seed++;
    return result;
}

float rand(vec3 focus_point, inout int seed)
{
    float result = fract(sin((seed+1)*dot(focus_point, vec3(12.9898, 78.233, 63.643)))*43758.5453123);
    seed++;
    return result;
}

float rand(inout int seed)
{
    float result = fract(sin((seed+1)*dot(vec2(0.5, 0.5), vec2(12.9898, 78.233)))*43758.5453123);
    seed++;
    return result;
}

vec2 rand2(vec2 focus_point, inout int seed)
{
    vec2 result;
    result.x = rand(focus_point, seed);
    result.y = rand(focus_point, seed);
    return result;
}

vec2 rand2(vec3 focus_point, inout int seed)
{
    vec2 result;
    result.x = rand(focus_point, seed);
    result.y = rand(focus_point, seed);
    return result;
}

vec2 rand2(inout int seed)
{
    vec2 result;
    result.x = rand(seed);
    result.y = rand(seed);
    return result;
}

vec3 rand3(vec2 focus_point, inout int seed)
{
    vec3 result;
    result.x = rand(focus_point, seed);
    result.y = rand(focus_point, seed);
    result.z = rand(focus_point, seed);
    return result;
}

vec3 rand3(vec3 focus_point, inout int seed)
{
    vec3 result;
    result.x = rand(focus_point, seed);
    result.y = rand(focus_point, seed);
    result.z = rand(focus_point, seed);
    return result;
}

vec3 rand3(inout int seed)
{
    vec3 result;
    result.x = rand(seed);
    result.y = rand(seed);
    result.z = rand(seed);
    return result;
}

vec3 rand3_near_focus(vec3 direction, float max_angle_shift, inout int seed)
{
    float phi = max_angle_shift * rand(direction, seed);
    float cos_half_phi = cos(phi/2);
    float sin_half_phi = sin(phi/2);
    vec3 axis = 2*rand3(direction, seed) - 1;
    vec3 sin_half_phi_axis = sin_half_phi * normalize(axis);
    quat rotation = quat(cos_half_phi, sin_half_phi_axis.x, sin_half_phi_axis.y, sin_half_phi_axis.z);
    return quat_apply(rotation, direction);
}

vec3 rand3_near(vec3 direction, float max_angle_shift, inout int seed)
{
    float phi = max_angle_shift * sqrt(rand(direction, seed));
    float cos_half_phi = cos(phi/2);
    float sin_half_phi = sin(phi/2);
    vec3 axis = 2*rand3(direction, seed) - 1;
    vec3 sin_half_phi_axis = sin_half_phi * normalize(axis);
    quat rotation = quat(cos_half_phi, sin_half_phi_axis.x, sin_half_phi_axis.y, sin_half_phi_axis.z);
    return quat_apply(rotation, direction);
}

vec4 rand4(vec2 focus_point, inout int seed)
{
    vec4 result;
    result.x = rand(focus_point, seed);
    result.y = rand(focus_point, seed);
    result.z = rand(focus_point, seed);
    result.w = rand(focus_point, seed);
    return result;
}

vec4 rand4(vec3 focus_point, inout int seed)
{
    vec4 result;
    result.x = rand(focus_point, seed);
    result.y = rand(focus_point, seed);
    result.z = rand(focus_point, seed);
    result.w = rand(focus_point, seed);
    return result;
}

vec4 rand4(inout int seed)
{
    vec4 result;
    result.x = rand(seed);
    result.y = rand(seed);
    result.z = rand(seed);
    result.w = rand(seed);
    return result;
}