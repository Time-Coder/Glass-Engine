#version 460 core

layout(location=0) out vec4 frag_color;
layout(location=3) out vec3 view_pos;
layout(location=4) out vec3 view_normal;

in vec3 tex_coord;
in vec3 world_coord;

#include "../../include/fog.glsl"
#include "../../include/sampling.glsl"
#include "../../include/Camera.glsl"

uniform samplerCube skybox_map;
uniform Camera camera;
uniform Fog fog;

void main()
{
    frag_color = textureColor(skybox_map, tex_coord);
    frag_color.rgb = fog_apply(fog, frag_color.rgb, camera.abs_position, world_coord);

    view_pos = vec3(0);
    view_normal = vec3(0);
}