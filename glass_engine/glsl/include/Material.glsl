#ifndef _MATERIAL_GLSL__
#define _MATERIAL_GLSL__

struct Material
{
	uint shading_model;
	// Flat = 0x1
    // Gouraud = 0x2
    // Phong = 0x3
    // PhongBlinn = 0x4
    // Toon = 0x5
    // OrenNayar = 0x6
    // Minnaert = 0x7
    // CookTorrance = 0x8
    // NoShading = 0x9
    // Unlit = 0x9
    // Fresnel = 0xa
    // PBR = 0xb

    bool recv_shadows;
	vec3 ambient;
	vec3 diffuse;
	vec3 specular;
	vec3 emission;
	vec4 reflection;
	vec4 refraction;
	float shininess;
	float opacity;
	float height_scale;
	float refractive_index;
	vec3 albedo;
	float metallic;
	float roughness;

	bool use_ambient_map;
	bool use_diffuse_map;
	bool use_specular_map;
	bool use_emission_map;
	bool use_shininess_map;
	bool use_normal_map;
	bool use_height_map;
	bool use_opacity_map;
	bool use_ambient_occlusion_map;
	bool use_reflection_map;
	bool use_refraction_map;
	bool use_refractive_index_map;
	bool use_albedo_map;
	bool use_metallic_map;
	bool use_roughness_map;
    bool env_mix_diffuse;

	sampler2D ambient_map;
	sampler2D diffuse_map;
	sampler2D specular_map;
	sampler2D emission_map;
	sampler2D shininess_map;
	sampler2D normal_map;
	sampler2D height_map;
	sampler2D opacity_map;
	sampler2D ambient_occlusion_map;
	sampler2D reflection_map;
	sampler2D refraction_map;
	sampler2D refractive_index_map;
	sampler2D albedo_map;
	sampler2D metallic_map;
	sampler2D roughness_map;
};

struct InternalMaterial
{
	uint shading_model;
    bool recv_shadows;
	vec3 ambient;
	vec3 diffuse;
	vec3 specular;
	vec3 emission;
	vec3 albedo;
	vec4 reflection;
	vec4 refraction;
	float refractive_index;
	float shininess;
	float opacity;
	float roughness;
	float metallic;
    float ambient_occlusion;
};

InternalMaterial fetch_internal_material(vec4 frag_color, Material material, vec2 tex_coord)
{
    InternalMaterial internal_material; // 实际使用的材质
    internal_material.shading_model = material.shading_model;
    internal_material.recv_shadows = material.recv_shadows;

    // 材质不透明度
    float material_opacity = material.opacity;
    if (material.use_opacity_map)
    {
        material_opacity = texture(material.opacity_map, tex_coord).r;
    }

    // 环境光颜色
    bool ambient_is_black = true;
    internal_material.ambient = material.ambient;
    if (length(internal_material.ambient) < 1E-3)
    {
        ambient_is_black = true;
    }
    if (material.use_ambient_map)
    {
        internal_material.ambient = texture(material.ambient_map, tex_coord).rgb;
        ambient_is_black = false;
    }
    if (material.use_diffuse_map && !material.use_ambient_map)
    {
        ambient_is_black = true;
    }

    // 本体颜色 base_color
    vec3 base_color = frag_color.rgb;

    // 漫反射颜色
    if (material.use_diffuse_map)
    {
        vec4 diffuse_color = texture(material.diffuse_map, tex_coord);
        internal_material.diffuse = diffuse_color.rgb;
        internal_material.opacity = 1 - (1-frag_color.a)*(1-diffuse_color.a*material_opacity);
    }
    else if (material.use_albedo_map)
    {
        vec4 diffuse_color = texture(material.albedo_map, tex_coord);
        internal_material.diffuse = diffuse_color.rgb;
        internal_material.opacity = 1 - (1-frag_color.a)*(1-diffuse_color.a*material_opacity);
    }
    else
    {
        internal_material.diffuse = material.diffuse;
        internal_material.opacity = 1 - (1-frag_color.a)*(1-material_opacity);
    }
    internal_material.diffuse = mix(base_color, internal_material.diffuse, material_opacity);
    
    if (ambient_is_black)
    {
        internal_material.ambient = 0.1 * internal_material.diffuse.rgb;
    }

    // 镜面高光颜色
    internal_material.specular = material.specular;
    if (material.use_specular_map)
    {
        internal_material.specular = texture(material.specular_map, tex_coord).rgb;
    }

    // 闪耀度
    internal_material.shininess = material.shininess;
    if (material.use_shininess_map)
    {
        internal_material.shininess = texture(material.shininess_map, tex_coord).r;
    }

    // 自发光颜色
    internal_material.emission = material.emission;
    if (material.use_emission_map)
    {
        internal_material.emission = texture(material.emission_map, tex_coord).rgb;
    }

    // 反射
    internal_material.reflection = material.reflection;
    if (material.use_reflection_map)
    {
        internal_material.reflection = texture(material.reflection_map, tex_coord);
    }
    if (material.env_mix_diffuse)
    {
        internal_material.reflection.rgb *= internal_material.diffuse;
    }

    // 折射
    internal_material.refraction = material.refraction;
    if (material.use_refraction_map)
    {
        internal_material.refraction = texture(material.refraction_map, tex_coord);
    }
    if (material.env_mix_diffuse)
    {
        internal_material.refraction.rgb *= internal_material.diffuse;
    }

    // 折射率
    internal_material.refractive_index = material.refractive_index;
    if (material.use_refractive_index_map)
    {
        internal_material.refractive_index = texture(material.refractive_index_map, tex_coord).r;
    }

    if (internal_material.shading_model == 11 || internal_material.shading_model == 8)
    {
        // 金属度
        internal_material.metallic = material.metallic;
        if (material.use_metallic_map)
        {
            internal_material.metallic = texture(material.metallic_map, tex_coord).r;
        }

        // 粗糙度
        internal_material.roughness = material.roughness;
        if (material.use_roughness_map)
        {
            internal_material.roughness = texture(material.roughness_map, tex_coord).r;
        }

        // 基础颜色
        internal_material.albedo = material.albedo;
        if (length(internal_material.albedo) == 0)
        {
            internal_material.albedo = internal_material.diffuse;
        }

        if (material.use_albedo_map)
        {
            internal_material.albedo = texture(material.albedo_map, tex_coord).rgb;
        }
        else if (material.use_diffuse_map)
        {
            internal_material.albedo = texture(material.diffuse_map, tex_coord).rgb;
        }

        internal_material.albedo = pow(internal_material.albedo, vec3(2.2));
    }

    // 环境光遮蔽
    internal_material.ambient_occlusion = 1;
    if (material.use_ambient_occlusion_map)
    {
        internal_material.ambient_occlusion = texture(material.ambient_occlusion_map, tex_coord).r;
    }

    return internal_material;
}

#endif