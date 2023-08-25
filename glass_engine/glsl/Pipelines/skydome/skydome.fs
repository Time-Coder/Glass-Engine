#version 460 core

in vec2 frag_tex_coord;
in vec3 world_coord;
out vec4 frag_color;

#include "../../include/fog.glsl"
#include "../../include/Camera.glsl"

uniform sampler2D skydome_map;
uniform Camera camera;
uniform Fog fog;

void main()
{
    frag_color = textureLod(skydome_map, frag_tex_coord, 0);
    frag_color.rgb = fog_apply(fog, frag_color.rgb, camera.abs_position, world_coord);
}