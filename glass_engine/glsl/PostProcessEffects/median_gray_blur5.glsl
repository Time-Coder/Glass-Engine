#define KERNEL_WIDTH 5

vec4 post_process(sampler2D screen_image, vec2 tex_coord)
{
    float values[KERNEL_WIDTH*KERNEL_WIDTH];
    vec2 tex_offset = 1.0 / textureSize(screen_image, 0);
    float dx = tex_offset.x;
    float dy = tex_offset.y;

    int current_index = 0;
    float half_width = (KERNEL_WIDTH - 1.0)/2.0;
    for (float i = -half_width; i <= half_width; i += 1)
    {
        float y = tex_coord.y + dy*i;
        for (float j = -half_width; j <= half_width; j += 1)
        {
            float x = tex_coord.x + dx*j;
            values[current_index] = textureLod(screen_image, vec2(x, y), 0).r;
            current_index++;
        }
    }

    int N = KERNEL_WIDTH * KERNEL_WIDTH;
    for (int j = N-1; j >= 0; j--)
    {
        for (int i = 0; i < j; i++)
        {
            if (values[i] > values[i+1])
            {
                float temp = values[i];
                values[i] = values[i+1];
                values[i+1] = temp;
            }
        }
    }

    int half_index = (KERNEL_WIDTH - 1) / 2;
    if (KERNEL_WIDTH % 2 == 0)
    {
        return vec4(vec3(0.5*(values[half_index] + values[half_index+1])), 1);
    }
    else
    {
        return vec4(vec3(values[half_index]), 1);
    }
}