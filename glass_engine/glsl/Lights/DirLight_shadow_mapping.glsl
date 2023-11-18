#if USE_DIR_LIGHT && USE_DIR_LIGHT_SHADOW

#include "DirLight.glsl"
#include "../include/Camera.glsl"
#include "../include/random.glsl"

vec4 world_to_lightNDC(DirLight light, Camera CSM_camera, int level, vec3 world_coord, out float depth_length)
{
    BoundingSphere bounding_sphere = Frustum_bounding_sphere(CSM_camera, level);

    vec3 center = bounding_sphere.center - light.direction*bounding_sphere.radius;
    float back_offset = 0;
    if (light.max_back_offset > dot(center, -light.direction))
    {
        center = bounding_sphere.center - light.direction*(light.max_back_offset - dot(bounding_sphere.center, -light.direction));
        back_offset = dot(center, -light.direction) - dot(bounding_sphere.center, -light.direction) - bounding_sphere.radius;
    }

    vec2 meters_per_pixel = 2*bounding_sphere.radius / textureSize(sampler2DArray(light.depth_map_handle), 0).xy;
    quat light_quat = quat_conj(light.abs_orientation);
    vec3 center_view = quat_apply(light_quat, center);
    center_view.xz = round(center_view.xz / meters_per_pixel)*meters_per_pixel;

    vec3 view_coord = quat_apply(light_quat, world_coord) - center_view;
    vec4 NDC_coord = vec4(0, 0, 0, 1);
    
    NDC_coord.x = view_coord.x/bounding_sphere.radius;
    NDC_coord.y = view_coord.z/bounding_sphere.radius;
    NDC_coord.z = 2*view_coord.y/(back_offset + 2*bounding_sphere.radius) - 1;
    depth_length = back_offset + 2*bounding_sphere.radius;

    return NDC_coord;
}

vec4 world_to_lightNDC(DirLight light, Camera CSM_camera, int level, vec3 world_coord)
{
    float depth_length = 0;
    return world_to_lightNDC(light, CSM_camera, level, world_coord, depth_length);
}

float _get_PCF_value(DirLight light, Camera CSM_camera, int level, vec3 frag_pos, vec3 frag_normal, float PCF_width, out int total_count, inout int rand_seed)
{
    float depth_length = 0;
    vec4 light_NDC = world_to_lightNDC(light, CSM_camera, level, frag_pos, depth_length);
    float self_depth = (light_NDC.z / light_NDC.w + 1) / 2;

    BoundingSphere bounding_sphere = Frustum_bounding_sphere(CSM_camera, level);
    ivec2 tex_size = textureSize(sampler2DArray(light.depth_map_handle), 0).xy;
    float beta = acos(max(0, dot(frag_normal, -light.direction)));
    float bias = (1+ceil(0.5*PCF_width)) * 2 * bounding_sphere.radius / max(tex_size.x, tex_size.y) * clamp(tan(beta), 0.2, 10.0);
    bias /= depth_length;
    self_depth -= bias;

    vec3 depth_map_tex_coord;
    depth_map_tex_coord.xy = (light_NDC.xy / light_NDC.w + 1) / 2;
    depth_map_tex_coord.z = level;

    vec2 dst = 1.0 / tex_size;
    float ds = dst.s;
    float dt = dst.t;
    int n_samples = 10;

    int not_occ_count = 0;
    total_count = 0;
    for (int i = 0; i < n_samples; i++)
    {
        vec2 rand_result = rand2(frag_pos, rand_seed)-0.5;
        float s = depth_map_tex_coord.s + rand_result.s * PCF_width * ds;
        float t = depth_map_tex_coord.t + rand_result.t * PCF_width * dt;
        if (s < 0 || s > 1 || t < 0 || t > 1)
        {
            continue;
        }

        float sample_depth = max(texture(sampler2DArray(light.depth_map_handle), vec3(s, t, level)).r, 0.0);
        not_occ_count += (sample_depth > self_depth ? 1 : 0);
        total_count += 1;
    }

    float visibility = 1;
    if (total_count > 0)
    {
        visibility = 1.0*not_occ_count/total_count;
    }
    return visibility;
}

float PCF(DirLight light, Camera CSM_camera, vec3 frag_pos, vec3 frag_normal)
{
    float level = locate_CSM_level(CSM_camera, frag_pos);
    int leveli = int(level);
    float level_rear = level - leveli;

    int rand_seed = 0;
    int total_count = 0;
    float visibility = _get_PCF_value(light, CSM_camera, leveli, frag_pos, frag_normal, 7, total_count, rand_seed);
    if (leveli < CSM_camera.CSM_levels)
    {
        int total_count2 = 0;
        float visibility2 = _get_PCF_value(light, CSM_camera, leveli+1, frag_pos, frag_normal, 7, total_count2, rand_seed);
        float weight1 = total_count*(1-level_rear);
        float weight2 = total_count2*level_rear;
        float weight_sum = weight1 + weight2;
        if (weight_sum > 1E-6)
        {
            weight1 /= weight_sum;
            weight2 /= weight_sum;
            visibility = weight1*visibility + weight2*visibility2;
        }
    }
    
    return visibility;
}

#endif