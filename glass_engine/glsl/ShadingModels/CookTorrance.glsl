#ifndef _COOKTORRANCE_LIGHTING_GLSL__
#define _COOKTORRANCE_LIGHTING_GLSL__

#include "Material.glsl"

float NormalDistributionFunction(vec3 halfway_vec, vec3 normal, float roughness)
{
    float roughness4 = pow(roughness, 4);
    float D = roughness4 / pow(pow(dot(normal, halfway_vec), 2) * (roughness4-1) + 1, 2);
    return D;
}

float GeometryFunction(float cos_theta_in, float cos_theta_out, float roughness)
{
    float k = pow(roughness + 1, 2) / 8;
    float G = cos_theta_in/(cos_theta_in*(1 - k) + k) * cos_theta_out/(cos_theta_out*(1 - k) + k);
    return G;
}

vec3 FresnelEquation(float cos_theta_out, vec3 albedo, float metallic)
{
    vec3 F0 = mix(vec3(0.04), albedo, metallic);
    vec3 F = F0 + (1 - F0) * pow(1 - cos_theta_out, 5);
    return F;
}

vec3 CookTorrance_lighting(vec3 to_light, vec3 to_camera, vec3 normal, InternalMaterial material)
{
    float cos_theta_in = max(dot(normal, to_light), 0);
    float cos_theta_out = max(dot(normal, to_camera), 0);
    vec3 halfway_vec = normalize(to_light + to_camera);
    float D = NormalDistributionFunction(halfway_vec, normal, material.roughness);
    float G = GeometryFunction(cos_theta_in, cos_theta_out, material.roughness);
    vec3 F = FresnelEquation(cos_theta_out, material.albedo, material.metallic);
    vec3 kd = (1 - F)*(1 - material.metallic);
    vec3 Lo = (kd * material.albedo + D*G*F / (4*cos_theta_in*cos_theta_out + 0.001))*cos_theta_in;
    Lo /= (Lo + vec3(1.0));
    return pow(Lo, vec3(1.0/2.2));
}

#endif