#include "sampling.glsl"
#include "FresnelRefract.glsl"
#include "../Lights/Lights_lighting.glsl"
#include "fog.glsl"
#include "background.glsl"

#define ENV_MAP_SIZE ivec2(1024, 1024)

vec3 fetch_env_color(
    vec3 out_dir, float roughness,
    Background background
#if USE_FOG
    , Fog fog
#endif
#if USE_DYNAMIC_ENV_MAPPING
    , bool dynamic_env_mapping
    , uvec2 env_map_handle
#endif
)
{
    vec4 env_color = vec4(0);
    float bias = 0.7*roughness;

#if USE_DYNAMIC_ENV_MAPPING
    if (dynamic_env_mapping && (env_map_handle.x > 0 || env_map_handle.y > 0))
    {
        sampler2D env_map = sampler2D(env_map_handle);
        env_color = max(textureSphere(env_map, ENV_MAP_SIZE, out_dir, bias), 0.0);
    }
#endif

    vec3 background_color = background.color.rgb;
    if (textureValid(background.skybox_map))
    {
        vec3 sampling_dir = quat_apply(quat(cos45, sin45, 0, 0), out_dir);
        background_color = max(texture(background.skybox_map, sampling_dir, bias).rgb, 0.0);
    }
    else if (textureValid(background.skydome_map))
    {
        background_color = max(textureSphere(background.skydome_map, ENV_MAP_SIZE, out_dir, bias).rgb, 0.0);
    }

#if USE_FOG
    background_color = fog_apply(fog, background_color, background.distance);
#endif

    return mix(background_color, env_color.rgb, env_color.a);
}

vec4 sphere_reflect_refract_color(
    InternalMaterial material, Camera CSM_camera,
    vec3 env_center, vec3 view_dir, vec3 frag_pos, vec3 frag_normal,
    Background background
#if USE_FOG
    , Fog fog
#endif
#if USE_DYNAMIC_ENV_MAPPING
    , uvec2 env_map_handle
#endif
)
{
    vec4 reflection = material.reflection;
    float refractive_index = material.refractive_index;
    float shininess = material.shininess;
    if (shininess < 1)
        shininess = 1;

    bool recv_shadows = material.recv_shadows;
    bool use_reflection = (length(reflection.rgb*reflection.a) > 1E-6);
    bool use_refraction = (use_reflection && refractive_index > 1E-6);
    if (!use_reflection && !use_refraction)
        return vec4(0);

    float reflection_factor = 1;
    float cos_theta_in = dot(-view_dir, frag_normal);
    if (use_refraction)
        reflection_factor = fresnel_reflect_ratio(1, refractive_index, cos_theta_in);
    if (reflection_factor > 1-1E-6)
        use_refraction = false;

    float sphere_radius = length(frag_pos - env_center);
    vec3 reflection_color = vec3(0);
    vec3 refraction_color = vec3(0);
    vec3 axis = cross(frag_normal, view_dir);
    int times = 3;
    if (gl_FrontFacing)
    {
        vec3 reflect_out_dir = normalize(reflect(view_dir, frag_normal));
        if (use_reflection)
        {
            
            reflection_color = reflection_factor * fetch_env_color(
                reflect_out_dir, material.roughness,
                background
#if USE_FOG
                , fog
#endif
#if USE_DYNAMIC_ENV_MAPPING
                , material.dynamic_env_mapping
                , env_map_handle
#endif
            );
            
            vec3 specular_color = get_specular_color(material, CSM_camera, reflect_out_dir, frag_pos, frag_normal);
            reflection_color += reflection_factor*specular_color;
        }

        if (use_refraction)
        {
            float sin_theta_i = length(axis);
            if (sin_theta_i > 1E-6)
                axis /= sin_theta_i;
            float sin_theta_o = 1/refractive_index * sin_theta_i;
            if (sin_theta_o < 1)
            {
                float cos_theta_o = sqrt(1 - sin_theta_o*sin_theta_o);
                axis *= cos_theta_o;
                float refraction_factor = pow(1 - reflection_factor, 2);
                quat rotate_quat = quat(sin_theta_o, axis.x, axis.y, axis.z);
                vec3 refract_out_dir = quat_apply(rotate_quat, reflect_out_dir);
                frag_normal = quat_apply(rotate_quat, frag_normal);
                frag_pos = env_center + sphere_radius * frag_normal;
                for (int i = 0; i < times; i++)
                {
                    refraction_color += refraction_factor * fetch_env_color(
                        refract_out_dir, material.roughness,
                        background
#if USE_FOG
                        , fog
#endif
#if USE_DYNAMIC_ENV_MAPPING
                        , material.dynamic_env_mapping
                        , env_map_handle
#endif
                    );
                    if (i >= 1)
                        material.recv_shadows = false;
                    vec3 specular_color = get_specular_color(material, CSM_camera, refract_out_dir, frag_pos, frag_normal);
                    refraction_color += refraction_factor*specular_color;

                    refraction_factor *= reflection_factor;
                    refract_out_dir = quat_apply(rotate_quat, refract_out_dir);
                    frag_normal = quat_apply(rotate_quat, frag_normal);
                    frag_pos = env_center + sphere_radius * frag_normal;
                }
            }
        }
    }
    else if (use_refraction)
    {
        axis = -axis;
        float sin_theta_o = length(axis);
        if (sin_theta_o > 1E-6)
            axis /= sin_theta_o;
        float sin_theta_i = refractive_index * sin_theta_o;
        if (sin_theta_i < 1)
        {
            float cos_theta_o = sqrt(1 - sin_theta_o*sin_theta_o);
            float refraction_factor = 1 - reflection_factor;
            
            quat rotate_quat = quat(sin_theta_o, axis.x, axis.y, axis.z);
            vec3 refract_out_dir = normalize(refract(view_dir, frag_normal, refractive_index));
            frag_normal = quat_apply(rotate_quat, frag_normal);
            for (int i = 0; i < times; i++)
            {
                refraction_color += refraction_factor * fetch_env_color(
                    refract_out_dir, material.roughness,
                    background
#if USE_FOG
                    , fog
#endif
#if USE_DYNAMIC_ENV_MAPPING
                    , material.dynamic_env_mapping
                    , env_map_handle
#endif
                );
                if (i >= 1)
                    material.recv_shadows = false;
                vec3 specular_color = get_specular_color(material, CSM_camera, refract_out_dir, frag_pos, frag_normal);
                refraction_color += refraction_factor*specular_color;

                refraction_factor *= reflection_factor;
                refract_out_dir = quat_apply(rotate_quat, refract_out_dir);
                frag_normal = quat_apply(rotate_quat, frag_normal);
            }
        }
    }

    vec4 env_color;
    env_color.rgb = reflection.rgb * (reflection_color + refraction_color);
    env_color.a = reflection.a;
    if (material.roughness > 1E-6)
    {
        vec3 diffuse_color = get_diffuse_color(material, CSM_camera, view_dir, frag_pos, frag_normal);        
        env_color.rgb *= mix(vec3(1), diffuse_color, material.roughness);
    }
    
    return env_color;
}

vec4 reflect_refract_color(
    InternalMaterial material, Camera CSM_camera,
    vec3 env_center, vec3 view_dir, vec3 frag_pos, vec3 frag_normal,
    Background background
#if USE_FOG
    , Fog fog
#endif
#if USE_DYNAMIC_ENV_MAPPING
    , uvec2 env_map_handle
#endif
)
{
    vec4 reflection = material.reflection;
    float refractive_index = material.refractive_index;
    float shininess = material.shininess;
    if (shininess < 1)
        shininess = 1;

    bool recv_shadows = material.recv_shadows;
    bool use_reflection = (length(reflection.rgb*reflection.a) > 1E-6);
    bool use_refraction = (use_reflection && refractive_index > 1E-6);
    if (!use_reflection && !use_refraction)
        return vec4(0);

    float reflection_factor = 1;
    float cos_theta_in = dot(-view_dir, frag_normal);
    if (use_refraction)
    {
        if (gl_FrontFacing)
            reflection_factor = fresnel_reflect_ratio(1, refractive_index, cos_theta_in);
        else
            reflection_factor = fresnel_reflect_ratio(refractive_index, 1, cos_theta_in);
    }
    if (reflection_factor > 1-1E-6)
        use_refraction = false;

    vec3 reflection_color = vec3(0);
    if (use_reflection)
    {
        vec3 reflect_out_dir = normalize(reflect(view_dir, frag_normal));
        reflection_color = reflection_factor * fetch_env_color(
            reflect_out_dir, material.roughness, background
#if USE_FOG
            , fog
#endif
#if USE_DYNAMIC_ENV_MAPPING
            , material.dynamic_env_mapping
            , env_map_handle
#endif
        );
        vec3 specular_color = get_specular_color(material, CSM_camera, reflect_out_dir, frag_pos, frag_normal);
        reflection_color += reflection_factor * specular_color;
    }

    vec3 refraction_color = vec3(0);
    if (use_refraction)
    {
        if (gl_FrontFacing)
            refractive_index = 1.0/refractive_index;
        vec3 refract_out_dir = normalize(refract(view_dir, frag_normal, refractive_index));
        refraction_color = (1-reflection_factor)*fetch_env_color(
            refract_out_dir, material.roughness,
            background
#if USE_FOG
            , fog
#endif
#if USE_DYNAMIC_ENV_MAPPING
            , material.dynamic_env_mapping
            , env_map_handle
#endif
        );
        vec3 specular_color = get_specular_color(material, CSM_camera, refract_out_dir, frag_pos, frag_normal);
        refraction_color += (1 - reflection_factor) * specular_color;
    }

    vec4 env_color;
    env_color.rgb = reflection.rgb * (reflection_color + refraction_color);
    env_color.a = reflection.a;
    if (material.roughness > 1E-6)
    {
        vec3 diffuse_color = get_diffuse_color(material, CSM_camera, view_dir, frag_pos, frag_normal);        
        env_color.rgb *= mix(vec3(1), diffuse_color, material.roughness);
    }
    
    return env_color;
}