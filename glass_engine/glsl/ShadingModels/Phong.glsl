#include "Lambert.glsl"

float Phong_specular(vec3 to_light, vec3 to_camera, vec3 normal, float shininess)
{
    vec3 reflect_dir = reflect(-to_light, normal);
    float cos_out = max(dot(reflect_dir, to_camera), 0.0);
    return pow(cos_out, shininess);
}

vec3 Phong_lighting(vec3 to_light, vec3 to_camera, vec3 normal, InternalMaterial material)
{
    vec3 diffuse_color = material.diffuse * Lambert_diffuse(to_light, normal);
    vec3 specular_color = material.specular * Phong_specular(to_light, to_camera, normal, material.shininess);
    vec3 rim_color = material.diffuse * rim(to_light, to_camera, normal, material.light_rim_power, material.rim_power);
    return material.shadow_visibility*(diffuse_color + specular_color) + rim_color;
}