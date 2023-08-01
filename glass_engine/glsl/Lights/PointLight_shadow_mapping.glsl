#ifndef _POINT_LIGHT_SHADOW_MAPPING_GLSL__
#define _POINT_LIGHT_SHADOW_MAPPING_GLSL__

float SSM(PointLight light, vec3 frag_pos, vec3 frag_normal)
{
    vec3 depth_map_tex_coord = frag_pos - light.abs_position;
    float self_depth = length(depth_map_tex_coord);
    if (self_depth < 0.1)
    {
        return 1;
    }
    depth_map_tex_coord /= self_depth;
    float bias = max(0.005 * (1.0 + dot(frag_normal, depth_map_tex_coord)), 0.002);
    self_depth -= bias;

    depth_map_tex_coord = quat_apply(quat(cos45, sin45, 0, 0), depth_map_tex_coord);
    float sample_depth = texture(samplerCube(light.depth_map_handle), depth_map_tex_coord).r;
    sample_depth *= light.coverage;

    float visibility = ((sample_depth > self_depth) ? 1.0 : 0.0);
    return visibility;
}

float PCF(PointLight light, vec3 frag_pos, vec3 frag_normal)
{
    vec3 depth_map_tex_coord = frag_pos - light.abs_position;
    float self_depth = length(depth_map_tex_coord);
    if (self_depth < 0.1)
    {
        return 1;
    }
    depth_map_tex_coord /= self_depth;

    float bias = max(0.02 * (1.0 + dot(frag_normal, depth_map_tex_coord)), 0.008);
    self_depth -= 3*bias;

    float max_angle_shift = 0.01;
    int n_samples = 16;

    int rand_seed = 0;
    int not_occ_count = 0;
    int total_count = 0;
    quat correction_quat = quat(cos45, sin45, 0, 0);
    for (int i = 0; i < n_samples; i++)
    {
        vec3 sample_dir = rand3_near(depth_map_tex_coord, max_angle_shift, rand_seed);
        sample_dir = quat_apply(correction_quat, sample_dir);

        float sample_depth = texture(samplerCube(light.depth_map_handle), sample_dir).r;
        sample_depth *= light.coverage;

        not_occ_count += (sample_depth > self_depth ? 1 : 0);
        total_count += 1;
    }
    return 1.0*not_occ_count/total_count;
}

#endif