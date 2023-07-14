vec4 getColor(sampler2D screen_image, vec2 tex_coord)
{
    return vec4(vec3(1.0 - texture(screen_image, tex_coord)), 1.0);
}