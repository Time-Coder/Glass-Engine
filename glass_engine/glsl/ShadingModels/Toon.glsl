#include "Phong.glsl"

float Toonify(float value, uint bands, float softness)
{
    return (soft_floor(value*(bands - 1) - softness/2, softness/2) + 1) / (bands - 1);
}

vec3 Toon_lighting(vec3 to_light, vec3 to_camera, vec3 normal, InternalMaterial material)
{
    float diffuse_factor = Lambert_diffuse(to_light, normal);
    vec3 diffuse_color = material.base_color * Toonify(diffuse_factor, material.diffuse_bands, material.diffuse_softness);
    float specular_factor = Phong_specular(to_light, to_camera, normal, material.shininess);
    vec3 specular_color = material.specular * Toonify(specular_factor, material.specular_bands, material.specular_softness);
    float rim_factor = pow(1 - dot(normal, to_camera), 1/(0.001+material.rim_power)) * pow(max(0, dot(to_light, normal)), 1/(1+material.light_rim_power));
    vec3 rim_color = material.base_color * soft_step(rim_factor-0.2, 0.05);
    return material.shadow_visibility*(diffuse_color + specular_color) + rim_color;
}