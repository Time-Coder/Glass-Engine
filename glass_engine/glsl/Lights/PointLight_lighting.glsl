#if USE_POINT_LIGHT

#include "../include/Material.glsl"
#include "../include/random.glsl"
#include "../include/Camera.glsl"
#include "PointLight_shadow_mapping.glsl"

bool get_lighting_info(
    in PointLight light, inout InternalMaterial material,
    in vec3 to_camera, in vec3 frag_pos, in vec3 frag_normal,
    out vec3 to_light, out float attenuation)
{
    to_light = light.abs_position - frag_pos;
    float d2 = dot(to_light, to_light);
    if (d2 > light.coverage*light.coverage)
    {
        return false;
    }
    float d = sqrt(d2);
    to_light /= d;

    material.light_rim_power = light.rim_power;
    material.shadow_visibility = 1;
#if USE_POINT_LIGHT_SHADOW
    if (light.generate_shadows && material.recv_shadows &&
        (light.depth_map_handle.x > 0 || light.depth_map_handle.y > 0))
    {
        material.shadow_visibility = PCF(light, frag_pos, frag_normal);
    }
#endif

    attenuation = 1.0 / (1.0 + light.K1 * d +  light.K2 * d2);
    return true;
}

vec3 lighting(
    PointLight light, InternalMaterial material,
    vec3 camera_pos, vec3 frag_pos, vec3 frag_normal)
{
    vec3 to_camera = normalize(camera_pos - frag_pos);
    vec3 to_light;
    float attenuation;
    if (!get_lighting_info(
            light, material, to_camera,
            frag_pos, frag_normal,
            to_light, attenuation))
    {
        return vec3(0);
    }

    vec3 lighting_color = lighting(to_light, to_camera, frag_normal, material);
    return attenuation * light.color * lighting_color;
}

vec3 get_diffuse_color(
    PointLight light, InternalMaterial material,
    vec3 view_dir, vec3 frag_pos, vec3 frag_normal)
{
    vec3 to_camera = -view_dir;
    vec3 to_light;
    float attenuation;
    if (!get_lighting_info(
            light, material, to_camera,
            frag_pos, frag_normal,
            to_light, attenuation))
    {
        return vec3(0);
    }

    float diffuse_factor = Lambert_diffuse(to_light, frag_normal);
    float rim_factor = rim(to_light, to_camera, frag_normal, light.rim_power, material.rim_power);
    return attenuation * (material.shadow_visibility*diffuse_factor + rim_factor) * light.color;
}

vec3 get_specular_color(
    PointLight light, InternalMaterial material,
    vec3 out_dir, vec3 frag_pos, vec3 frag_normal)
{
    vec3 to_camera = normalize(reflect(-out_dir, frag_normal));
    vec3 to_light;
    float attenuation;
    if (!get_lighting_info(
            light, material,
            to_camera, frag_pos, frag_normal,
            to_light, attenuation))
    {
        return vec3(0);
    }

    float specular_factor = 0;
#if USE_SHADING_MODEL_PHONG
    if (material.shading_model == SHADING_MODEL_PHONG)
    {
        specular_factor = Phong_specular(to_light, to_camera, frag_normal, material.shininess);
    }
#endif

#if USE_SHADING_MODEL_PHONG_BLINN
    if (material.shading_model == SHADING_MODEL_PHONG_BLINN)
    {
        specular_factor = PhongBlinn_specular(to_light, to_camera, frag_normal, material.shininess);
    }
#endif

    return material.shadow_visibility * attenuation * specular_factor * light.color;
}

#endif