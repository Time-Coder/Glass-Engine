#ifndef _MATH_GLSL__
#define _MATH_GLSL__

#include "quat.glsl"

const float PI = acos(-1);
const float cos45 = 0.5*sqrt(2);
const float sin45 = cos45;

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

float rand(vec2 frag_coord, inout int seed)
{
    float result = fract(sin((seed+1)*dot(frag_coord, vec2(12.9898, 78.233)))*43758.5453123);
    seed++;
    return result;
}

float rand(inout int seed)
{
    float result = fract(sin((seed+1)*dot(vec2(0.5, 0.5), vec2(12.9898, 78.233)))*43758.5453123);
    seed++;
    return result;
}

vec2 rand_vec2(vec2 frag_coord, inout int seed)
{
    vec2 result;
    result.x = rand(frag_coord, seed);
    result.y = rand(frag_coord, seed);
    return result;
}

vec2 rand_vec2(inout int seed)
{
    vec2 result;
    result.x = rand(seed);
    result.y = rand(seed);
    return result;
}

vec3 rand_vec3(vec2 frag_coord, inout int seed)
{
    vec3 result;
    result.x = rand(frag_coord, seed);
    result.y = rand(frag_coord, seed);
    result.z = rand(frag_coord, seed);
    return result;
}

vec3 rand_vec3(inout int seed)
{
    vec3 result;
    result.x = rand(seed);
    result.y = rand(seed);
    result.z = rand(seed);
    return result;
}

vec4 rand_vec4(vec2 frag_coord, inout int seed)
{
    vec4 result;
    result.x = rand(frag_coord, seed);
    result.y = rand(frag_coord, seed);
    result.z = rand(frag_coord, seed);
    result.w = rand(frag_coord, seed);
    return result;
}

vec4 rand_vec4(inout int seed)
{
    vec4 result;
    result.x = rand(seed);
    result.y = rand(seed);
    result.z = rand(seed);
    result.w = rand(seed);
    return result;
}

float max3(vec3 v)
{
    return max(max(v.x, v.y), v.z);
}

float max4(vec4 v)
{
    return max(max(max(v.x, v.y), v.z), v.w);
}

float soft_abs(float x, float t)
{
    float result = abs(x);
    result = (result<t) ? 0.5*(x*x/t + t) : result;
    return result;
}

float soft_abs(float x)
{
    float t = 0.1;
    float result = abs(x);
    result = (result<t) ? 0.5*(x*x/t + t) : result;
    return result;
}

float soft_sign(float x, float t)
{
    return x / soft_abs(x, t);
}

float soft_sign(float x)
{
    float t = 0.1;
    return x / soft_abs(x, t);
}

float soft_step(float x, float t)
{
    return 0.5*(soft_sign(x, t)+1.0);
}

float soft_step(float x)
{
    float t = 0.1;
    return 0.5*(soft_sign(x, t)+1.0);
}

float soft_max(float x, float y, float t)
{
    return 0.5 * (x + y + soft_abs(x - y, t));
}

float soft_max(float x, float y)
{
    float t = 0.1;
    return 0.5 * (x + y + soft_abs(x - y, t));
}

float soft_min(float x, float y, float t)
{
    return 0.5 * (x + y - soft_abs(x - y, t));
}

float soft_min(float x, float y)
{
    float t = 0.1;
    return 0.5 * (x + y - soft_abs(x - y, t));
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

#endif