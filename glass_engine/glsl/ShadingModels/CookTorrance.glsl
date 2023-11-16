#include "../include/Material.glsl"

float NormalDistributionFunction(vec3 halfway_vec, vec3 normal, float roughness)
{
    roughness = mix(0.02, 1.0, roughness);
    float roughness4 = pow(roughness, 4);
    return roughness4 / pow(1 - (1 - roughness4)*pow(dot(normal, halfway_vec), 2), 2);
}

float GeometryFunction(float cos_to_light, float cos_to_camera, float roughness)
{
    float k = pow(roughness + 1, 2) / 8;
    float G = cos_to_light/(cos_to_light*(1 - k) + k) * cos_to_camera/(cos_to_camera*(1 - k) + k);
    return G;
}

vec3 FresnelEquation(float cos_to_camera, vec3 base_color, float metallic)
{
    vec3 F0 = mix(vec3(0.04), base_color, metallic);
    vec3 F = F0 + (1 - F0) * pow(1 - cos_to_camera, 5);
    return F;
}

vec3 CookTorrance_lighting(vec3 to_light, vec3 to_camera, vec3 normal, InternalMaterial material)
{
    float cos_to_light = max(dot(normal, to_light), 0);
    float cos_to_camera = max(dot(normal, to_camera), 0);
    vec3 halfway_vec = normalize(to_light + to_camera);
    float D = NormalDistributionFunction(halfway_vec, normal, material.roughness);
    float G = GeometryFunction(cos_to_light, cos_to_camera, material.roughness);
    vec3 F = FresnelEquation(cos_to_camera, material.base_color, material.metallic);
    vec3 kd = (1 - F)*(1 - material.metallic);
    vec3 Lo = kd * material.base_color * cos_to_light + D*G*F / (4*cos_to_camera + 0.001);
    return material.shadow_visibility * Lo;
}