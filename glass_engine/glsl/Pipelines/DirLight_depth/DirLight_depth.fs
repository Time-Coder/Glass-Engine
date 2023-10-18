#version 430 core

in GeometryOut
{
    vec4 color;
    vec4 back_color;
    vec3 tex_coord;
    flat int visible;
} fs_in;

#include "../../include/InternalMaterial.glsl"

uniform Material material;
uniform Material back_material;

void main()
{
    if (fs_in.visible == 0)
    {
        discard;
    }

    InternalMaterial internal_material = 
        fetch_internal_material(
            (gl_FrontFacing ? fs_in.color : fs_in.back_color),
            (gl_FrontFacing ? material : back_material),
            fs_in.tex_coord.st
        );

    if (internal_material.opacity < 1E-6)
    {
        discard;
    }
}