#if USE_POINT_LIGHT && USE_POINT_LIGHT_SHADOW

#include "PointLight.glsl"

float PCF(PointLight light, vec3 frag_pos, vec3 frag_normal)
{
    vec3 depth_map_tex_coord = frag_pos - light.abs_position;
    float self_depth = length(depth_map_tex_coord);
    if (self_depth < 0.1)
    {
        return 1.0;
    }

    depth_map_tex_coord /= self_depth;

    float max_angle_shift = atan(0.05/self_depth);
    float beta = acos(max(0, dot(frag_normal, -depth_map_tex_coord)));
    float bias = 0.05 * clamp(tan(beta), 0.2, 10.0);
    self_depth -= bias;

    int n_samples = 10;
    int rand_seed = 0;
    int not_occ_count = 0;
    int total_count = 0;
    quat correction_quat = quat(cos45, sin45, 0, 0);
    for (int i = 0; i < n_samples; i++)
    {
        vec3 sample_dir = rand3_near(depth_map_tex_coord, max_angle_shift, rand_seed);
        sample_dir = quat_apply(correction_quat, sample_dir);
        float sample_depth = max(texture(samplerCube(light.depth_map_handle), sample_dir).r, 0.0);
        sample_depth *= light.coverage;
        not_occ_count += (sample_depth > self_depth ? 1 : 0);
        total_count += 1;
    }

    return 1.0*not_occ_count/total_count;
}

#endif