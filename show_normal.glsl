vec4 post_process(sampler2D screen_image, vec2 tex_coord)
{
    vec3 normal = world_normal_of(tex_coord);

    vec4 color;
    color.rgb = (normal + 1.0)/2.0;
    color.a = 1;
    return color;
}