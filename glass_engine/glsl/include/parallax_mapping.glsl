#ifndef _PARALLAX_MAPPING_GLSL_
#define _PARALLAX_MAPPING_GLSL_

#include "Material.glsl"
#include "limits.glsl"
#include "sampling.glsl"
#include "Camera.glsl"


void parallax_mapping(Camera camera, sampler2D height_map, float height_scale, mat3 world_TBN, inout vec3 world_pos, inout vec2 frag_tex_coord)
{
    vec3 view_dir = world_pos - camera.abs_position;
    float view_dir_length = length(view_dir);
    view_dir = view_dir / view_dir_length;
    mat3 view_TBN = world_TBN_to_view(camera, world_TBN);
    mat3 inv_TBN = inverse(view_TBN);
    vec3 view_dir_in_tbn = inv_TBN * view_dir;

    float cos_theta = dot(-view_dir, view_TBN[2]);
    float half_dmax = 0.5 * height_scale;
    float max_d = half_dmax/cos_theta + 0.01;
    float delta_d = max(half_dmax/10, max_d/100);
    
    float lower_d = -min(max_d, view_dir_length);
    float upper_d = lower_d;

    float z_line = -lower_d*cos_theta;
    vec2 tex_coord = frag_tex_coord + lower_d*view_dir_in_tbn.st;
    float z_bump = height_scale * (texture(height_map, tex_coord).r-0.5);

    float z_line_lower = z_line;
    float z_bump_lower = z_bump;
    float z_line_upper = z_line;
    float z_bump_upper = z_bump;
    
    bool is_line_high = (z_line > z_bump);
    bool should_break = false;
    while (!should_break && (z_line > z_bump) == is_line_high)
    {
        lower_d = upper_d;
        upper_d += delta_d;
        if (upper_d > max_d)
        {
            upper_d = max_d;
            should_break = true;
        }
        z_line = -upper_d*cos_theta;
        tex_coord = frag_tex_coord + upper_d*view_dir_in_tbn.st;
        z_bump = height_scale * (texture(height_map, tex_coord).r-0.5);
        z_line_upper = z_line;
        z_bump_upper = z_bump;
    }

    int times = 0;
    float middle_d = (lower_d*(z_bump_upper - z_line_upper) + upper_d*(z_line_lower - z_bump_lower)) / (z_bump_upper -  z_line_upper + z_line_lower - z_bump_lower);
    while (upper_d - lower_d > 1E-6 && times < 20)
    {
        middle_d = (lower_d*(z_bump_upper - z_line_upper) + upper_d*(z_line_lower - z_bump_lower)) / (z_bump_upper -  z_line_upper + z_line_lower - z_bump_lower);
        z_line = -middle_d*cos_theta;
        tex_coord = frag_tex_coord + middle_d*view_dir_in_tbn.st;
        z_bump = height_scale * (texture(height_map, tex_coord).r-0.5);
        if ((z_line > z_bump) == is_line_high)
        {
            lower_d = middle_d;
            z_line_lower = z_line;
            z_bump_lower = z_bump;
        }
        else
        {
            upper_d = middle_d;
            z_line_upper = z_line;
            z_bump_upper = z_bump;
        }
        times++;
    }

    frag_tex_coord = tex_coord;
    world_pos = world_pos + middle_d*view_dir;
}

void change_geometry(Camera camera, Material material, inout vec2 tex_coord, inout mat3 world_TBN, inout vec3 world_pos)
{
    world_TBN[2] = normalize(world_TBN[2]);
    if (!gl_FrontFacing)
    {
        world_TBN[2] = -world_TBN[2];
    }

    if (hasnan(world_TBN))
    {
        return;
    }

    if (textureValid(material.height_map))
    {
        parallax_mapping(camera, material.height_map, material.height_scale, world_TBN, world_pos, tex_coord);
    }

    if (textureValid(material.normal_map))
    {
        vec3 normal_in_tbn = 2*texture(material.normal_map, tex_coord).rgb-1;
        float len_normal = length(normal_in_tbn);
        if (len_normal < 1E-6)
        {
            normal_in_tbn = vec3(0);
        }
        else
        {
            normal_in_tbn /= len_normal;
        }

        world_TBN[0] = material.height_scale/0.05 * world_TBN[0]/dot(world_TBN[0], world_TBN[0]);
        world_TBN[1] = material.height_scale/0.05 * world_TBN[1]/dot(world_TBN[1], world_TBN[1]);
        world_TBN[2] = world_TBN * normal_in_tbn;
        
        len_normal = length(world_TBN[2]);
        if (len_normal < 1E-6)
        {
            world_TBN[2] = vec3(0);
        }
        else
        {
            world_TBN[2] /= len_normal;
        }
    }
}

#endif