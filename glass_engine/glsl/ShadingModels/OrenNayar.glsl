#include "rim.glsl"
#include "../include/Material.glsl"

vec3 OrenNayar_diffuse(vec3 to_light, vec3 to_camera, vec3 normal, float roughness, vec3 diffuse_color)
{
    float cos_theta_i = dot(normal, to_light);
    float cos_theta_r = dot(normal, to_camera);
    float theta_i = acos(cos_theta_i);
    float theta_r = acos(cos_theta_r);
    float cos_phi_r_phi_i = dot(normalize(to_camera - cos_theta_r*normal), normalize(to_light - cos_theta_i*normal));
    float alpha = max(theta_r, theta_i);
    float beta =  min(theta_r, theta_i);
    float sigma = 0.5*acos(-1)*roughness;
    float sigma2 = sigma*sigma;
    float C1 = 1 - 0.5 * sigma2 / (sigma2 + 0.33);
    float C2 = 0.45 * sigma2 / (sigma2 + 0.09);
    C2 *= (cos_phi_r_phi_i >= 0 ? sin(alpha) : sin(alpha) - pow(2*beta/PI, 3));
    float C3 = 2 * sigma2/(sigma2 + 0.09) * pow((alpha/PI)*(beta/PI), 2);
    float L1 = C1 + cos_phi_r_phi_i*C2*tan(beta) + (1 - abs(cos_phi_r_phi_i))*C3*tan(0.5*(alpha+beta));
    vec3 L2 = 0.17 * diffuse_color * sigma2 / (sigma2 + 0.13) * (1 - cos_phi_r_phi_i*pow(2*beta/PI, 2));
    return (L1 + L2) * max(cos_theta_i, 0.0);
}

vec3 OrenNayar_lighting(vec3 to_light, vec3 to_camera, vec3 normal, InternalMaterial material)
{
    vec3 diffuse_color = material.base_color * OrenNayar_diffuse(to_light, to_camera, normal, material.roughness, material.base_color);
    vec3 rim_color = material.base_color * rim(to_light, to_camera, normal, material.light_rim_power, material.rim_power);
    return material.shadow_visibility * diffuse_color + rim_color;
}