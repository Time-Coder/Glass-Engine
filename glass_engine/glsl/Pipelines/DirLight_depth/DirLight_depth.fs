#version 460 core

in flat int visible;

layout (location = 0) out float ESM_value;
layout (location = 1) out vec2 VSM_values;
layout (location = 2) out vec4 EVSM_values;

void main()
{
    if (visible == 0)
    {
        discard;
    }

    ESM_value = exp(80 * gl_FragCoord.z);

    VSM_values.x = 2*gl_FragCoord.z-1;
    VSM_values.y = VSM_values.x * VSM_values.x;

    float depth = 2*gl_FragCoord.z-1;
    float c = 5;
    EVSM_values.x = exp(c*depth);
    EVSM_values.y = -exp(-c*depth);
    EVSM_values.z = exp(2*c*depth);
    EVSM_values.w = -exp(-2*c*depth);
}