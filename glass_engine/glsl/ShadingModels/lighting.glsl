#ifndef _LIGHTING_GLSL__
#define _LIGHTING_GLSL__

#include "Flat.glsl"
#include "Gouraud.glsl"
#include "Phong.glsl"
#include "PhongBlinn.glsl"
#include "Toon.glsl"
#include "OrenNayar.glsl"
#include "Minnaert.glsl"
#include "CookTorrance.glsl"
#include "Fresnel.glsl"

vec3 lighting(vec3 to_light, vec3 to_camera, vec3 normal, InternalMaterial material)
{
    switch (material.shading_model)
    {
    case SHADING_MODEL_FLAT: return Flat_lighting(to_light, to_camera, normal, material);
    case SHADING_MODEL_GOURAUD: return Gouraud_lighting(to_light, to_camera, normal, material);
    case SHADING_MODEL_PHONG: return Phong_lighting(to_light, to_camera, normal, material);
    case SHADING_MODEL_PHONG_BLINN: return PhongBlinn_lighting(to_light, to_camera, normal, material);
    case SHADING_MODEL_TOON: return Toon_lighting(to_light, to_camera, normal, material);
    case SHADING_MODEL_OREN_NAYAR: return OrenNayar_lighting(to_light, to_camera, normal, material);
    case SHADING_MODEL_MINNAERT: return Minnaert_lighting(to_light, to_camera, normal, material);
    case SHADING_MODEL_COOK_TORRANCE:
    case SHADING_MODEL_PBR: return CookTorrance_lighting(to_light, to_camera, normal, material);
    case SHADING_MODEL_FRESNEL: return Fresnel_lighting(to_light, to_camera, normal, material);
    default: return vec3(0);
    }
}

#endif