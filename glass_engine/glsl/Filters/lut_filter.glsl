uniform sampler2D LUT_image;
uniform ivec2 block_shape;

vec4 getColor(sampler2D screen_image, vec2 tex_coord)
{
    ivec2 LUT_image_size = textureSize(LUT_image, 0);
    ivec2 block_size = LUT_image_size / block_shape;
    int n_blocks = block_size.x * block_size.y;

    vec4 color = clamp(textureLod(screen_image, tex_coord, 0), 0.0, 1.0);
    vec2 dxy = color.rg * block_shape / LUT_image_size;

    float i_blockf = color.b * (n_blocks - 1);
    int i_block = int(i_blockf);
    float rear = i_blockf - i_block;

    ivec2 block_index = ivec2(i_block % block_size.x, i_block / block_size.x);
    vec2 start_xy = float(block_index * block_shape) / LUT_image_size;
    vec2 new_tex_coord = start_xy + dxy;
    vec4 new_color = textureLod(LUT_image, vec2(new_tex_coord.x, 1-new_tex_coord.y), 0);

    if (i_block < n_blocks-1)
    {
        block_index = ivec2((i_block+1) % block_size.x, (i_block+1) / block_size.x);
        start_xy = float(block_index * block_shape) / LUT_image_size;
        new_tex_coord = start_xy + dxy;
        new_color = mix(new_color, textureLod(LUT_image, vec2(new_tex_coord.x, 1-new_tex_coord.y), 0), rear);
    }

    return new_color;
}