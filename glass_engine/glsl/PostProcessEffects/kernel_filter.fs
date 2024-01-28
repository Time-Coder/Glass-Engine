#version 430 core

in vec2 tex_coord;
out vec4 frag_color;

uniform sampler2D screen_image;
uniform int channels;

buffer Kernel
{
    int rows;
    int cols;
    float data[];
};

void main()
{
    vec2 tex_offset = 1.0 / textureSize(screen_image, 0);
    float dx = tex_offset.x;
    float dy = tex_offset.y;

    frag_color = vec4(0);
    for (int i = 0; i < rows; i++)
    {
        float t = tex_coord.t + (i - 0.5*(rows-1))*dy;
        for (int j = 0; j < cols; j++)
        {
            float s = tex_coord.s + (j - 0.5*(cols-1))*dx;
            vec4 current_value = max(textureLod(screen_image, vec2(s, t), 0), 0.0);
            if (channels == 1)
            {
                current_value.gb = current_value.rr;
                current_value.a = 1;
            }
            frag_color += data[i*cols + j] * current_value;
        }
    }
}
