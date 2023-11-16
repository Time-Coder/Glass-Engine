const float PI = acos(-1);
const float cos45 = 0.5*sqrt(2);
const float sin45 = cos45;

uint get_digit(uint value, uint p)
{
    value /= p;
    return (value - value / 10 * 10);
}

float luminance(vec3 color)
{
    return dot(color, vec3(0.2126, 0.7152, 0.0722));
}

float luminance(vec4 color)
{
    return dot(color.rgb*color.a, vec3(0.2126, 0.7152, 0.0722));
}

bool is_equal(float a, float b)
{
    return abs(a - b) <= (abs(a) < abs(b) ? abs(b) : abs(a)) * 1E-6;
}

float max3(vec3 v)
{
    return max(max(v.x, v.y), v.z);
}

float max4(vec4 v)
{
    return max(max(max(v.x, v.y), v.z), v.w);
}