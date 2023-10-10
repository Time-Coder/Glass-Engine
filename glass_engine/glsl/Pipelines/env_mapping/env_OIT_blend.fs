
#version 430 core

in TexCoord
{
    vec2 tex_coord;
} fs_in;

out vec4 frag_color;

#include "../../include/OIT.glsl"
#include "../../include/sampling.glsl"

uniform samplerCube opaque_color_map;
uniform samplerCube accum_map;
uniform samplerCube reveal_map;

void main()
{
    float theta = PI*(1.5 - 2*fs_in.tex_coord.x);
    float phi = PI*(fs_in.tex_coord.y-0.5);

    vec3 cube_tex_coord;
    cube_tex_coord.x = cos(phi)*cos(theta);
    cube_tex_coord.y = cos(phi)*sin(theta);
    cube_tex_coord.z = sin(phi);
    cube_tex_coord = quat_apply(quat(cos45, sin45, 0, 0), cube_tex_coord);

    vec4 opaque_color = textureColor(opaque_color_map, cube_tex_coord);
    vec4 accum = texture(accum_map, cube_tex_coord);
    float reveal = texture(reveal_map, cube_tex_coord).r;
    if (hasinf(accum.rgb))
    {
        accum.rgb = vec3(accum.a);
    }
    vec3 transparent_color = accum.rgb / max(accum.a, 1E-6);
    float alpha = exp(reveal);
    frag_color.rgb = mix(transparent_color, opaque_color.rgb, alpha);
    frag_color.a = 1-(1-opaque_color.a)*alpha;
}