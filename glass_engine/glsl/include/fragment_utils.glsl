#ifndef _FRAGMENT_UTILS_GLSL__
#define _FRAGMENT_UTILS_GLSL__

#include "Material.glsl"
#include "Camera.glsl"
#include "parallax_mapping.glsl"

void change_geometry(Material material, inout vec3 view_pos, inout vec3 view_normal,
                     inout vec2 frag_tex_coord, mat3 view_TBN)
{
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