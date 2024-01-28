#version 430 core

in vec2 tex_coord;
out vec4 frag_color;

#include "../include/Camera.glsl"
#include "../include/sampling.glsl"

uniform float iTime; // shader playback time (in seconds)
uniform float iTimeDelta; // render time (in seconds)
uniform float iFrameRate; // shader frame rate
uniform int iFrame; // shader playback frame
uniform vec4 iDate; // (year, month, day, time in seconds)

uniform sampler2D screen_image;
uniform sampler2D view_pos_map;
uniform sampler2D view_normal_map;
uniform sampler2D depth_map;
uniform Camera camera;

vec3 view_pos_of(vec2 tex_coord)
{
    if (textureValid(view_pos_map))
    {
        return textureLod(view_pos_map, tex_coord, 0).rgb;
    }
    
    return screen_to_view(camera, vec3(tex_coord, textureLod(depth_map, tex_coord, 0).r));
}

vec3 world_pos_of(vec2 tex_coord)
{
    return view_to_world(camera, view_pos_of(tex_coord));
}

vec3 view_normal_of(vec2 tex_coord)
{
    if (textureValid(view_normal_map))
    {
        return textureLod(view_normal_map, tex_coord, 0).rgb;
    }

    vec3 view_pos = view_pos_of(tex_coord);
    vec3 dir1 = dFdx(view_pos);
    vec3 dir2 = dFdy(view_pos);
    vec3 normal = cross(dir1, dir2);
    float len_normal = length(normal);
    if (len_normal < 1E-6)
    {
        return vec3(0, 0, 0);
    }
    else
    {
        return (normal / len_normal);
    }
}

vec3 world_normal_of(vec2 tex_coord)
{
    vec3 view_normal = view_normal_of(tex_coord);
    return view_dir_to_world(camera, view_normal);
}

vec2 view_pos_to_tex_coord(vec3 view_pos)
{
    vec4 NDC = view_to_NDC(camera, view_pos);
    return 0.5*(NDC.xy/NDC.w + 1);
}

vec2 world_pos_to_tex_coord(vec3 world_pos)
{
    vec4 NDC = Camera_project(camera, world_pos);
    return 0.5*(NDC.xy/NDC.w + 1);
}

#include FILE_NAME

void main()
{ 
    frag_color = post_process(screen_image, tex_coord);
}