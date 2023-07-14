#version 460 core

out vec4 out_color;

// per pixel linked list
uniform sampler2D transparent_mask;
layout(r32ui) volatile uniform uimage2D start_offset_map;
layout(r32f) volatile uniform image2D nearest_opaque_depth_map;
layout(r32ui) volatile uniform uimage2D fragments_link_map;
layout(rgba32f) volatile uniform image2D fragments_color_map;

void main()
{
    if (texelFetch(transparent_mask, ivec2(gl_FragCoord.xy), 0).r < 0.5)
    {
        discard;
    }

    ivec2 fragmets_buffer_size = imageSize(fragments_link_map);
    uint current_index = imageLoad(start_offset_map, ivec2(gl_FragCoord.xy)).r;
    vec3 C = vec3(0, 0, 0);
    while (current_index > 0)
    {
        ivec2 current_coord = ivec2((current_index-1) / fragmets_buffer_size.y, (current_index-1) % fragmets_buffer_size.y);
        vec4 c = imageLoad(fragments_color_map, ivec2(gl_FragCoord.xy));
        C = c.rgb * c.a + (1-c.a) * C;
        current_index = imageLoad(fragments_link_map, current_coord).r;
    }
    
    out_color = vec4(C, 1);
}