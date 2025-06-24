#ifndef _TEX_COORD_GLSL_
#define _TEX_COORD_GLSL_

#include "Material.glsl"

void transform_tex_coord(Material material, Material back_material, vec3 tex_coord, out vec3 new_tex_coord, out vec3 back_tex_coord)
{
    new_tex_coord = tex_coord;
    new_tex_coord.st *= material.st_scale;
    float st_angle_rad = material.st_rotation / 180.0 * PI;
    new_tex_coord.st = mat2(
        cos(st_angle_rad), sin(st_angle_rad),
        -sin(st_angle_rad), cos(st_angle_rad)
    ) * new_tex_coord.st;
    new_tex_coord.st += material.st_offset;

    back_tex_coord = tex_coord;
    back_tex_coord.st *= back_material.st_scale;
    st_angle_rad = back_material.st_rotation / 180.0 * PI;
    back_tex_coord.st = mat2(
        cos(st_angle_rad), sin(st_angle_rad),
        -sin(st_angle_rad), cos(st_angle_rad)
    ) * back_tex_coord.st;
    back_tex_coord.st += back_material.st_offset;
}

#endif