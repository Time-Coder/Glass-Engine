uniform sampler2D LUT;
uniform float contribute;

vec4 post_process(sampler2D screen_image, vec2 tex_coord)
{
    ivec2 LUT_size = textureSize(LUT, 0);
    int block_width = 0;
    ivec2 block_shape = ivec2(0);
    if (LUT_size.x == LUT_size.y)
    {
        block_width = int(pow(LUT_size.x, 2.0/3.0));
    }
    else
    {
        block_width = min(LUT_size.x, LUT_size.y);
    }
    block_shape = ivec2(block_width);

    ivec2 block_size = LUT_size / block_shape;
    vec2 block_ratio = vec2(block_shape) / vec2(LUT_size);
    int n_blocks = block_size.x * block_size.y;

    vec4 color = clamp(textureLod(screen_image, tex_coord, 0), 0.0, 1.0);
    vec2 dxy = color.rg * (block_ratio - 1.0/LUT_size) + 0.5/LUT_size;

    float i_blockf = color.b * (n_blocks - 1);
    int i_block = int(i_blockf);
    float rear = i_blockf - i_block;

    ivec2 block_index = ivec2(i_block % block_size.x, i_block / block_size.x);
    vec2 start_xy = block_index * block_ratio;
    vec2 new_tex_coord = start_xy + dxy;
    vec4 new_color = textureLod(LUT, vec2(new_tex_coord.x, 1-new_tex_coord.y), 0);

    if (i_block < n_blocks-1)
    {
        block_index = ivec2((i_block+1) % block_size.x, (i_block+1) / block_size.x);
        start_xy = block_index * block_ratio;
        new_tex_coord = start_xy + dxy;
        new_color = mix(new_color, textureLod(LUT, vec2(new_tex_coord.x, 1-new_tex_coord.y), 0), rear);
    }

    return mix(color, new_color, contribute);
}