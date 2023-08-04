#version 460 core

#extension GL_EXT_texture_array : require

in TexCoord
{
    vec2 tex_coord;
} fs_in;

out vec4 frag_color;

uniform sampler2DArray screen_image;

buffer Kernel
{
    int rows;
    int cols;
    float data[];
};

void main()
{
    vec2 tex_offset = 1.0 / textureSize(screen_image, 0).xy;
    float dx = tex_offset.x;
    float dy = tex_offset.y;

    frag_color = vec4(0, 0, 0, 0);
    for (int i = 0; i < rows; i++)
    {
        float t = fs_in.tex_coord.t + (i - 0.5*(rows-1))*dy;
        for (int j = 0; j < cols; j++)
        {
            float s = fs_in.tex_coord.s + (j - 0.5*(cols-1))*dx;
            frag_color += data[i*cols + j] * texture2DArray(screen_image, vec3(s, t, gl_Layer));
        }
    }
}