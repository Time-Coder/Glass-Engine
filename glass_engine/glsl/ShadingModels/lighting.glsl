#include "Lambert.glsl"

#if USE_SHADING_MODEL_FLAT
#include "Flat.glsl"
#endif

#if USE_SHADING_MODEL_GOURAUD
#include "Gouraud.glsl"
#endif

#if USE_SHADING_MODEL_PHONG
#include "Phong.glsl"
#endif

#if USE_SHADING_MODEL_PHONG_BLINN
#include "PhongBlinn.glsl"
#endif

#if USE_SHADING_MODEL_TOON
#include "Toon.glsl"
#endif

#if USE_SHADING_MODEL_OREN_NAYAR
#include "OrenNayar.glsl"
#endif

#if USE_SHADING_MODEL_MINNAERT
#include "Minnaert.glsl"
#endif

#if USE_SHADING_MODEL_COOK_TORRANCE
#include "CookTorrance.glsl"
#endif

#if USE_SHADING_MODEL_FRESNEL
#include "Fresnel.glsl"
#endif

vec3 lighting(vec3 to_light, vec3 to_camera, vec3 normal, InternalMaterial material)
{
    switch (material.shading_model)
    {
#if USE_SHADING_MODEL_FLAT
    case SHADING_MODEL_FLAT: return Flat_lighting(to_light, to_camera, normal, material);
#endif
#if USE_SHADING_MODEL_GOURAUD
    case SHADING_MODEL_GOURAUD: return Gouraud_lighting(to_light, to_camera, normal, material);
#endif
#if USE_SHADING_MODEL_PHONG
    case SHADING_MODEL_PHONG: return Phong_lighting(to_light, to_camera, normal, material);
#endif
#if USE_SHADING_MODEL_PHONG_BLINN
    case SHADING_MODEL_PHONG_BLINN: return PhongBlinn_lighting(to_light, to_camera, normal, material);
#endif
#if USE_SHADING_MODEL_TOON
    case SHADING_MODEL_TOON: return Toon_lighting(to_light, to_camera, normal, material);
#endif
#if USE_SHADING_MODEL_OREN_NAYAR
    case SHADING_MODEL_OREN_NAYAR: return OrenNayar_lighting(to_light, to_camera, normal, material);
#endif
#if USE_SHADING_MODEL_MINNAERT
    case SHADING_MODEL_MINNAERT: return Minnaert_lighting(to_light, to_camera, normal, material);
#endif
#if USE_SHADING_MODEL_COOK_TORRANCE
    case SHADING_MODEL_COOK_TORRANCE:
    case SHADING_MODEL_PBR: return CookTorrance_lighting(to_light, to_camera, normal, material);
#endif
#if USE_SHADING_MODEL_FRESNEL
    case SHADING_MODEL_FRESNEL: return Fresnel_lighting(to_light, to_camera, normal, material);
#endif
    default: return vec3(0);
    }
}