#include "Material.glsl"
#include "sampling.glsl"

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
    internal_material.dynamic_env_mapping = material.dynamic_env_mapping;

    // base_color
    internal_material.opacity = material.opacity;
    if (textureValid(material.opacity_map))
    {
        internal_material.opacity = max(texture(material.opacity_map, tex_coord).r, 0.0);
    }

    internal_material.base_color = material.base_color;
    if (textureValid(material.base_color_map))
    {
        internal_material.base_color = max(texture(material.base_color_map, tex_coord), 0.0).rgb;
    }
    internal_material.base_color = frag_color.rgb * internal_material.base_color;
    
    // ambient
    internal_material.ambient = material.ambient;
    if (textureValid(material.ambient_map))
    {
        internal_material.ambient = max(texture(material.ambient_map, tex_coord).rgb, 0.0);
    }
    else if (textureValid(material.base_color_map))
    {
        internal_material.ambient = 0.2 * max(texture(material.base_color_map, tex_coord).rgb, 0.0);
    }
    else if (length(internal_material.ambient) < 1E-6)
    {
        internal_material.ambient = 0.2 * material.base_color;
    }
    
    // specular
    internal_material.specular = material.specular;
    if (textureValid(material.specular_map))
    {
        internal_material.specular = max(texture(material.specular_map, tex_coord).rgb, 0.0);
    }
    internal_material.specular *= material.shininess_strength;
    
    // shininess
    internal_material.shininess = material.shininess;
    if (textureValid(material.shininess_map))
    {
        internal_material.shininess = 256 * max(texture(material.shininess_map, tex_coord).r, 0.0);
    }

    // emission
    internal_material.emission = material.emission;
    bool emission_map_valid = textureValid(material.emission_map);
    if (emission_map_valid)
    {
        internal_material.emission = max(texture(material.emission_map, tex_coord), 0.0).rgb;
    }
    if (!emission_map_valid &&
        (material.shading_model == SHADING_MODEL_UNLIT) &&
        (length(internal_material.emission) < 1E-6))
    {
        internal_material.emission = internal_material.base_color;
    }
    internal_material.emission *= material.emission_strength;

    // reflection
    internal_material.reflection = material.reflection;
    if (textureValid(material.reflection_map))
    {
        internal_material.reflection = max(texture(material.reflection_map, tex_coord), 0.0);
    }
    if (material.env_mix_diffuse)
    {
        internal_material.reflection.rgb = internal_material.reflection.rgb * internal_material.base_color;
    }
    internal_material.refractive_index = material.refractive_index;

    // arm
    internal_material.ao = 1;
    internal_material.roughness = material.roughness;
    internal_material.metallic = material.metallic;

    if (textureValid(material.arm_map))
    {
        vec3 arm = max(texture(material.arm_map, tex_coord).rgb, 0.0);
        if (material.arm_use_a)
        {
            internal_material.ao = arm[0];
        }
        internal_material.roughness = arm[1];
        internal_material.metallic = arm[2];
    }

    if (textureValid(material.ao_map))
    {
        internal_material.ao = max(texture(material.ao_map, tex_coord).r, 0.0);
    }

    if (textureValid(material.roughness_map))
    {
        internal_material.roughness = max(texture(material.roughness_map, tex_coord).r, 0.0);
    }

    if (textureValid(material.metallic_map))
    {
        internal_material.metallic = max(texture(material.metallic_map, tex_coord).r, 0.0);
    }

    return internal_material;
}