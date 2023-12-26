#version 430 core

#if USE_BINDLESS_TEXTURE
#extension GL_ARB_bindless_texture : require
#endif

in GeometryOut
{
    vec3 world_pos;
    vec4 color;
    vec4 back_color;
    vec3 tex_coord;
    flat int visible;
} fs_in;

#include "../../Lights/PointLight.glsl"
#include "../../include/InternalMaterial.glsl"

uniform PointLight point_light;
uniform Material material;
uniform Material back_material;

void main()
{
    if (fs_in.visible == 0)
    {
        discard;
    }

    InternalMaterial internal_material;
    if (gl_FrontFacing)
    {
        internal_material = fetch_internal_material(
            fs_in.color, material, fs_in.tex_coord.st
        );
    }
    else
    {
        internal_material = fetch_internal_material(
            fs_in.back_color, back_material, fs_in.tex_coord.st
        );
    }

    if (internal_material.opacity < 1E-6)
    {
        discard;
    }

    float distance_to_light = length(point_light.abs_position - fs_in.world_pos);
    gl_FragDepth = distance_to_light / point_light.coverage;
}