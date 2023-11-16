#include "math.glsl"
#include "soft.glsl"
#include "quat.glsl"

#define CAMERA_PROJECTION_PERSPECTIVE 0
#define CAMERA_PROJECTION_ORTHOGRAPHIC 1

struct CameraLens
{
	float focus;
	float aperture;
	bool auto_focus;
	vec2 focus_tex_coord;
	float focus_change_time;
	float explosure;
	bool auto_explosure;
	bool local_explosure;
	float explosure_adapt_time;
};

struct Camera
{
	float near;
	float far;
	uint projection_mode;
	float tan_half_fov;
	float sin_half_fov;
	float aspect;
	float height;
	float width;
	quat abs_orientation;
	vec3 abs_position;
	uint CSM_levels;
	CameraLens lens;
};

struct BoundingSphere
{
	vec3 center;
	float radius;
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

vec4 view_to_NDC(Camera camera, vec3 view_coord, uint projection_mode)
{
	vec4 NDC_coord;
	float clip = camera.far - camera.near;
	if (projection_mode == CAMERA_PROJECTION_PERSPECTIVE)
	{
		NDC_coord.x = view_coord.x / (camera.aspect * camera.tan_half_fov);
		NDC_coord.y = view_coord.z / camera.tan_half_fov;
		NDC_coord.z = 2*camera.far*(view_coord.y-camera.near)/clip-view_coord.y;
		NDC_coord.w = view_coord.y;
	}
	else
	{
		NDC_coord.x = 2*view_coord.x / camera.width;
		NDC_coord.y = 2*view_coord.z / camera.height;
		NDC_coord.z = 2*(view_coord.y-camera.near)/clip-1;
		NDC_coord.w = 1;
	}
	
	return NDC_coord;
}

vec3 screen_to_view(Camera camera, vec3 screen_coord)
{
	vec3 view_coord;
	float clip = camera.far - camera.near;
	if (camera.projection_mode == CAMERA_PROJECTION_PERSPECTIVE)
	{
		view_coord.y = camera.near * camera.far / (camera.far - clip * screen_coord.z);
		view_coord.x = (2*screen_coord.x - 1) * view_coord.y * camera.aspect * camera.tan_half_fov;
		view_coord.z = (2*screen_coord.y - 1) * view_coord.y * camera.tan_half_fov;
	}
	else
	{
		view_coord.y = screen_coord.z*clip + camera.near;
		view_coord.x = (screen_coord.x - 0.5) * camera.width;
		view_coord.z = (screen_coord.y - 0.5) * camera.height;
	}
	return view_coord;
}

vec3 screen_to_world(Camera camera, vec3 screen_coord)
{
	return view_to_world(camera, screen_to_view(camera, screen_coord));
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
	
	return view_to_NDC(camera, view_coord, CAMERA_PROJECTION_PERSPECTIVE);
}

vec4 Camera_project_skydome(Camera camera, vec3 world_coord)
{
	vec3 view_coord = world_dir_to_view(camera, world_coord);
	return view_to_NDC(camera, view_coord, CAMERA_PROJECTION_PERSPECTIVE);
}

float PSSM(Camera camera, int i)
{
	float k = float(i)/float(camera.CSM_levels);
	return mix(camera.near + (camera.far - camera.near)*k, camera.near * pow(camera.far / camera.near, k), 0.75);
}

int locate_CSM_leveli(Camera camera, vec3 world_pos)
{
	vec3 view_pos = world_to_view(camera, world_pos);
	if (view_pos.y < PSSM(camera, 0))
		return 0;
	for (int i = 0; i < camera.CSM_levels; i++)
	{
		float z0 = PSSM(camera, i);
		float z1 = PSSM(camera, i+1);
		if (z0 <= view_pos.y && view_pos.y <= z1)
			return i;
	}
	return int(camera.CSM_levels-1);
}

float locate_CSM_level(Camera camera, vec3 world_pos)
{
	vec3 view_pos = world_to_view(camera, world_pos);
	if (view_pos.y < PSSM(camera, 0))
		return 0;

	float level = camera.CSM_levels-1;
	for (int i = 0; i < camera.CSM_levels; i++)
	{
		float z0 = PSSM(camera, i);
		float z1 = PSSM(camera, i+1);
		if (z0 <= view_pos.y && view_pos.y <= z1)
		{
			level = soft_floor(i + (view_pos.y - z0) / (z1 - z0), 0.5);
			break;
		}
	}
	return clamp(level, 0, camera.CSM_levels-1);
}

BoundingSphere Frustum_bounding_sphere(Camera camera, int i)
{
	float z0 = PSSM(camera, i);
	float z1 = PSSM(camera, i+1);
	float clip = z1 - z0;
	if (i+1 < camera.CSM_levels) z1 += 0.5*clip;

	float ratio = camera.tan_half_fov * sqrt(1 + camera.aspect*camera.aspect);
	float R0 = z0 * ratio;
	float R1 = z1 * ratio;

	BoundingSphere bounding_sphere;
	bounding_sphere.radius = R1;
	bounding_sphere.center = vec3(0, z1, 0);
	float h = z1 - z0;
	float theta = atan(h/(R1-R0));
	if (theta > PI/4)
	{
		bounding_sphere.radius = sqrt(h*h / 4 + (R1*R1 + R0*R0)/2 + pow(R1*R1 - R0*R0, 2)/(4*h*h));
		bounding_sphere.center.y = z0 + 0.5*(h + (R1*R1 - R0*R0)/h);
	}

	bounding_sphere.center = view_to_world(camera, bounding_sphere.center);
	return bounding_sphere;
}

Camera cube_camera(int face_id, vec3 center_pos, float near, float far)
{
	Camera camera;
	camera.abs_position = center_pos;
	camera.near = near;
	camera.far = far;
	camera.tan_half_fov = 1;
	camera.sin_half_fov = sin45;
	camera.aspect = 1;
	camera.projection_mode = CAMERA_PROJECTION_PERSPECTIVE;
	switch(face_id)
	{
	case 0: camera.abs_orientation = quat(cos45, 0, 0, -sin45); break;
	case 1: camera.abs_orientation = quat(cos45, 0, 0, sin45); break;
	case 2: camera.abs_orientation = quat(cos45, -sin45, 0, 0); break;
	case 3: camera.abs_orientation = quat(cos45, sin45, 0, 0); break;
	case 4: camera.abs_orientation = quat(1, 0, 0, 0); break;
	case 5: camera.abs_orientation = quat(0, 0, 0, 1); break;
	}
	return camera;
}

Camera cube_camera(int face_id, vec3 center_pos)
{
	return cube_camera(face_id, center_pos, 0.1, 100);
}

Camera cube_camera(int face_id)
{
	return cube_camera(face_id, vec3(0), 0.1, 100);
}