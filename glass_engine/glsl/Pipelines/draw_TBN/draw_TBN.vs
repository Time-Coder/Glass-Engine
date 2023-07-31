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
layout (location = 7) in vec3 abs_position;
layout (location = 8) in vec4 abs_orientation;
layout (location = 9) in vec3 abs_scale;
layout (location = 10) in uvec2 env_map_handle;
layout (location = 11) in int visible;

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
    Transform transform;
    transform.abs_position = abs_position;
    transform.abs_orientation = vec4_to_quat(abs_orientation);
    transform.abs_scale = abs_scale;

    vec3 vertex_pos = transform_apply(transform, position);
    vec3 vertex_view_pos = world_to_view(camera, vertex_pos);
    gl_Position = view_to_NDC(camera, vertex_view_pos);
    
    mat3 TBN = mat3(tangent, bitangent, normal);
    vs_out.view_pos = vertex_view_pos;
    vs_out.view_TBN = world_TBN_to_view(camera, transform_apply_to_TBN(transform, TBN));
    vs_out.visible = (visible != 0);
}