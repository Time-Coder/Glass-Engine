#ifndef _PARALLAX_MAPPING_GLSL__
#define _PARALLAX_MAPPING_GLSL__

#include "Material.glsl"

void parallax_mapping(sampler2D height_map, float height_scale, mat3 view_TBN, inout vec3 view_pos, inout vec2 frag_tex_coord)
{
    vec3 view_dir = view_pos;
    float to_camera_distance = length(view_dir);
    view_dir = view_dir / to_camera_distance;
    mat3 inv_TBN = inverse(view_TBN);
    vec3 view_dir_in_tbn = inv_TBN * view_dir;

    float cos_theta = dot(-view_dir, view_TBN[2]);
    float half_dmax = 0.5 * height_scale;
    float max_d = half_dmax/cos_theta + 0.01;
    float delta_d = max(half_dmax/10, max_d/100);
    
    float lower_d = -min(max_d, to_camera_distance);
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
    while(!should_break && (z_line > z_bump) == is_line_high)
    {
        lower_d = upper_d;
        upper_d += delta_d;
        if(upper_d > max_d)
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
    float middle_d;
    while(upper_d - lower_d > 1E-6 && times < 20)
    {
        // (lower_d, z_line_lower) -> (upper_d, z_line_upper)
        // (lower_d, z_bump_lower) -> (upper_d, z_bump_upper)

        middle_d = (lower_d*(z_bump_upper - z_line_upper) + upper_d*(z_line_lower - z_bump_lower)) / (z_bump_upper -  z_line_upper + z_line_lower - z_bump_lower);
        // middle_d = 0.5*(lower_d + upper_d);

        z_line = -middle_d*cos_theta;
        tex_coord = frag_tex_coord + middle_d*view_dir_in_tbn.st;
        z_bump = height_scale * (texture(height_map, tex_coord).r-0.5);
        if((z_line > z_bump) == is_line_high)
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
    view_pos = view_pos + middle_d*view_dir;
}

void change_geometry(Material material, inout vec3 view_pos, inout vec3 view_normal,
                     inout vec2 frag_tex_coord, mat3 view_TBN)
{
    if (hasnan(view_TBN))
    {
        return;
    }

    // 视差贴图
    if (material.use_height_map)
    {
        parallax_mapping(
            material.height_map, material.height_scale, view_TBN,
            view_pos, frag_tex_coord);
    }

    // 法向量贴图
    if (material.use_normal_map)
    {
        vec3 normal_in_tbn = 2*texture(material.normal_map, frag_tex_coord).rgb-1;
        float len_normal = length(normal_in_tbn);
        if (len_normal < 1E-6) normal_in_tbn = vec3(0, 0, 0);
        else normal_in_tbn /= len_normal;
        
        vec3 view_tangent = view_TBN[0];
        view_tangent = material.height_scale/0.05 * view_tangent/dot(view_tangent, view_tangent);

        vec3 view_bitangent = view_TBN[1];
        view_bitangent = material.height_scale/0.05 * view_bitangent/dot(view_bitangent, view_bitangent);

        view_normal = mat3(view_tangent, view_bitangent, view_normal) * normal_in_tbn;
        len_normal = length(view_normal);
        if (len_normal < 1E-6) view_normal = vec3(0, 0, 0);
        else view_normal /= len_normal;
    }
}

#endif