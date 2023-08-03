#version 460 core

#extension GL_ARB_bindless_texture : enable

layout (triangles, invocations=6) in;
layout (triangle_strip, max_vertices=3) out;

in flat int vertex_visible[];
out flat int visible;
out vec3 world_pos;

#include "../../include/Camera.glsl"
#include "../../Lights/SpotLight.glsl"

uniform SpotLight spot_light;
uniform float explode_distance;

void main()
{
    vec3 v1 = gl_in[1].gl_Position.xyz - gl_in[0].gl_Position.xyz;
    vec3 v2 = gl_in[2].gl_Position.xyz - gl_in[0].gl_Position.xyz;
    vec3 face_world_normal = normalize(cross(v1, v2));

    gl_Layer = gl_InvocationID;
    Camera camera = cube_camera(gl_InvocationID, spot_light.abs_position, 0.1, spot_light.coverage);
    for (int i = 0; i < 3; i++)
    {
        world_pos = gl_in[i].gl_Position.xyz + explode_distance * face_world_normal;
        visible = vertex_visible[i];

        gl_Position = Camera_project(camera, world_pos);
        EmitVertex();
    }
    
    EndPrimitive();
}