#ifndef _CAMERA_GLSL_
#define _CAMERA_GLSL_

#include "math.glsl"

struct Camera
{
	// 内参数
	// 共有
	float near;
	float far;
	float clip;
	float focus;
	float aperture;
	bool auto_focus;
	vec2 focus_tex_coord;
	float focus_change_speed;
	int projection_mode; // 0: 透视投影, 1: 正射投影

	// 透视投影专有
	float tan_half_fov;
	float sin_half_fov;
	float aspect;

	// 正射投影专有
	float height;
	float width;

	// 外参数
	quat abs_orientation;
	vec3 abs_position;
};

vec3 world_to_view(Camera camera, vec3 world_coord)
{
	return quat_apply(quat_conj(camera.abs_orientation), world_coord - camera.abs_position);
}

vec3 view_to_world(Camera camera, vec3 view_coord)
{
	return quat_apply(camera.abs_orientation, view_coord) + camera.abs_position;
}

vec3 world_dir_to_view(Camera camera, vec3 world_dir)
{
	return quat_apply(quat_conj(camera.abs_orientation), world_dir);
}

vec3 view_dir_to_world(Camera camera, vec3 view_dir)
{
	return quat_apply(camera.abs_orientation, view_dir);
}

mat3 world_TBN_to_view(Camera camera, mat3 TBN)
{
	mat3 view_TBN;
	quat conj_orientation = quat_conj(camera.abs_orientation);
	view_TBN[0] = quat_apply(conj_orientation, TBN[0]);
	view_TBN[1] = quat_apply(conj_orientation, TBN[1]);
	view_TBN[2] = quat_apply(conj_orientation, TBN[2]);
	return view_TBN;
}

vec4 view_to_NDC(Camera camera, vec3 view_coord, int projection_mode)
{
	// 标准设备坐标
	vec4 NDC_coord;
	if(projection_mode == 0) // 透视投影
	{
		NDC_coord.x = view_coord.x / (camera.aspect * camera.tan_half_fov);
		NDC_coord.y = view_coord.z / camera.tan_half_fov;
		NDC_coord.z = 2*camera.far*(view_coord.y-camera.near)/camera.clip-view_coord.y;
		NDC_coord.w = view_coord.y;
	}
	else // 正射投影
	{
		NDC_coord.x = 2*view_coord.x / camera.width;
		NDC_coord.y = 2*view_coord.z / camera.height;
		NDC_coord.z = 2*(view_coord.y-camera.near)/camera.clip-1;
		NDC_coord.w = 1;
	}
	
	return NDC_coord;
}

vec4 view_to_NDC(Camera camera, vec3 view_coord)
{
	return view_to_NDC(camera, view_coord, camera.projection_mode);
}

vec4 Camera_project(Camera camera, vec3 world_coord)
{
	vec3 view_coord = world_to_view(camera, world_coord);
	return view_to_NDC(camera, view_coord);
}

vec4 Camera_project_skybox(Camera camera, vec3 world_coord)
{
	world_coord = quat_apply(quat(cos45, -sin45, 0, 0), world_coord);
	vec3 view_coord = world_dir_to_view(camera, world_coord);
	
	return view_to_NDC(camera, view_coord, 0);
}

vec4 Camera_project_skydome(Camera camera, vec3 world_coord)
{
	vec3 view_coord = world_dir_to_view(camera, world_coord);
	return view_to_NDC(camera, view_coord, 0);
}

#endif