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

vec4 world_to_lightNDC(DirLight light, Camera camera, int level, vec3 world_coord)
{
    float depth_length = 0;
    return world_to_lightNDC(light, camera, level, world_coord, depth_length);
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

    BoundingSphere bounding_sphere = Frustum_bounding_sphere(camera, level);
    ivec2 tex_size = textureSize(sampler2DArray(light.depth_map_handle), 0).xy;
    float beta = max(0, acos(dot(frag_normal, -light.direction)));
    float bias = 17 * bounding_sphere.radius / max(tex_size.x, tex_size.y) * tan(beta);
    bias /= depth_length;
    self_depth -= bias;

    float sample_depth = texture2DArray(sampler2DArray(light.depth_map_handle), depth_map_tex_coord).r;
    float visibility = ((sample_depth > self_depth-bias) ? 1 : 0);

    return visibility;
}

float _get_PCF_value(DirLight light, Camera camera, int level, vec3 frag_pos, vec3 frag_normal, float PCF_width, inout int rand_seed)
{
    float depth_length = 0;
    vec4 light_NDC = world_to_lightNDC(light, camera, level, frag_pos, depth_length);
    float self_depth = (light_NDC.z / light_NDC.w + 1) / 2;

    BoundingSphere bounding_sphere = Frustum_bounding_sphere(camera, level);
    ivec2 tex_size = textureSize(sampler2DArray(light.depth_map_handle), 0).xy;
    float beta = max(0, acos(dot(frag_normal, -light.direction)));
    float bias = 17 * bounding_sphere.radius / max(tex_size.x, tex_size.y) * tan(beta);
    bias /= depth_length;
    self_depth -= bias;

    vec3 depth_map_tex_coord;
    depth_map_tex_coord.xy = (light_NDC.xy / light_NDC.w + 1) / 2;
    depth_map_tex_coord.z = level;

    vec2 dst = 1.0 / tex_size;
    float ds = dst.s;
    float dt = dst.t;

    int not_occ_count = 0;
    int total_count = 0;
    for (int i = 0; i < 16; i++)
    {
        vec2 rand_result = rand2(frag_pos, rand_seed);
        float s = depth_map_tex_coord.s + rand_result.s*(PCF_width-1) * ds;
        float t = depth_map_tex_coord.t + rand_result.t*(PCF_width-1) * dt;

        float sample_depth = texture2DArray(sampler2DArray(light.depth_map_handle), vec3(s, t, level)).r;
        not_occ_count += (sample_depth > self_depth ? 1 : 0);
        total_count += 1;
    }

    float visibility = 1.0*not_occ_count/total_count;
    return visibility;
}

float PCF(DirLight light, Camera camera, vec3 frag_pos, vec3 frag_normal)
{
    float level = locate_CSM_level(camera, frag_pos);
    int leveli = int(level);
    float level_rear = level - leveli;

    int rand_seed = 0;
    float visibility = _get_PCF_value(light, camera, leveli, frag_pos, frag_normal, 7, rand_seed);
    if (leveli < camera.CSM_levels)
    {
        float visibility2 = _get_PCF_value(light, camera, leveli+1, frag_pos, frag_normal, 7, rand_seed);
        visibility = mix(visibility, visibility2, level_rear);
    }
    
    return visibility;
}

#endif