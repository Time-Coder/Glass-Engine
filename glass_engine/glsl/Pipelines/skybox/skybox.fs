#version 460 core

out vec4 frag_color;
in vec3 tex_coord;
in vec3 world_coord;

#include "../../include/fog.glsl"
#include "../../include/Camera.glsl"

uniform samplerCube skybox_map;
uniform Camera camera;
uniform Fog fog;

void main()
{
    frag_color = texture(skybox_map, tex_coord);
    frag_color.rgb = fog_apply(fog, frag_color.rgb, camera.abs_position, world_coord);
}