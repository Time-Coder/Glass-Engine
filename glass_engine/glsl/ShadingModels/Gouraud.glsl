#include "Phong.glsl"

vec3 Gouraud_lighting(vec3 to_light, vec3 to_camera, vec3 normal, InternalMaterial material)
{
    return Phong_lighting(to_light, to_camera, normal, material);
}