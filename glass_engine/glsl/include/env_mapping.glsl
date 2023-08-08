#ifndef _ENVIRONMENT_MAPPING_GLSL__
#define _ENVIRONMENT_MAPPING_GLSL__

#include "sampling.glsl"
#include "FresnelRefract.glsl"

vec3 fetch_env_color(
    vec3 out_dir,
    bool use_skybox_map, samplerCube skybox_map,
    bool use_skydome_map, sampler2D skydome_map,
    bool use_env_map, sampler2D env_map
)
{
    vec4 env_color = vec4(0, 0, 0, 0);
    if (use_env_map)
    {
        env_color = textureSphere(env_map, out_dir);
    }
    
    vec3 sampling_dir = quat_apply(quat(cos45, sin45, 0, 0), out_dir);
    if (use_skybox_map)
    {
        vec3 skybox_color = texture(skybox_map, sampling_dir).rgb;
        env_color.rgb = mix(skybox_color, env_color.rgb, env_color.a);
    }
    else if (use_skydome_map)
    {
        vec3 skydome_color = textureSphere(skydome_map, out_dir).rgb;
        env_color.rgb = mix(skydome_color, env_color.rgb, env_color.a);
    }
    return env_color.rgb;
}

vec4 sphere_reflect_refract_color(
    vec4 reflection, vec4 refraction, float refractive_index,
    vec3 view_dir, vec3 normal,
    bool use_skybox_map, samplerCube skybox_map,
    bool use_skydome_map, sampler2D skydome_map,
    bool use_env_map, sampler2D env_map)
{
    if (!use_skybox_map && !use_skydome_map && !use_env_map)
    {
        return vec4(0, 0, 0, 0);
    }
    float cos_theta_in = dot(-view_dir, normal);

    bool use_reflection = (reflection.a > 0);
    bool use_refraction = (refraction.a > 0 && refractive_index > 0);
    if (!use_reflection && !use_refraction)
    {
        return vec4(0, 0, 0, 0);
    }
    
    float reflection_factor = 1;
    if (use_refraction)
    {
        reflection_factor = fresnel_equation(1, refractive_index, cos_theta_in);
    }
    if(reflection_factor > 1-1E-6)
    {
        use_refraction = false;
    }

    // 反射
    vec3 reflection_color = vec3(0, 0, 0);
    vec3 refraction_color = vec3(0, 0, 0);
    vec3 axis = cross(normal, view_dir);
    int times = 3;
    if (gl_FrontFacing)
    {
        // 反射
        vec3 reflect_out_dir = normalize(reflect(view_dir, normal));
        if (use_reflection)
        {
            reflection_color = reflection_factor * fetch_env_color(
                reflect_out_dir,
                use_skybox_map, skybox_map,
                use_skydome_map, skydome_map,
                use_env_map, env_map
            );
        }

        // 折射
        if (use_refraction)
        {
            float sin_theta_i = length(axis);
            if (sin_theta_i > 1E-6)
            {
                axis /= sin_theta_i;
            }
            float sin_theta_o = 1/refractive_index * sin_theta_i;
            if (sin_theta_o < 1)
            {
                float cos_theta_o = sqrt(1 - sin_theta_o*sin_theta_o);
                axis *= cos_theta_o;
                float refraction_factor = pow(1 - reflection_factor, 2);
                quat rotate_quat = quat(sin_theta_o, axis.x, axis.y, axis.z);
                vec3 refract_out_dir = quat_apply(rotate_quat, reflect_out_dir);
                for (int i = 0; i < times; i++)
                {
                    refraction_color += refraction_factor * fetch_env_color(
                        refract_out_dir,
                        use_skybox_map, skybox_map,
                        use_skydome_map, skydome_map,
                        use_env_map, env_map
                    );

                    refraction_factor *= reflection_factor;
                    refract_out_dir = quat_apply(rotate_quat, refract_out_dir);
                }
            }
        }
    }
    else if (use_refraction)
    {
        axis = -axis;
        float sin_theta_o = length(axis);
        if (sin_theta_o > 1E-6)
        {
            axis /= sin_theta_o;
        }
        float sin_theta_i = refractive_index * sin_theta_o;
        if (sin_theta_i < 1)
        {
            float cos_theta_o = sqrt(1 - sin_theta_o*sin_theta_o);
            float refraction_factor = 1 - reflection_factor;
            
            quat rotate_quat = quat(sin_theta_o, axis.x, axis.y, axis.z);
            vec3 refract_out_dir = normalize(refract(view_dir, normal, refractive_index));
            for (int i = 0; i < times; i++)
            {
                refraction_color += refraction_factor * fetch_env_color(
                    refract_out_dir,
                    use_skybox_map, skybox_map,
                    use_skydome_map, skydome_map,
                    use_env_map, env_map
                );

                refraction_factor *= reflection_factor;
                refract_out_dir = quat_apply(rotate_quat, refract_out_dir);
            }
        }
    }

    vec4 env_color;
    env_color.rgb = 
        reflection.rgb*reflection.a * reflection_color +
        refraction.rgb*refraction.a * refraction_color;
    env_color.a = 1 - (1-reflection.a)*(1-refraction.a);
    
    return env_color;
}

vec4 reflect_refract_color(
    vec4 reflection, vec4 refraction, float refractive_index,
    vec3 view_dir, vec3 normal,
    bool use_skybox_map, samplerCube skybox_map,
    bool use_skydome_map, sampler2D skydome_map,
    bool use_env_map, sampler2D env_map)
{
    if (!use_skybox_map && !use_skydome_map && !use_env_map)
    {
        return vec4(0, 0, 0, 0);
    }
    float cos_theta_in = dot(-view_dir, normal);


    bool use_reflection = (reflection.a > 0);
    bool use_refraction = (refraction.a > 0 && refractive_index > 0);
    if (!use_reflection && !use_refraction)
    {
        return vec4(0, 0, 0, 0);
    }

    float reflection_factor = 1;
    if (use_refraction)
    {
        if(gl_FrontFacing)
        {
            reflection_factor = fresnel_equation(1, refractive_index, cos_theta_in);
        }
        else
        {
            reflection_factor = fresnel_equation(refractive_index, 1, cos_theta_in);
        }
    }
    if(reflection_factor > 1-1E-6)
    {
        use_refraction = false;
    }

    // 反射
    vec3 reflection_color = vec3(0, 0, 0);
    if (use_reflection)
    {
        vec3 reflect_out_dir = normalize(reflect(view_dir, normal));
        reflection_color = reflection_factor * fetch_env_color(
            reflect_out_dir,
            use_skybox_map, skybox_map,
            use_skydome_map, skydome_map,
            use_env_map, env_map
        );
    }

    // 折射
    vec3 refraction_color = vec3(0, 0, 0);
    if (use_refraction)
    {
        if (gl_FrontFacing)
        {
            refractive_index = 1.0/refractive_index;
        }
        
        vec3 refract_out_dir = normalize(refract(view_dir, normal, refractive_index));
        refraction_color = (1-reflection_factor)*fetch_env_color(
            refract_out_dir,
            use_skybox_map, skybox_map,
            use_skydome_map, skydome_map,
            use_env_map, env_map
        );
    }

    vec4 env_color;
    env_color.rgb = 
        reflection.rgb*reflection.a * reflection_color +
        refraction.rgb*refraction.a * refraction_color;
    env_color.a = 1 - (1-reflection.a)*(1-refraction.a);
    
    return env_color;
}

#endif