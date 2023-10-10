#version 430 core

in vec2 tex_coord;
out vec4 out_color;

uniform vec3 iResolution; // viewport resolution (in pixels)
uniform float iTime; // shader playback time (in seconds)
uniform float iTimeDelta; // render time (in seconds)
uniform float iFrameRate; // shader frame rate
uniform int iFrame; // shader playback frame
uniform float iChannelTime[4]; // channel playback time (in seconds)
uniform vec3 iChannelResolution[4]; // channel resolution (in pixels)
uniform vec4 iMouse; // mouse pixel coords. xy: current (if MLB down), zw: click
uniform sampler2D iChannel0, iChannel1, iChannel2, iChannel3; // input channel. XX = 2D/Cube
uniform vec4 iDate; // (year, month, day, time in seconds)
uniform float iSampleRate; // sound sample rate (i.e., 44100)

#include "{file_name}"

void main()
{
    vec2 frag_coord = tex_coord * iResolution.xy;
    mainImage(out_color, frag_coord);
}