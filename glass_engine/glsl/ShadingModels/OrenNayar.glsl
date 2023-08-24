#ifndef _OREN_NAYAR_GLSL__
#define _OREN_NAYAR_GLSL__

#include "rim.glsl"

float OrenNayar_diffuse(vec3 to_light, vec3 to_camera, vec3 normal, float roughness)
{
    float cos_to_light = max(0, dot(normal, to_light));
    float cos_to_camera = max(0, dot(normal, to_camera));
    float theta_to_light = acos(cos_to_light);
    float theta_to_camera = acos(cos_to_camera);

    float theta2 = roughness*roughness;
    float A = 1 - 0.5*(theta2/(theta2 +0.33));
    float B = 0.45 *(theta2/(theta2+0.09));
    
    float alpha = max(theta_to_camera, theta_to_light);
    float beta =  min(theta_to_camera, theta_to_light);
    float gamma = length(to_camera - normal*to_light) * length(to_light - normal*to_light);
    return cos_to_light * (A + B * max(0, gamma) * sin(alpha) * tan(beta));
}

vec3 OrenNayar_lighting(
    vec3 to_light, vec3 to_camera, vec3 normal,
    InternalMaterial material)
{
    vec3 diffuse_color = material.diffuse * OrenNayar_diffuse(to_light, to_camera, normal, material.roughness);
    vec3 rim_color = material.diffuse * rim(to_light, to_camera, normal, material.light_rim_power, material.rim_power);
    return material.ambient + diffuse_color + rim_color;
}

#endif