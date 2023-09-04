#ifndef _FRESNEL_REFRACT_GLSL__
#define _FRESNEL_REFRACT_GLSL__

vec3 wavelength_to_color(float wavelength)
{
    vec4 color = vec4(0);
    if (380.0 <= wavelength && wavelength < 440.0)
    {
        color.r = (440.0 - wavelength) / (440.0 - 380.0);
        color.b = 1.0;
    }
    else if (440.0 <= wavelength && wavelength < 490.0)
    {
        color.g = (wavelength - 440.0) / (490.0 - 440.0);
        color.b = 1.0;
    }
    else if (wavelength >= 490.0 && wavelength < 510.0)
    {
        color.g = 1.0;
        color.b = (510.0 - wavelength) / (510.0 - 490.0);
    }
    else if (wavelength >= 510.0 && wavelength < 580.0)
    {
        color.r = (wavelength - 510.0) / (580.0 - 510.0);
        color.g = 1.0;
    }
    else if (wavelength >= 580.0 && wavelength < 645.0)
    {
        color.r = 1.0;
        color.g = (645.0 - wavelength) / (645.0 - 580.0);
    }
    else if (wavelength >= 645.0 && wavelength <= 780.0)
    {
        color.r = 1.0;
    }
 
    if (380.0 <= wavelength && wavelength < 420.0)
    {
        color.a = 0.30 + 0.70 * (wavelength - 380.0) / (420.0 - 380.0);
    }
    else if (420.0 <= wavelength && wavelength < 701.0)
    {
        color.a = 1.0;
    }
    else if (701.0 <= wavelength && wavelength < 780.0)
    {
        color.a = 0.30 + 0.70 * (780.0 - wavelength) / (780.0 - 700.0);
    }

    return color.rgb * color.a;
}

float fresnel_reflect_ratio(float n1, float n2, float cos_theta_i)
{
    float sin_theta_i2 = 1 - cos_theta_i*cos_theta_i;
    float sin_theta_o2 = (n1*n1/(n2*n2))*sin_theta_i2;
    if (sin_theta_o2 >= 1)
    {
        return 1;
    }
    
    float cos_theta_o = sqrt(1 - sin_theta_o2);

    float n1_cos_theta_i = n1 * cos_theta_i;
    float n2_cos_theta_o = n2 * cos_theta_o;
    float n1_cos_theta_o = n1 * cos_theta_o;
    float n2_cos_theta_i = n2 * cos_theta_i;

    float Rs = (n1_cos_theta_i - n2_cos_theta_o) / (n1_cos_theta_i + n2_cos_theta_o);
    float Rp = (n1_cos_theta_o - n2_cos_theta_i) / (n1_cos_theta_o + n2_cos_theta_i);
    return clamp(0.5*(Rs*Rs + Rp*Rp), 0, 1);
}

#endif