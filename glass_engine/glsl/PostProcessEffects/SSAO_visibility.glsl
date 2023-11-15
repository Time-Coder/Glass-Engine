#include "../include/random.glsl"
#include "../include/limits.glsl"

uniform float radius;
uniform int samples;
uniform float power;

vec4 post_process(sampler2D screen_image, vec2 tex_coord)
{
    if (radius <= 1E-4 || samples <= 0 || power <= 1E-6)
    {
        return vec4(1);
    }

    int rand_seed = 0;

    vec3 view_pos = view_pos_of(tex_coord);
    vec3 view_normal = view_normal_of(tex_coord);
    if (length(view_pos) < 1E-6 || length(view_normal) < 1E-6)
    {
        return vec4(1);
    }

    vec3 rand_vec = normalize(rand3(tex_coord, rand_seed));
    do
    {
        rand_vec = normalize(rand3(tex_coord, rand_seed));
    } while(hasnan(rand_vec) || length(cross(rand_vec, view_normal)) < 1E-6);
    vec3 view_tangent = normalize(cross(rand_vec, view_normal));
    vec3 view_bitangent = normalize(cross(view_normal, view_tangent));
    mat3 view_TBN = mat3(view_tangent, view_bitangent, view_normal);

    float occlulated_samples = 0;
    for(int i = 0; i < samples; i++)
    {
        float radius = rand(tex_coord, rand_seed);
        float phi = 0.5*PI*rand(tex_coord, rand_seed);
        while(radius * sin(phi) < 1E-3)
        {
            radius = rand(tex_coord, rand_seed);
            phi = 0.5*PI*rand(tex_coord, rand_seed);
        }
        float theta = 2*PI*rand(tex_coord, rand_seed);

        float x = radius*cos(phi)*cos(theta);
        float y = radius*cos(phi)*sin(theta);
        float z = radius*sin(phi);

        vec3 sample_view_pos = view_pos + radius * view_TBN * vec3(x, y, z);
        float sample_depth = sample_view_pos.y;

        vec2 sample_tex_coord = view_pos_to_tex_coord(sample_view_pos);
        if (sample_tex_coord.x < 0 || sample_tex_coord.x > 1 ||
            sample_tex_coord.y < 0 || sample_tex_coord.y > 1)
        {
            continue;
        }

        vec3 view_pos_of_same_tex_coord = view_pos_of(sample_tex_coord);
        if (length(view_pos_of_same_tex_coord) < 1E-6)
        {
            continue;
        }
        float depth_of_same_tex_coord = view_pos_of_same_tex_coord.y;

        if (sample_depth > depth_of_same_tex_coord)
        {
            occlulated_samples += soft_step(length(sample_view_pos - view_pos)/length(view_pos_of_same_tex_coord - sample_view_pos)-0.9, 0.1);
        }
    }
    return vec4(vec3(pow(1-occlulated_samples/samples, power)), 1.0);
}
