#version 430 core

layout(location=0) out vec4 frag_color;
layout(location=3) out vec3 view_pos;
layout(location=4) out vec3 view_normal;

in vec3 tex_coord;
in vec3 view_dir;

#include "../../include/fog.glsl"
#include "../../include/Camera.glsl"

uniform samplerCube skybox_map;
uniform float sky_distance;
uniform Camera camera;

#if USE_FOG
uniform Fog fog;
#endif

void main()
{
    frag_color = max(texture(skybox_map, tex_coord), 0.0);

#if USE_FOG
    frag_color.rgb = fog_apply(fog, frag_color.rgb, sky_distance);
#endif

    view_pos = sky_distance * normalize(view_dir);
    view_normal = vec3(0);
}