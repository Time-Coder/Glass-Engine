float rim(vec3 to_light, vec3 to_camera, vec3 normal, float light_rim_power, float material_rim_power)
{
    if (light_rim_power < 1E-6 || material_rim_power < 1E-6)
        return 0;
    float light_rim = pow(clamp(0.5 - 0.5*dot(to_light, to_camera), 0, 1), 1/(0.001+light_rim_power));
    float material_rim = pow(clamp(1 - dot(normal, to_camera), 0, 1), 1/(0.001+material_rim_power));
    return light_rim * material_rim;
}