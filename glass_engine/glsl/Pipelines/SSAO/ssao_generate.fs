#version 460 core

#include "../../include/Camera.glsl"
#include "../../include/math.glsl"

in vec2 tex_coord;
out float SSAO_factor;

uniform sampler2D view_pos_alpha_map;
uniform sampler2D view_normal_map;
uniform Camera camera;

uniform float SSAO_radius;
uniform int SSAO_samples;
uniform float SSAO_power;

void main()
{
    int rand_seed = 0;

    vec3 view_pos = texture(view_pos_alpha_map, tex_coord).xyz;
    vec3 view_normal = texture(view_normal_map, tex_coord).xyz;
    if (length(view_pos) < 1E-6 || length(view_normal) < 1E-6)
    {
        SSAO_factor = 0;
        return;
    }

    vec3 rand_vec = normalize(rand_vec3(tex_coord, rand_seed));
    do
    {
        rand_vec = normalize(rand_vec3(tex_coord, rand_seed));
    } while(hasnan(rand_vec) || length(cross(rand_vec, view_normal)) < 1E-6);
    vec3 view_tangent = normalize(cross(rand_vec, view_normal));
    vec3 view_bitangent = normalize(cross(view_normal, view_tangent));
    mat3 view_TBN = mat3(view_tangent, view_bitangent, view_normal);

    float occlulated_samples = 0;
    float PI = acos(-1);
    for(int i = 0; i < SSAO_samples; i++)
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

        vec3 sample_view = view_pos + SSAO_radius * view_TBN * vec3(x, y, z);
        float sample_depth = sample_view.y;

        vec4 sample_NDC = view_to_NDC(camera, sample_view);
        vec2 sample_tex_coord = 0.5*(sample_NDC.xy/sample_NDC.w + 1);
        if (sample_tex_coord.x < 0 || sample_tex_coord.x > 1 ||
            sample_tex_coord.y < 0 || sample_tex_coord.y > 1)
        {
            continue;
        }

        vec4 view_pos_alpha_of_same_tex_coord = texture(view_pos_alpha_map, sample_tex_coord);
        vec3 view_pos_of_same_tex_coord = view_pos_alpha_of_same_tex_coord.xyz;
        float alpha = view_pos_alpha_of_same_tex_coord.a;
        if (length(view_pos_of_same_tex_coord) < 1E-6)
        {
            continue;
        }
        float depth_of_same_tex_coord = view_pos_of_same_tex_coord.y;

        if(sample_depth > depth_of_same_tex_coord)
        {
            occlulated_samples += alpha * soft_step(length(sample_view - view_pos)/length(view_pos_of_same_tex_coord - sample_view)-1+0.1, 0.1);
        }
    }
    SSAO_factor = 1 - pow(1-occlulated_samples/SSAO_samples, SSAO_power);
}