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