#ifndef _DIR_LIGHT_SHADOW_MAPPING_GLSL__
#define _DIR_LIGHT_SHADOW_MAPPING_GLSL__

vec4 world_to_lightNDC(DirLight light, Camera camera, int level, vec3 world_coord, out float depth_length)
{
    BoundingSphere bounding_sphere = Frustum_bounding_sphere(camera, level);

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

float SSM(DirLight light, Camera camera, vec3 frag_pos, vec3 frag_normal)
{
    int level = locate_CSM_leveli(camera, frag_pos);
    float depth_length = 0;
    vec4 light_NDC = world_to_lightNDC(light, camera, level, frag_pos, depth_length);
    float self_depth = (light_NDC.z / light_NDC.w + 1) / 2;
    vec3 depth_map_tex_coord;
    depth_map_tex_coord.xy = (light_NDC.xy / light_NDC.w + 1) / 2;
    depth_map_tex_coord.z = level;

    float bias = max(0.005 * (1.0 + dot(frag_normal, light.direction)), 0.002);
    bias /= depth_length;

    float sample_depth = texture2DArray(sampler2DArray(light.depth_map_handle), depth_map_tex_coord).r;
    float visibility = ((sample_depth > self_depth-bias) ? 1 : 0);
    return visibility;
}

float _get_PCF_value(DirLight light, Camera camera, int level, vec3 frag_pos, vec3 frag_normal, float PCF_width, inout int rand_seed)
{
    float depth_length = 0;
    vec4 light_NDC = world_to_lightNDC(light, camera, level, frag_pos, depth_length);
    float self_depth = (light_NDC.z / light_NDC.w + 1) / 2;

    float bias = max(0.02 * (1.0 + dot(frag_normal, light.direction)), 0.008);
    self_depth -= bias;

    vec3 depth_map_tex_coord;
    depth_map_tex_coord.xy = (light_NDC.xy / light_NDC.w + 1) / 2;
    depth_map_tex_coord.z = level;

    vec2 dst = 1.0 / textureSize(sampler2DArray(light.depth_map_handle), 0).st;
    float ds = dst.s;
    float dt = dst.t;

    int not_occ_count = 0;
    int total_count = 0;
    for (int i = 0; i < 16; i++)
    {
        vec2 rand_result = rand2(frag_pos, rand_seed);
        float s = depth_map_tex_coord.s + 0.5*(PCF_width-1)*rand_result.s * ds;
        float t = depth_map_tex_coord.t + 0.5*(PCF_width-1)*rand_result.t * ds;
        float sample_depth = texture2DArray(sampler2DArray(light.depth_map_handle), vec3(s, t, level)).r;
        not_occ_count += (sample_depth > self_depth ? 1 : 0);
        total_count += 1;
    }    
    return 1.0*not_occ_count/total_count;
}

float PCF(DirLight light, Camera camera, vec3 frag_pos, vec3 frag_normal)
{
    float level = locate_CSM_level(camera, frag_pos);
    int leveli = int(level);
    float level_rear = level - leveli;

    int rand_seed = 0;
    float visibility = _get_PCF_value(light, camera, leveli, frag_pos, frag_normal, 9, rand_seed);
    if (leveli < camera.CSM_levels)
    {
        float visibility2 = _get_PCF_value(light, camera, leveli+1, frag_pos, frag_normal, 9, rand_seed);
        visibility = mix(visibility, visibility2, level_rear);
    }
    
    return visibility;
}

float _get_PCSS_value(DirLight light, Camera camera, int level, vec3 frag_pos, vec3 frag_normal, inout int rand_seed)
{
    float depth_length = 0;
    vec4 light_NDC = world_to_lightNDC(light, camera, level, frag_pos, depth_length);
    float self_depth = (light_NDC.z / light_NDC.w + 1) / 2;

    float bias = max(0.02 * (1.0 + dot(frag_normal, light.direction)), 0.008);
    self_depth -= bias;

    vec3 depth_map_tex_coord;
    depth_map_tex_coord.xy = (light_NDC.xy / light_NDC.w + 1) / 2;
    depth_map_tex_coord.z = level;

    ivec2 texture_size = textureSize(sampler2DArray(light.depth_map_handle), 0).xy;
    vec2 dst = 1.0 / texture_size.st;
    float ds = dst.s;
    float dt = dst.t;
    
    int blocker_search_width = 5;
    int num_blockers = 0;
    float sum_blocker_depth = 0;
    for (int i = 0; i < 16; i++)
    {
        vec2 rand_result = rand2(frag_pos, rand_seed);
        float s = depth_map_tex_coord.s + 0.5*(blocker_search_width-1)*rand_result.s * ds;
        float t = depth_map_tex_coord.t + 0.5*(blocker_search_width-1)*rand_result.t * ds;
        float sample_depth = texture2DArray(sampler2DArray(light.depth_map_handle), vec3(s, t, level)).r;
        if(sample_depth < self_depth)
        {
            num_blockers += 1;
            sum_blocker_depth += sample_depth;
        }
    }
    float mean_blocker_depth = sum_blocker_depth / num_blockers;
    if (num_blockers == 0)
    {
        return 1;
    }

    BoundingSphere bounding_sphere = Frustum_bounding_sphere(camera, level);
    vec2 PCF_size = (self_depth/mean_blocker_depth - 1) * (1/depth_length) / (2*bounding_sphere.radius) * texture_size;
    PCF_size.x = max(PCF_size.x, 1);
    PCF_size.y = max(PCF_size.y, 1);

    int not_occ_count = 0;
    int total_count = 0;
    int num_samples = int(4*log(1+PCF_size.x*PCF_size.y));
    for (int i = 0; i < num_samples; i++)
    {
        vec2 rand_result = rand2(frag_pos, rand_seed);
        float s = depth_map_tex_coord.s + 0.5*(PCF_size.x-1)*rand_result.s * ds;
        float t = depth_map_tex_coord.t + 0.5*(PCF_size.y-1)*rand_result.t * ds;
        float sample_depth = texture2DArray(sampler2DArray(light.depth_map_handle), vec3(s, t, level)).r;
        not_occ_count += (sample_depth > self_depth ? 1 : 0);
        total_count += 1;
    }
    return 1.0*not_occ_count/total_count;
}

float PCSS(DirLight light, Camera camera, vec3 frag_pos, vec3 frag_normal)
{
    float level = locate_CSM_level(camera, frag_pos);
    int leveli = int(level);
    float level_rear = level - leveli;

    int rand_seed = 0;
    float visibility = _get_PCSS_value(light, camera, leveli, frag_pos, frag_normal, rand_seed);
    if (leveli < camera.CSM_levels)
    {
        float visibility2 = _get_PCSS_value(light, camera, leveli+1, frag_pos, frag_normal, rand_seed);
        visibility = mix(visibility, visibility2, level_rear);
    }
    
    return visibility;
}

float _get_VSM_value(DirLight light, Camera camera, int level, vec3 frag_pos, vec3 frag_normal)
{
    float depth_length = 0;
    vec4 light_NDC = world_to_lightNDC(light, camera, level, frag_pos, depth_length);
    float self_depth = light_NDC.z / light_NDC.w;

    float bias = max(0.02 * (1.0 + dot(frag_normal, light.direction)), 0.008);
    self_depth -= bias;

    vec3 depth_map_tex_coord;
    depth_map_tex_coord.xy = (light_NDC.xy / light_NDC.w + 1) / 2;
    depth_map_tex_coord.z = level;

    vec2 VSM_values = texture2DArray(sampler2DArray(light.depth_map_handle), depth_map_tex_coord).xy;
    float mean = VSM_values.x;
    float dev = VSM_values.y - mean*mean;
    float delta = self_depth - mean;
    if (self_depth > mean)
    {
        return dev/(dev+delta*delta);
    }
    else
    {
        return 1;
    }
}

float VSM(DirLight light, Camera camera, vec3 frag_pos, vec3 frag_normal)
{
    float level = locate_CSM_level(camera, frag_pos);
    int leveli = int(level);
    float level_rear = level - leveli;

    float visibility = _get_VSM_value(light, camera, leveli, frag_pos, frag_normal);
    // if (leveli < camera.CSM_levels)
    // {
    //     float visibility2 = _get_VSM_value(light, camera, leveli+1, frag_pos, frag_normal);
    //     visibility = mix(visibility, visibility2, level_rear);
    // }
    
    return visibility;
}

float _get_EVSM_value(DirLight light, Camera camera, int level, vec3 frag_pos, vec3 frag_normal)
{
    float depth_length = 0;
    vec4 light_NDC = world_to_lightNDC(light, camera, level, frag_pos, depth_length);
    float self_depth = light_NDC.z / light_NDC.w;

    float bias = max(0.02 * (1.0 + dot(frag_normal, light.direction)), 0.008);
    self_depth -= bias;

    vec3 depth_map_tex_coord;
    depth_map_tex_coord.xy = (light_NDC.xy / light_NDC.w + 1) / 2;
    depth_map_tex_coord.z = level;

    vec4 EVSM_values = texture2DArray(sampler2DArray(light.depth_map_handle), depth_map_tex_coord);
    float mean1 = EVSM_values.x;
    float dev1 = EVSM_values.z - mean1*mean1;
    float mean2 = EVSM_values.y;
    float dev2 = EVSM_values.w - mean2*mean2;
    float delta1 =  exp( 5*self_depth) - mean1;
    float delta2 = -exp(-5*self_depth) - mean2;
    return min(dev1/(dev1-delta1*delta1), dev2/(dev2-delta2*delta2));
}

float EVSM(DirLight light, Camera camera, vec3 frag_pos, vec3 frag_normal)
{
    float level = locate_CSM_level(camera, frag_pos);
    int leveli = int(level);
    float level_rear = level - leveli;

    float visibility = _get_EVSM_value(light, camera, leveli, frag_pos, frag_normal);
    // if (leveli < camera.CSM_levels)
    // {
    //     float visibility2 = _get_VSM_value(light, camera, leveli+1, frag_pos, frag_normal);
    //     visibility = mix(visibility, visibility2, level_rear);
    // }
    
    return visibility;
}

#endif