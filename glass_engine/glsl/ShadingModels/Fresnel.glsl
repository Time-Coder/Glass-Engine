#ifndef _FRESNEL_GLSL__
#define _FRESNEL_GLSL__

vec3 Fresnel(vec3 to_camera, vec3 normal, vec3 base_color, float metallic, float rim_power)
{
    float cos_to_camera = max(0, dot(to_camera, normal));
    vec3 F0 = mix(vec3(0.04), base_color, metallic);
    vec3 F = F0 + (1 - F0) * pow(1 - cos_to_camera, 1/(0.001 + rim_power));
    return F;
}

vec3 Fresnel_lighting(
    vec3 to_light, vec3 to_camera, vec3 normal,
    InternalMaterial material)
{
    vec3 fresnel_color = Fresnel(to_camera, normal, material.base_color, material.metallic, material.rim_power);
    return material.ambient + fresnel_color;
}

#endif