#version 460 core

#extension GL_ARB_bindless_texture : require

in VertexOut
{
    vec3 view_pos;
    mat3 view_TBN;
    vec3 tex_coord;
    vec4 color;
    vec4 back_color;
    flat int env_map_index;
    flat bool visible;
} fs_in;

in VertexInfo
{
    flat vec2 screen_coord[3];
    flat vec2 tex_coord[3];
} vertex_info;

out vec4 out_color;

#include "Material.glsl"
#include "PointLight.glsl"
#include "DirLight.glsl"
#include "SpotLight.glsl"
#include "fragment_utils.glsl"
#include "env_mapping.glsl"
#include "math.glsl"

buffer PointLights
{
    int n_point_lights;
    PointLight point_lights[];
};

buffer DirLights
{
    int n_dir_lights;
    DirLight dir_lights[];
};

buffer SpotLights
{
    int n_spot_lights;
    SpotLight spot_lights[];
};

buffer BindlessSamplerCubes
{
    int n_bindless_samplerCubes;
    samplerCube bindless_samplerCubes[];
};

uniform Material material;
uniform Material back_material;
uniform sampler2D SSAO_map;
uniform Camera camera;

// 环境映射
uniform bool use_skybox_map;
uniform bool use_skydome_map;
uniform samplerCube skybox_map;
uniform sampler2D skydome_map;

// per pixel linked list
uniform sampler2D transparent_mask;
uniform image2D nearest_opaque_depth_map;

layout(binding=0) uniform atomic_uint fragments_buffer_counter;
layout(r32ui) uniform uimage2D start_offset_map;
layout(r32ui) uniform uimage2D fragments_link_map;
layout(rgba32f) uniform image2D fragments_color_map;
layout(r32f) uniform image2D fragments_depth_map;

#define CURRENT_COLOR (gl_FrontFacing ? fs_in.color : fs_in.back_color)
#define CURRENT_MATERIAL (gl_FrontFacing ? material : back_material)

void main()
{
    // 可见性测试
    if (!fs_in.visible)
    {
        discard;
    }

    mat3 view_TBN = fs_in.view_TBN;
    vec3 view_normal = normalize(view_TBN[2]);
    if (!gl_FrontFacing)
    {
        view_normal = -view_normal;
    }
    view_TBN[2] = view_normal;
    if (hasnan(view_TBN))
    {
        return;
    }

    vec3 view_pos = fs_in.view_pos;
    vec2 frag_tex_coord = fs_in.tex_coord.st;

    // 高度贴图和法线贴图改变几何信息
    change_geometry(
        CURRENT_MATERIAL,
        view_pos, view_normal,
        frag_tex_coord, view_TBN
    );

    // 自定义深度测试
    float nearest_opaque_depth = texelFetch(nearest_opaque_depth_map, ivec2(gl_FragCoord.xy), 0).r;
    if (2*gl_FragCoord.z-1 >= nearest_opaque_depth)
    {
        discard;
    }

    // 实际使用的材质
    InternalMaterial internal_material = fetch_internal_material(
        CURRENT_COLOR, CURRENT_MATERIAL, frag_tex_coord
    );

    // 透明度过低丢弃
    if (internal_material.opacity < 1E-6 && length(internal_material.emission) < 1E-6)
    {
        discard;
    }

    // 环境光
    vec3 out_color3 = internal_material.ambient;

    vec3 view_dir = view_dir_to_world(camera, view_pos);
    vec3 normal = view_dir_to_world(camera, view_normal);

    // 点光源
    for(int i = 0; i < n_point_lights; i++)
    {
        out_color3 += Phong_lighting(point_lights[i], internal_material, view_dir, normal, true);
    }

    // 平行光
    for(int i = 0; i < n_dir_lights; i++)
    {
        out_color3 += Phong_lighting(dir_lights[i], internal_material, view_dir, normal, true);
    }

    // 聚光
    for(int i = 0; i < n_spot_lights; i++)
    {
        out_color3 += Phong_lighting(spot_lights[i], internal_material, view_dir, normal, true);
    }

    // SSAO
    float ssao_factor = texelFetch(SSAO_map, ivec2(gl_FragCoord.xy/2), 0).r;
    out_color3 = (1-ssao_factor)*out_color3;

    // 自发光
    out_color3 = internal_material.emission + out_color3;

    // 环境映射
    float texture_lod = get_texture_lod(skydome_map, vertex_info.tex_coord, vertex_info.screen_coord, screen_size);
    vec4 env_color = fetch_env_color(
        internal_material.reflection,
        internal_material.refraction,
        internal_material.refraction_index,
        view_dir, normal, texture_lod,
        use_skybox_map, skybox_map,
        use_skydome_map, skydome_map,
        (fs_in.env_map_index > 0), bindless_samplerCubes[fs_in.env_map_index]
    );
    out_color3 = mix(out_color3, env_color.rgb, env_color.a);

    // 最终颜色
    out_color = vec4(out_color3, internal_material.opacity);

    // 写入 per pixel linked list
    uint new_index = atomicCounterIncrement(fragments_buffer_counter) + 1;

    ivec2 fragmets_buffer_size = imageSize(fragments_color_map);
    ivec2 new_coord = ivec2((new_index-1) / fragmets_buffer_size.y, (new_index-1) % fragmets_buffer_size.y);

    uint current_index = imageLoad(start_offset_map, ivec2(gl_FragCoord.xy)).r;
    if (current_index == 0)
    {
        imageStore(fragments_color_map, new_coord, out_color);
        imageStore(fragments_depth_map, new_coord, vec4(view_pos.y));
        imageStore(fragments_link_map, new_coord, uvec4(0));
        imageStore(start_offset_map, ivec2(gl_FragCoord.xy), ivec4(new_index));
        return;
    }
    ivec2 current_coord = ivec2((current_index-1) / fragmets_buffer_size.y, (current_index-1) % fragmets_buffer_size.y);
    vec4 current_color = imageLoad(fragments_color_map, current_coord);
    float current_depth = imageLoad(fragments_depth_map, current_coord).r;
    
    if (view_pos.y >= current_depth)
    {
        imageStore(fragments_color_map, new_coord, out_color);
        imageStore(fragments_depth_map, new_coord, vec4(view_pos.y));
        imageStore(fragments_link_map, new_coord, uvec4(current_index));
        imageStore(start_offset_map, ivec2(gl_FragCoord.xy), ivec4(new_index));
        return;
    }

    uint next_index = imageLoad(fragments_link_map, current_coord).r;
    while(next_index != 0 && view_pos.y < current_depth)
    {
        current_index = next_index;
        current_coord = ivec2((current_index-1) / fragmets_buffer_size.y, (current_index-1) % fragmets_buffer_size.y);
        current_depth = imageLoad(fragments_depth_map, current_coord).r;
        next_index = imageLoad(fragments_link_map, current_coord).r;
    }
    imageStore(fragments_link_map, current_coord, uvec4(new_index));

    imageStore(fragments_color_map, new_coord, out_color);
    imageStore(fragments_depth_map, new_coord, vec4(view_pos.y));
    imageStore(fragments_link_map, new_coord, uvec4(next_index));
}