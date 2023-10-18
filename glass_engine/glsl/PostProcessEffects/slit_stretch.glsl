float triWave(float x)
{
    return(abs(mod(x-10.0, 20.0)-10.0)+1.0);
}

vec4 post_process(sampler2D screen_image, vec2 tex_coord)
{
    vec2 uv = 2.0*(tex_coord-0.5);

    vec2 uvR = uv*(1.0-length(uv)/(triWave(iTime*5.0)));
    vec2 uvG = uv*(1.0-length(uv)/(triWave(iTime*5.0+0.1)));
    vec2 uvB = uv*(1.0-length(uv)/(triWave(iTime*5.0+0.2)));

    uvR = uvR/2.0 + 0.5;
    uvG = uvG/2.0 + 0.5;
    uvB = uvB/2.0 + 0.5;

    float R = max(texture(screen_image, uvR).r, 0.0);
    float G = max(texture(screen_image, uvG).g, 0.0);
    float B = max(texture(screen_image, uvB).b, 0.0);

    return vec4(R, G, B, 1.0);
}