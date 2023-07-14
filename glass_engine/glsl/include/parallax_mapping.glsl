#ifndef _PARALLAX_MAPPING_GLSL__
#define _PARALLAX_MAPPING_GLSL__

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

#endif