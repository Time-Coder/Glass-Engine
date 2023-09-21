#ifndef _MATH_GLSL__
#define _MATH_GLSL__

#include "quat.glsl"

const float PI = acos(-1);
const float cos45 = 0.5*sqrt(2);
const float sin45 = cos45;

#define saturate(value) clamp(value, 0.0, 1.0)

float roundn(float value, uint n)
{
    float pow10n = pow(10, n);
    return round(value * pow10n) / pow10n;
}

uint get_digit(uint value, uint p)
{
    value /= p;
    return (value - value / 10 * 10);
}

float triangle_area(vec2 A, vec2 B, vec2 C)
{
    float a = length(B - C);
    float b = length(A - C);
    float c = length(A - B);
    float p = (a + b + c) / 2;
    return sqrt(p * (p - a) * (p - b) * (p - c));
}

float triangle_area(vec3 A, vec3 B, vec3 C)
{
    float a = length(B - C);
    float b = length(A - C);
    float c = length(A - B);
    float p = (a + b + c) / 2;
    return sqrt(p * (p - a) * (p - b) * (p - c));
}

bool is_equal(float a, float b)
{
    return abs(a - b) <= (abs(a) < abs(b) ? abs(b) : abs(a)) * 1E-6;
}

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

vec2 Hammersley(vec3 focus_point, uint i, uint N, inout int seed)
{
    uint rand_value = uint(1024*rand(focus_point, seed));
    uint bits = (i+rand_value << 16u) | (i+rand_value >> 16u);
    bits = ((bits & 0x55555555u) << 1u) | ((bits & 0xAAAAAAAAu) >> 1u);
    bits = ((bits & 0x33333333u) << 2u) | ((bits & 0xCCCCCCCCu) >> 2u);
    bits = ((bits & 0x0F0F0F0Fu) << 4u) | ((bits & 0xF0F0F0F0u) >> 4u);
    bits = ((bits & 0x00FF00FFu) << 8u) | ((bits & 0xFF00FF00u) >> 8u);
    float y = float(bits) * 2.3283064365386963e-10;

    return vec2(float(i)/float(N), y);
} 

float max3(vec3 v)
{
    return max(max(v.x, v.y), v.z);
}

float max4(vec4 v)
{
    return max(max(max(v.x, v.y), v.z), v.w);
}

float soft_abs(float value, float softness)
{
    float abs_value = abs(value);
    if (softness < 1E-6)
    {
        return abs_value;
    }

    return ((abs_value < softness) ? 0.5*(value*value/softness + softness) : abs_value);
}

float soft_sign(float value, float softness)
{
    float soft_abs_value = soft_abs(value, softness);
    if (soft_abs_value < 1E-6)
    {
        return sign(value);
    }
    return value / soft_abs_value;
}

vec2 soft_abs(vec2 value, float softness)
{
    vec2 result;
    result.x = soft_abs(value.x, softness);
    result.y = soft_abs(value.y, softness);
    return result;
}

vec3 soft_abs(vec3 value, float softness)
{
    vec3 result;
    result.x = soft_abs(value.x, softness);
    result.y = soft_abs(value.y, softness);
    result.z = soft_abs(value.z, softness);
    return result;
}

vec4 soft_abs(vec4 value, float softness)
{
    vec4 result;
    result.x = soft_abs(value.x, softness);
    result.y = soft_abs(value.y, softness);
    result.z = soft_abs(value.z, softness);
    result.w = soft_abs(value.w, softness);
    return result;
}

vec2 soft_sign(vec2 value, float softness)
{
    vec2 result;
    result.x = soft_sign(value.x, softness);
    result.y = soft_sign(value.y, softness);
    return result;
}

vec3 soft_sign(vec3 value, float softness)
{
    vec3 result;
    result.x = soft_sign(value.x, softness);
    result.y = soft_sign(value.y, softness);
    result.z = soft_sign(value.z, softness);
    return result;
}

vec4 soft_sign(vec4 value, float softness)
{
    vec4 result;
    result.x = soft_sign(value.x, softness);
    result.y = soft_sign(value.y, softness);
    result.z = soft_sign(value.z, softness);
    result.w = soft_sign(value.w, softness);
    return result;
}

#define soft_step(value, softness) (0.5*(soft_sign((value), (softness)) + 1.0))
#define soft_max(value1, value2, softness) (0.5 * ((value1) + (value2) + soft_abs((value1) - (value2), (softness))))
#define soft_min(value1, value2, softness) (0.5 * ((value1) + (value2) - soft_abs((value1) - (value2), (softness))))
#define soft_clamp(value, min_value, max_value, softness) soft_max(soft_min(value, max_value, softness), min_value, softness)
#define soft_saturate(value, softness) soft_clamp(value, 0.0, 1.0, softness)

float soft_floor(float x, float t)
{
    float floor_x = floor(x);
    float fract_x = x - floor_x;
    if (fract_x < 0.5)
    {
        return floor_x - 1 + soft_step(fract_x, t);
    }
    else if (fract_x > 0.5)
    {
        return floor_x + soft_step(fract_x - 1, t);
    }
    else
    {
        return floor_x;
    }
}

vec2 soft_floor(vec2 value, float softness)
{
    vec2 result;
    result.x = soft_floor(value.x, softness);
    result.y = soft_floor(value.y, softness);
    return result;
}

vec3 soft_floor(vec3 value, float softness)
{
    vec3 result;
    result.x = soft_floor(value.x, softness);
    result.y = soft_floor(value.y, softness);
    result.z = soft_floor(value.z, softness);
    return result;
}

vec4 soft_floor(vec4 value, float softness)
{
    vec4 result;
    result.x = soft_floor(value.x, softness);
    result.y = soft_floor(value.y, softness);
    result.z = soft_floor(value.z, softness);
    result.w = soft_floor(value.w, softness);
    return result;
}

float luminance(vec3 color)
{
    return dot(color, vec3(0.2126, 0.7152, 0.0722));
}

float luminance(vec4 color)
{
    return dot(color.rgb*color.a, vec3(0.2126, 0.7152, 0.0722));
}

float karis_weight(vec3 color)
{
    float luma = luminance(color) * 0.25;
    return 1.0 / (1.0 + luma);
}

float karis_weight(vec4 color)
{
    float luma = luminance(color) * 0.25;
    return 1.0 / (1.0 + luma);
}

bool hasnan(float x)
{
    return isnan(x);
}

bool hasnan(double x)
{
    return isnan(x);
}

bool hasnan(vec2 v)
{
    return (isnan(v.x) || isnan(v.y));
}

bool hasnan(dvec2 v)
{
    return (isnan(v.x) || isnan(v.y));
}

bool hasnan(vec3 v)
{
    return (isnan(v.x) || isnan(v.y) || isnan(v.z));
}

bool hasnan(dvec3 v)
{
    return (isnan(v.x) || isnan(v.y) || isnan(v.z));
}

bool hasnan(vec4 v)
{
    return (isnan(v.x) || isnan(v.y) || isnan(v.z) || isnan(v.w));
}

bool hasnan(dvec4 v)
{
    return (isnan(v.x) || isnan(v.y) || isnan(v.z) || isnan(v.w));
}

bool hasnan(quat q)
{
    return (isnan(q.x) || isnan(q.y) || isnan(q.z) || isnan(q.w));
}

bool hasinf(float x)
{
    return isinf(x);
}

bool hasinf(double x)
{
    return isinf(x);
}

bool hasinf(vec2 v)
{
    return (isinf(v.x) || isinf(v.y));
}

bool hasinf(dvec2 v)
{
    return (isinf(v.x) || isinf(v.y));
}

bool hasinf(vec3 v)
{
    return (isinf(v.x) || isinf(v.y) || isinf(v.z));
}

bool hasinf(dvec3 v)
{
    return (isinf(v.x) || isinf(v.y) || isinf(v.z));
}

bool hasinf(vec4 v)
{
    return (isinf(v.x) || isinf(v.y) || isinf(v.z) || isinf(v.w));
}

bool hasinf(dvec4 v)
{
    return (isinf(v.x) || isinf(v.y) || isinf(v.z) || isinf(v.w));
}

bool hasinf(quat q)
{
    return (isinf(q.x) || isinf(q.y) || isinf(q.z) || isinf(q.w));
}

#define DEFINE_MAT_HAS_NAN_INF(rows, cols) \
bool hasnan(mat##rows##x##cols A)\
{\
    for (int i = 0; i < rows; i++)\
    {\
        for (int j = 0; j < cols; j++)\
        {\
            if(isnan(A[j][i]))\
            {\
                return true;\
            }\
        }\
    }\
    return false;\
}\
bool hasnan(dmat##rows##x##cols A)\
{\
    for (int i = 0; i < rows; i++)\
    {\
        for (int j = 0; j < cols; j++)\
        {\
            if(isnan(A[j][i]))\
            {\
                return true;\
            }\
        }\
    }\
    return false;\
}\
bool hasinf(mat##rows##x##cols A)\
{\
    for (int i = 0; i < rows; i++)\
    {\
        for (int j = 0; j < cols; j++)\
        {\
            if(isinf(A[j][i]))\
            {\
                return true;\
            }\
        }\
    }\
    return false;\
}\
bool hasinf(dmat##rows##x##cols A)\
{\
    for (int i = 0; i < rows; i++)\
    {\
        for (int j = 0; j < cols; j++)\
        {\
            if(isinf(A[j][i]))\
            {\
                return true;\
            }\
        }\
    }\
    return false;\
}

DEFINE_MAT_HAS_NAN_INF(2, 2)
DEFINE_MAT_HAS_NAN_INF(2, 3)
DEFINE_MAT_HAS_NAN_INF(2, 4)
DEFINE_MAT_HAS_NAN_INF(3, 2)
DEFINE_MAT_HAS_NAN_INF(3, 3)
DEFINE_MAT_HAS_NAN_INF(3, 4)
DEFINE_MAT_HAS_NAN_INF(4, 2)
DEFINE_MAT_HAS_NAN_INF(4, 3)
DEFINE_MAT_HAS_NAN_INF(4, 4)

float legendre_eval(float x, int n)
{
    switch (n)
    {
    case 0: return 1;
    case 1: return x;
    default: 
    {
        float Pi_2 = 1;
        float Pi_1 = x;
        for (int i = 2; i <= n; i++)
        {
            float Pi = (2*i - 1) * x * Pi_1 - (i - 1) * Pi_2;
            Pi /= i;

            Pi_2 = Pi_1;
            Pi_1 = Pi;
        }
        return Pi_1;
    }
    }
}

#endif