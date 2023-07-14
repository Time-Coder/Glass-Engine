#ifndef _DRAW_NONE_FILLED_GLSL__
#define _DRAW_NONE_FILLED_GLSL__

vec4 draw_none_filled()
{
    vec4 out_color = vec4(0, 0, 0, 0);
    if (material.use_diffuse_map)
    {
        vec4 texture_color = texture(material.diffuse_map, fs_in.tex_coord.st);
        out_color = mix(fs_in.color, texture_color, texture_color.a);
    }
    else
    {
        out_color = fs_in.color;
    }

    if (out_color.a < 1E-6)
    {
        discard;
    }

    if (is_opaque_pass)
    {
        if(out_color.a < 1-1E-6)
        {
            discard;
        }
    }
    else
    {
        if(out_color.a >= 1-1E-6)
        {
            discard;
        }
    }

    return out_color;
}

#endif