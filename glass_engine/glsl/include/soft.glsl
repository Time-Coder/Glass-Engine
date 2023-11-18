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