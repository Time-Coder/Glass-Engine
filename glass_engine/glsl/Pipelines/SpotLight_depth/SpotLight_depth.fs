#version 460 core

#extension GL_ARB_bindless_texture : enable

in flat int visible;
in vec3 world_pos;

#include "../../Lights/SpotLight.glsl"
#include "../../include/Material.glsl"

uniform SpotLight spot_light;
uniform Material material;
uniform Material back_material;

void main()
{
    if (!fs_in.visible)
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

    float distance_to_light = length(spot_light.abs_position - world_pos);
    gl_FragDepth = distance_to_light / spot_light.coverage;
}