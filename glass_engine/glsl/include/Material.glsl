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
	float emission_strength;
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
	bool dynamic_env_mapping;
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
	bool dynamic_env_mapping;
};