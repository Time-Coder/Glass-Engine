#ifndef _TRANSFORM_GLSL__
#define _TRANSFORM_GLSL__

#include "quat.glsl"

struct Transform
{
	vec3 abs_scale;
	vec3 abs_position;
	quat abs_orientation;
};

vec3 transform_apply(Transform tran, vec3 coord)
{
	return quat_apply(tran.abs_orientation, tran.abs_scale*coord) + tran.abs_position;
}

vec3 transform_apply_to_normal(Transform tran, vec3 normal)
{
	float sx = tran.abs_scale.x;
	float sy = tran.abs_scale.y;
	float sz = tran.abs_scale.z;
	return quat_apply(tran.abs_orientation, vec3(sz*sy, sx*sz, sx*sy) * normal);
}

mat3 transform_apply_to_TBN(Transform tran, mat3 TBN)
{
	vec3 t = TBN[0];
	vec3 b = TBN[1];
	vec3 n = TBN[2];

	float sx = tran.abs_scale.x;
	float sy = tran.abs_scale.y;
	float sz = tran.abs_scale.z;

	t = quat_apply(tran.abs_orientation, tran.abs_scale * t);
	b = quat_apply(tran.abs_orientation, tran.abs_scale * b);
	n = normalize(quat_apply(tran.abs_orientation, vec3(sz*sy, sx*sz, sx*sy) * n));
	return mat3(t, b, n);
}

#endif