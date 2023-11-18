#if USE_DIR_LIGHT

#include "../include/Material.glsl"
#include "../include/random.glsl"
#include "../include/Camera.glsl"
#include "../ShadingModels/Lambert.glsl"
#include "../ShadingModels/lighting.glsl"
#include "DirLight_shadow_mapping.glsl"

vec3 get_lighting_info(
    in DirLight light, inout InternalMaterial material, in Camera CSM_camera,
    in vec3 to_camera, in vec3 frag_pos, in vec3 frag_normal
)
{
    vec3 to_light = -normalize(light.direction);
    material.light_rim_power = light.rim_power;
    material.shadow_visibility = 1;

#if USE_DIR_LIGHT_SHADOW
    if (light.generate_shadows && material.recv_shadows &&
        (light.depth_map_handle.x > 0 || light.depth_map_handle.y > 0))
    {
        material.shadow_visibility = PCF(light, CSM_camera, frag_pos, frag_normal);
    }
#endif

    return to_light;
}

vec3 lighting(DirLight light, InternalMaterial material, Camera CSM_camera,
    vec3 camera_pos, vec3 frag_pos, vec3 frag_normal)
{
    vec3 to_camera = normalize(camera_pos - frag_pos);
    vec3 to_light = get_lighting_info(light, material, CSM_camera, to_camera, frag_pos, frag_normal);
    
    vec3 lighting_color = lighting(to_light, to_camera, frag_normal, material);
    
    return light.color * lighting_color;
}

vec3 get_diffuse_color(DirLight light, InternalMaterial material, Camera CSM_camera,
    vec3 view_dir, vec3 frag_pos, vec3 frag_normal)
{
    vec3 to_camera = -view_dir;
    vec3 to_light = get_lighting_info(light, material, CSM_camera, to_camera, frag_pos, frag_normal);
    
    float diffuse_factor = Lambert_diffuse(to_light, frag_normal);
    float rim_factor = rim(to_light, to_camera, frag_normal, light.rim_power, material.rim_power);
    
    return (material.shadow_visibility*diffuse_factor + rim_factor) * light.color;
}

vec3 get_specular_color(DirLight light, InternalMaterial material, Camera CSM_camera,
    vec3 out_dir, vec3 frag_pos, vec3 frag_normal)
{
#if !USE_SHADING_MODEL_PHONG && !USE_SHADING_MODEL_PHONG_BLINN
    return vec3(0);
#else
    vec3 to_camera = normalize(reflect(-out_dir, frag_normal));
    vec3 to_light = get_lighting_info(light, material, CSM_camera, to_camera, frag_pos, frag_normal);
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

    return material.shadow_visibility * specular_factor * light.color;
#endif
}

#endif