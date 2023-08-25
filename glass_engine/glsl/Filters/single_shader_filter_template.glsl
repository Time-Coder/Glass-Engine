#version 460 core

in TexCoord
{
    vec2 tex_coord;
} fs_in;

out vec4 frag_color;

uniform float iTime; // shader playback time (in seconds)
uniform float iTimeDelta; // render time (in seconds)
uniform float iFrameRate; // shader frame rate
uniform int iFrame; // shader playback frame
uniform vec4 iDate; // (year, month, day, time in seconds)
uniform sampler2D screen_image;

#include "{file_name}"

void main()
{ 
    frag_color = getColor(screen_image, fs_in.tex_coord);
}