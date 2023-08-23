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
	float shininess;
    float shininess_strength;
	float opacity;
	float height_scale;
	float refractive_index;
	vec3 base_color;
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
	bool use_refractive_index_map;
	bool use_base_color_map;
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
	sampler2D refractive_index_map;
	sampler2D base_color_map;
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
	vec3 base_color;
	vec4 reflection;
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
    vec3 material_ambient = material.ambient;
    if (material.use_ambient_map)
    {
        material_ambient = texture(material.ambient_map, tex_coord).rgb;
    }
    else if (material.use_diffuse_map)
    {
        material_ambient = 0.1 * texture(material.diffuse_map, tex_coord).rgb;
    }
    else if (material.use_base_color_map)
    {
        material_ambient = 0.1 * texture(material.base_color_map, tex_coord).rgb;
    }
    else if (length(material_ambient) < 1E-6)
    {
        material_ambient = 0.1 * material.diffuse;
    }
    internal_material.ambient = mix(0.1*frag_color.rgb, material_ambient, material_opacity);

    // 漫反射颜色
    vec3 material_diffuse = material.diffuse;
    internal_material.opacity = 1 - (1-frag_color.a)*(1-material_opacity);
    if (material.use_diffuse_map)
    {
        vec4 material_diffuse4 = texture(material.diffuse_map, tex_coord);
        material_diffuse = material_diffuse4.rgb;
        internal_material.opacity = 1 - (1-frag_color.a)*(1-material_diffuse4.a*material_opacity);
    }
    else if (material.use_base_color_map)
    {
        vec4 material_diffuse4 = texture(material.base_color_map, tex_coord);
        material_diffuse = material_diffuse4.rgb;
        internal_material.opacity = 1 - (1-frag_color.a)*(1-material_diffuse4.a*material_opacity);
    }
    internal_material.diffuse = mix(frag_color.rgb, material_diffuse, material_opacity);

    // 镜面高光颜色
    vec3 material_specular = material.specular;
    if (material.use_specular_map)
    {
        material_specular = texture(material.specular_map, tex_coord).rgb;
    }
    material_specular *= material.shininess_strength;
    internal_material.specular = mix(vec3(1,1,1), material_specular, material_opacity);

    // 闪耀度
    internal_material.shininess = material.shininess;
    if (material.use_shininess_map)
    {
        internal_material.shininess = texture(material.shininess_map, tex_coord).r;
    }

    // 自发光颜色
    vec3 material_emission = material.emission;
    if (material.shading_model == 9)
    {
        internal_material.opacity = 1 - (1-frag_color.a)*(1-material_opacity);
    }
    if (material.use_emission_map)
    {
        vec4 material_emission4 = texture(material.emission_map, tex_coord);
        material_emission = material_emission4.rgb;
        if (material.shading_model == 9)
        {
            internal_material.opacity = 1 - (1-frag_color.a)*(1-material_emission4.a*material_opacity);
        }
    }
    if (material.shading_model != 9)
    {
        internal_material.emission = mix(vec3(0,0,0), material_emission, material_opacity);
    }

    // 反射
    internal_material.reflection = material.reflection;
    if (material.use_reflection_map)
    {
        internal_material.reflection = texture(material.reflection_map, tex_coord);
    }
    if (material.env_mix_diffuse)
    {
        internal_material.reflection.rgb = sqrt(internal_material.reflection.rgb * internal_material.diffuse);
    }
    internal_material.reflection.a *= material_opacity;

    // 折射率
    internal_material.refractive_index = material.refractive_index;
    if (material.use_refractive_index_map)
    {
        internal_material.refractive_index = texture(material.refractive_index_map, tex_coord).r;
    }
    
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
    vec3 material_base_color = material.base_color;
    if (length(material_base_color) < 1E-6)
    {
        material_base_color = internal_material.diffuse;
    }
    if (material.use_base_color_map)
    {
        material_base_color = texture(material.base_color_map, tex_coord).rgb;
    }
    else if (material.use_diffuse_map)
    {
        material_base_color = texture(material.diffuse_map, tex_coord).rgb;
    }
    internal_material.base_color = mix(frag_color.rgb, material_base_color, material_opacity);
    internal_material.base_color = pow(internal_material.base_color, vec3(2.2));

    // 环境光遮蔽
    float material_ao = 1;
    if (material.use_ambient_occlusion_map)
    {
        material_ao = texture(material.ambient_occlusion_map, tex_coord).r;
    }
    internal_material.ambient_occlusion = mix(1, material_ao, material_opacity);

    return internal_material;
}

#endif