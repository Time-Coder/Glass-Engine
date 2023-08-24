#ifndef _RIM_GLSL__
#define _RIM_GLSL__

float rim(vec3 to_light, vec3 to_camera, vec3 normal, float light_rim_power, float material_rim_power)
{
    if (light_rim_power < 1E-6 || material_rim_power < 1E-6)
    {
        return 0;
    }

    return pow(0.5 - 0.5*dot(to_light, to_camera), 1/(0.001+light_rim_power)) * pow(1 - dot(normal, to_camera), 1/(0.001+material_rim_power));
}

#endif