buffer Kernel
{
    int rows;
    int cols;
    float data[];
};

vec4 getColor(sampler2D screen_image, vec2 tex_coord)
{
    vec2 tex_offset = 1.0 / textureSize(screen_image, 0);
    float dx = tex_offset.x;
    float dy = tex_offset.y;

    vec4 frag_color = vec4(0, 0, 0, 0);
    for (int i = 0; i < rows; i++)
    {
        float t = tex_coord.t + (i - 0.5*(rows-1))*dy;
        for (int j = 0; j < cols; j++)
        {
            float s = tex_coord.s + (j - 0.5*(cols-1))*dx;
            frag_color += data[i*cols + j] * texture(screen_image, vec2(s, t));
        }
    }

    return frag_color;
}
