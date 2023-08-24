#ifndef _LIGHTS_GLSL__
#define _LIGHTS_GLSL__

#include "PointLight.glsl"
#include "DirLight.glsl"
#include "SpotLight.glsl"

buffer PointLights
{
    int n_point_lights;
    PointLight point_lights[];
};

buffer DirLights
{
    int n_dir_lights;
    DirLight dir_lights[];
};

buffer SpotLights
{
    int n_spot_lights;
    SpotLight spot_lights[];
};

#define GET_ONE_LIGHT_SPECULAR(light, internal_material, camera, view_dir, frag_pos, frag_normal) \
(\
    internal_material.shading_model == 3 ? \
        Phong_specular(\
            light, internal_material, camera,\
            view_dir, frag_pos, frag_normal\
        ) : (\
    internal_material.shading_model == 4 ? \
        PhongBlinn_specular(\
            light, internal_material, camera,\
            view_dir, frag_pos, frag_normal\
        ) : vec3(0))\
)

#define FRAG_LIGHTING_ONE(light, internal_material, camera_pos, CSM_camera, frag_pos, frag_normal) \
(\
    internal_material.shading_model == 3 ? \
        Phong_lighting(\
            light, internal_material,\
            camera_pos, CSM_camera, frag_pos, frag_normal\
        ) : (\
    internal_material.shading_model == 4 ? \
        PhongBlinn_lighting(\
            light, internal_material,\
            camera_pos, CSM_camera, frag_pos, frag_normal\
        ) : (\
    internal_material.shading_model == 5 ? \
        Toon_lighting(\
            light, internal_material,\
            camera_pos, CSM_camera, frag_pos, frag_normal\
        ) : (\
    internal_material.shading_model == 6 ? \
        OrenNayar_lighting(\
            light, internal_material,\
            camera_pos, CSM_camera, frag_pos, frag_normal\
        ) : (\
    internal_material.shading_model == 7 ? \
        Minnaert_lighting(\
            light, internal_material,\
            camera_pos, CSM_camera, frag_pos, frag_normal\
        ) : (\
    internal_material.shading_model == 10 ? \
        Fresnel_lighting(\
            light, internal_material,\
            camera_pos, CSM_camera, frag_pos, frag_normal\
        ) : (\
    (internal_material.shading_model == 8 || internal_material.shading_model == 11) ? \
        CookTorrance_lighting(\
            light, internal_material,\
            camera_pos, CSM_camera, frag_pos, frag_normal\
        ) : vec3(0, 0, 0)\
    ))))))\
)

vec3 GET_AMBIENT_DIFFUSE_FACTOR(bool recv_shadows, Camera camera, vec3 frag_pos, vec3 frag_normal)
{
    vec3 factor = vec3(0.2);

    // 点光源
    for(int i = 0; i < n_point_lights; i++)
    {
        factor += ambient_diffuse_factor(point_lights[i], recv_shadows, frag_pos, frag_normal);
    }

    // 平行光
    for(int i = 0; i < n_dir_lights; i++)
    {
        factor += ambient_diffuse_factor(dir_lights[i], recv_shadows, camera, frag_pos, frag_normal);
    }

    // 聚光
    for(int i = 0; i < n_spot_lights; i++)
    {
        factor += ambient_diffuse_factor(spot_lights[i], recv_shadows, frag_pos, frag_normal);
    }

    return soft_min(2*factor, vec3(1,1,1), 0.1);
}

vec3 GET_SPECULAR(InternalMaterial internal_material, Camera camera, vec3 view_dir, vec3 frag_pos, vec3 frag_normal)
{
    vec3 specular_color = vec3(0);

    // 点光源
    for(int i = 0; i < n_point_lights; i++)
    {
        specular_color += GET_ONE_LIGHT_SPECULAR(
            point_lights[i], internal_material, camera,
            view_dir, frag_pos, frag_normal
        );
    }

    // 平行光
    for(int i = 0; i < n_dir_lights; i++)
    {
        specular_color += GET_ONE_LIGHT_SPECULAR(
            dir_lights[i], internal_material, camera,
            view_dir, frag_pos, frag_normal
        );
    }

    // 聚光
    for(int i = 0; i < n_spot_lights; i++)
    {
        specular_color += GET_ONE_LIGHT_SPECULAR(
            spot_lights[i], internal_material, camera,
            view_dir, frag_pos, frag_normal
        );
    }

    return 3*specular_color;
}

vec3 FRAG_LIGHTING(InternalMaterial internal_material, Camera CSM_camera, vec3 camera_pos, vec3 frag_pos, vec3 frag_normal)
{
    vec3 out_color3 = internal_material.ambient;

    // 点光源
    for(int i = 0; i < n_point_lights; i++)
    {
        out_color3 += FRAG_LIGHTING_ONE(
            point_lights[i], internal_material, CSM_camera,
            camera_pos, frag_pos, frag_normal
        );
    }

    // 平行光
    for(int i = 0; i < n_dir_lights; i++)
    {
        out_color3 += FRAG_LIGHTING_ONE(
            dir_lights[i], internal_material, CSM_camera,
            camera_pos, frag_pos, frag_normal
        );
    }

    // 聚光
    for(int i = 0; i < n_spot_lights; i++)
    {
        out_color3 += FRAG_LIGHTING_ONE(
            spot_lights[i], internal_material, CSM_camera,
            camera_pos, frag_pos, frag_normal
        );
    }

    return out_color3;
}

#undef FRAG_LIGHTING_ONE

#define FLAT_LIGHTING(out_color3, internal_material, CSM_camera, camera_pos, face_pos, face_normal) \
out_color3 = internal_material.ambient;\
for(int j = 0; j < n_point_lights; j++)\
{\
    out_color3 += Flat_lighting(point_lights[j], internal_material, CSM_camera, camera_pos, face_pos, face_normal);\
}\
for(int j = 0; j < n_dir_lights; j++)\
{\
    out_color3 += Flat_lighting(dir_lights[j], internal_material, CSM_camera, camera_pos, face_pos, face_normal);\
}\
for(int j = 0; j < n_spot_lights; j++)\
{\
    out_color3 += Flat_lighting(spot_lights[j], internal_material, CSM_camera, camera_pos, face_pos, face_normal);\
}

#define GOURAUD_LIGHTING(out_color3, internal_material, CSM_camera, camera_pos, vertex_pos, vertex_normal) \
out_color3 = internal_material.ambient;\
for(int j = 0; j < n_point_lights; j++)\
{\
    out_color3 += Gouraud_lighting(point_lights[j], internal_material, CSM_camera, camera_pos, vertex_pos, vertex_normal);\
}\
for(int j = 0; j < n_dir_lights; j++)\
{\
    out_color3 += Gouraud_lighting(dir_lights[j], internal_material, CSM_camera, camera_pos, vertex_pos, vertex_normal);\
}\
for(int j = 0; j < n_spot_lights; j++)\
{\
    out_color3 += Gouraud_lighting(spot_lights[j], internal_material, CSM_camera, camera_pos, vertex_pos, vertex_normal);\
}

#endif