#include "../include/math.glsl"

vec3 _Uncharted(vec3 x)
{
  const float A = 0.15;
  const float B = 0.50;
  const float C = 0.10;
  const float D = 0.20;
  const float E = 0.02;
  const float F = 0.30;
  const float W = 11.2;
  return ((x*(A*x+C*B)+D*E)/(x*(A*x+B)+D*F))-E/F;
}

vec4 getColor(sampler2D screen_image, vec2 tex_coord)
{
    vec4 color = texture(screen_image, tex_coord);

    float ExposureBias = 2.5;
    color.rgb = sin(PI/2*_Uncharted(ExposureBias*color.rgb) / _Uncharted(vec3(11.2)));

    return color;
}