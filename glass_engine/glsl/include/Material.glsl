#ifndef _MATERIAL_GLSL__
#define _MATERIAL_GLSL__

#define SHADING_MODEL_FLAT 1
#define SHADING_MODEL_GOURAUD 2
#define SHADING_MODEL_PHONG 3
#define SHADING_MODEL_PHONG_BLINN 4
#define SHADING_MODEL_TOON 5
#define SHADING_MODEL_OREN_NAYAR 6
#define SHADING_MODEL_MINNAERT 7
#define SHADING_MODEL_COOK_TORRANCE 8
#define SHADING_MODEL_UNLIT 9
#define SHADING_MODEL_FRESNEL 10
#define SHADING_MODEL_PBR 11

#include "sampling.glsl"

struct Material
{
	uint shading_model;
    bool recv_shadows;
	vec3 ambient;
	vec3 diffuse;
	vec3 specular;
	vec3 emission;
	vec4 reflection;
	float shininess;
    float shininess_strength;
	float opacity;
	float height_scale;
	float refractive_index;
	vec3 base_color;
	float metallic;
	float roughness;
    int diffuse_bands;
    int specular_bands;
    float diffuse_softness;
    float specular_softness;
    float rim_power;
    bool fog;
    bool env_mix_diffuse;

	sampler2D ambient_map;
	sampler2D diffuse_map;
	sampler2D specular_map;
	sampler2D emission_map;
	sampler2D shininess_map;
	sampler2D glossiness_map;
	sampler2D normal_map;
	sampler2D height_map;
	sampler2D opacity_map;
	sampler2D reflection_map;
	sampler2D base_color_map;
    sampler2D ao_map;
    sampler2D roughness_map;
	sampler2D metallic_map;
    sampler2D arm_map;
};

struct InternalMaterial
{
	uint shading_model;
    bool recv_shadows;
    vec3 preshading_color;
	vec3 ambient;
	vec3 diffuse;
	vec3 specular;
	vec3 emission;
	vec3 base_color;
	vec4 reflection;
	float refractive_index;
	float shininess;
	float opacity;
    float ao;
	float roughness;
	float metallic;
    uint diffuse_bands;
    uint specular_bands;
    float diffuse_softness;
    float specular_softness;
    float rim_power;
    float light_rim_power;
    float shadow_visibility;
    bool fog;
};

InternalMaterial fetch_internal_material(vec4 frag_color, Material material, vec2 tex_coord)
{
    InternalMaterial internal_material;
    internal_material.shading_model = material.shading_model;
    internal_material.recv_shadows = material.recv_shadows;
    internal_material.diffuse_bands = material.diffuse_bands;
    internal_material.specular_bands = material.specular_bands;
    internal_material.diffuse_softness = material.diffuse_softness;
    internal_material.specular_softness = material.specular_softness;
    internal_material.rim_power = material.rim_power;
    internal_material.fog = material.fog;

    // 材质不透明度
    float material_opacity = material.opacity;
    if (textureValid(material.opacity_map))
    {
        material_opacity = textureColor(material.opacity_map, tex_coord).r;
    }

    // 环境光颜色
    internal_material.ambient = material.ambient;
    if (textureValid(material.ambient_map))
    {
        internal_material.ambient = textureColor(material.ambient_map, tex_coord).rgb;
    }
    else if (textureValid(material.diffuse_map))
    {
        internal_material.ambient = 0.2 * textureColor(material.diffuse_map, tex_coord).rgb;
    }
    else if (textureValid(material.base_color_map))
    {
        internal_material.ambient = 0.2 * textureColor(material.base_color_map, tex_coord).rgb;
    }
    else if (length(internal_material.ambient) < 1E-6)
    {
        internal_material.ambient = 0.2 * material.diffuse;
    }
    internal_material.ambient = mix(0.2*frag_color.rgb, internal_material.ambient, material_opacity);

    // 漫反射颜色
    internal_material.diffuse = material.diffuse;
    internal_material.opacity = 1 - (1-frag_color.a)*(1-material_opacity);
    if (textureValid(material.diffuse_map))
    {
        vec4 material_diffuse4 = textureColor(material.diffuse_map, tex_coord);
        internal_material.diffuse = material_diffuse4.rgb;
        internal_material.opacity = 1 - (1-frag_color.a)*(1-material_diffuse4.a*material_opacity);
    }
    else if (textureValid(material.base_color_map))
    {
        vec4 material_diffuse4 = textureColor(material.base_color_map, tex_coord);
        internal_material.diffuse = material_diffuse4.rgb;
        internal_material.opacity = 1 - (1-frag_color.a)*(1-material_diffuse4.a*material_opacity);
    }
    internal_material.diffuse = mix(frag_color.rgb, internal_material.diffuse, material_opacity);

    // 镜面高光颜色
    internal_material.specular = material.specular;
    if (textureValid(material.specular_map))
    {
        internal_material.specular = textureColor(material.specular_map, tex_coord).rgb;
    }
    internal_material.specular *= material.shininess_strength;
    internal_material.specular = mix(vec3(0.3), internal_material.specular, material_opacity);

    // 闪耀度
    internal_material.shininess = material.shininess;
    if (textureValid(material.shininess_map))
    {
        internal_material.shininess = 256 * textureColor(material.shininess_map, tex_coord).r;
    }
    else if (textureValid(material.glossiness_map))
    {
        float glossiness = textureColor(material.glossiness_map, tex_coord).r;
        internal_material.shininess = 256 * glossiness * glossiness;
    }

    // 自发光颜色
    internal_material.emission = material.emission;
    if (material.shading_model == SHADING_MODEL_UNLIT)
    {
        internal_material.opacity = 1 - (1-frag_color.a)*(1-material_opacity);
    }
    if (textureValid(material.emission_map))
    {
        vec4 material_emission4 = textureColor(material.emission_map, tex_coord);
        internal_material.emission = material_emission4.rgb;
        if (material.shading_model == SHADING_MODEL_UNLIT)
        {
            internal_material.opacity = 1 - (1-frag_color.a)*(1-material_emission4.a*material_opacity);
        }
    }
    internal_material.emission = mix(vec3(0), internal_material.emission, material_opacity);
    if (material.shading_model == SHADING_MODEL_UNLIT && length(internal_material.emission) < 1E-6)
    {
        internal_material.emission = internal_material.diffuse;
    }

    // 反射
    internal_material.reflection = material.reflection;
    if (textureValid(material.reflection_map))
    {
        internal_material.reflection = textureColor(material.reflection_map, tex_coord);
    }
    if (material.env_mix_diffuse)
    {
        internal_material.reflection.rgb = internal_material.reflection.rgb * internal_material.diffuse;
    }
    internal_material.reflection.a *= material_opacity;

    // 折射率
    internal_material.refractive_index = material.refractive_index;
    
    // arm
    internal_material.ao = 1;
    internal_material.roughness = material.roughness;
    internal_material.metallic = material.metallic;
    if (textureValid(material.arm_map))
    {
        vec3 arm = textureColor(material.arm_map, tex_coord).rgb;
        internal_material.ao = arm[0];
        internal_material.roughness = arm[1];
        internal_material.metallic = arm[2];
    }

    // 环境光遮蔽
    if (textureValid(material.ao_map))
    {
        internal_material.ao = textureColor(material.ao_map, tex_coord).r;
    }
    internal_material.ao = mix(1, internal_material.ao, material_opacity);

    // 粗糙度
    if (textureValid(material.roughness_map))
    {
        internal_material.roughness = textureColor(material.roughness_map, tex_coord).r;
    }

    // 金属度
    if (textureValid(material.metallic_map))
    {
        internal_material.metallic = textureColor(material.metallic_map, tex_coord).r;
    }

    // 基础颜色
    internal_material.base_color = material.base_color;
    if (length(internal_material.base_color) < 1E-6)
    {
        internal_material.base_color = internal_material.diffuse;
    }
    if (textureValid(material.base_color_map))
    {
        internal_material.base_color = textureColor(material.base_color_map, tex_coord).rgb;
    }
    else if (textureValid(material.diffuse_map))
    {
        internal_material.base_color = textureColor(material.diffuse_map, tex_coord).rgb;
    }
    internal_material.base_color = mix(frag_color.rgb, internal_material.base_color, material_opacity);

    return internal_material;
}

#endif