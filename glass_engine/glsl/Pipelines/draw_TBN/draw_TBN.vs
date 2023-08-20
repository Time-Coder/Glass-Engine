#version 460 core


// vertex
layout (location = 0) in vec3 position;
layout (location = 1) in vec3 tangent;
layout (location = 2) in vec3 bitangent;
layout (location = 3) in vec3 normal;
layout (location = 4) in vec3 tex_coord;
layout (location = 5) in vec4 color;
layout (location = 6) in vec4 back_color;

// instance
layout (location = 7) in vec4 col0;
layout (location = 8) in vec4 col1;
layout (location = 9) in vec4 col2;
layout (location = 10) in vec4 col3;
layout (location = 11) in uvec2 env_map_handle;
layout (location = 12) in int visible;

out VertexOut
{
    vec3 view_pos;
    mat3 view_TBN;
    flat bool visible;
} vs_out;

#include "../../include/Transform.glsl"
#include "../../include/Camera.glsl"

uniform Camera camera;

void main()
{
    mat4 transform = mat4(col0, col1, col2, col3);

    vec3 vertex_pos = transform_apply(transform, position);
    vec3 vertex_view_pos = world_to_view(camera, vertex_pos);
    gl_Position = view_to_NDC(camera, vertex_view_pos);
    
    mat3 TBN = mat3(tangent, bitangent, normal);
    vs_out.view_pos = vertex_view_pos;
    vs_out.view_TBN = world_TBN_to_view(camera, transform_apply_to_TBN(transform, TBN));
    vs_out.visible = (visible != 0);
}