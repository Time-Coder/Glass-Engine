#define imageRead(value_center, image, tex_coord) \
vec4 value_center;\
{\
    ivec2 image_size = imageSize(image);\
    float x_max = float(image_size.x - 1);\
    float y_max = float(image_size.y - 1);\
\
    vec2 texel_coord = tex_coord * (vec2(image_size) - 1.0);\
    float x = floor(texel_coord.x);\
    float y = floor(texel_coord.y);\
    float x_rear = texel_coord.x - x;\
    float y_rear = texel_coord.y - y;\
    vec4 value1 = imageLoad(image, ivec2(x, y));\
    vec4 value2 = imageLoad(image, ivec2(min(x+1, x_max), y));\
    vec4 value3 = imageLoad(image, ivec2(x, min(y+1, y_max)));\
    vec4 value4 = imageLoad(image, ivec2(min(x+1, x_max), min(y+1, y_max)));\
    vec4 value12 = mix(value1, value2, x_rear);\
    vec4 value34 = mix(value3, value4, x_rear);\
    value_center = mix(value12, value34, y_rear);\
}

#define imageWrite(image, tex_coord, value) \
{\
    ivec2 image_size = imageSize(image);\
    float x_max = float(image_size.x - 1);\
    float y_max = float(image_size.y - 1);\
\
    vec2 texel_coord = tex_coord * (vec2(image_size) - 1.0);\
    float x = floor(texel_coord.x);\
    float y = floor(texel_coord.y);\
    float x_rear = texel_coord.x - x;\
    float y_rear = texel_coord.y - y;\
\
    vec4 value1 = (1-x_rear)*(1-y_rear)*value;\
    vec4 value2 = x_rear*(1-y_rear)*value;\
    vec4 value3 = (1-x_rear)*y_rear*value;\
    vec4 value4 = x_rear*y_rear*value;\
\
    ivec2 texel_coord1 = ivec2(x, y);\
    ivec2 texel_coord2 = ivec2(min(x+1, x_max), y);\
    ivec2 texel_coord3 = ivec2(x, min(y+1, y_max));\
    ivec2 texel_coord4 = ivec2(min(x+1, x_max), min(y+1, y_max));\
\
    vec4 old_value1 = imageLoad(image, texel_coord1);\
    vec4 old_value2 = imageLoad(image, texel_coord2);\
    vec4 old_value3 = imageLoad(image, texel_coord3);\
    vec4 old_value4 = imageLoad(image, texel_coord4);\
\
    imageStore(image, texel_coord1, old_value1+value1);\
    memoryBarrierImage();\
\
    imageStore(image, texel_coord2, old_value2+value2);\
    memoryBarrierImage();\
\
    imageStore(image, texel_coord3, old_value3+value3);\
    memoryBarrierImage();\
\
    imageStore(image, texel_coord4, old_value4+value4);\
    memoryBarrierImage();\
}