#version 460 core

in vec2 frag_tex_coord;
in vec3 view_dir;

layout(location=0) out vec4 frag_color;
layout(location=3) out vec3 view_pos;
layout(location=4) out vec3 view_normal;

#include "../../include/fog.glsl"
#include "../../include/sampling.glsl"
#include "../../include/Camera.glsl"

uniform sampler2D skydome_map;
uniform float sky_distance;
uniform Camera camera;
uniform Fog fog;

void main()
{
    frag_color = textureColorLod(skydome_map, frag_tex_coord, 0);
    frag_color.rgb = fog_apply(fog, frag_color.rgb, sky_distance);

    view_pos = sky_distance * normalize(view_dir);
    view_normal = vec3(0);
}