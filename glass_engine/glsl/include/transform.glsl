#ifndef _TRANSFORM_GLSL_
#define _TRANSFORM_GLSL_

#include "quat.glsl"

struct RigidTransform
{
	vec3 abs_position;
	quat abs_orientation;
};

struct SimilarTransform
{
	float abs_scale;
	vec3 abs_position;
	quat abs_orientation;
};

vec3 transform_apply(SimilarTransform tran, vec3 coord)
{
	return quat_apply(tran.abs_orientation, tran.abs_scale*coord) + tran.abs_position;
}

vec3 transform_apply_to_normal(SimilarTransform tran, vec3 normal)
{
	return normalize(quat_apply(tran.abs_orientation, normal));
}

mat3 transform_apply_to_TBN(SimilarTransform tran, mat3 TBN)
{
	vec3 t = TBN[0];
	vec3 b = TBN[1];
	vec3 n = TBN[2];

	t = quat_apply(tran.abs_orientation, tran.abs_scale * t);
	b = quat_apply(tran.abs_orientation, tran.abs_scale * b);
	n = normalize(quat_apply(tran.abs_orientation, n));
	return mat3(t, b, n);
}

vec3 transform_apply(RigidTransform tran, vec3 coord)
{
	return quat_apply(tran.abs_orientation, coord) + tran.abs_position;
}

vec3 transform_apply_to_normal(RigidTransform tran, vec3 normal)
{
	return quat_apply(tran.abs_orientation, normal);
}

mat3 transform_apply_to_TBN(RigidTransform tran, mat3 TBN)
{
	vec3 t = TBN[0];
	vec3 b = TBN[1];
	vec3 n = TBN[2];

	t = quat_apply(tran.abs_orientation, t);
	b = quat_apply(tran.abs_orientation, b);
	n = quat_apply(tran.abs_orientation, n);
	return mat3(t, b, n);
}

vec3 transform_apply(mat4 tran, vec3 coord)
{
	vec4 result = tran * vec4(coord, 1);
	return result.xyz;
}

vec3 transform_apply_to_normal(mat4 tran, vec3 normal)
{
	mat3 A = mat3(tran);
	float det = determinant(A);
	if (abs(det) < 1E-6)
	{
		return vec3(0);
	}
	
	return sign(det) * normalize(transpose(inverse(mat3(tran))) * normal);
}

mat3 transform_apply_to_TBN(mat4 tran, mat3 TBN)
{
	vec3 t = TBN[0];
	vec3 b = TBN[1];
	vec3 n = TBN[2];

	t = mat3(tran) * t;
	b = mat3(tran) * b;
	n = transform_apply_to_normal(tran, n);
	return mat3(t, b, n);
}

mat3 cross_mat(vec3 v)
{
	return mat3(
		vec3(0, v.z, -v.y),
		vec3(-v.z, 0, v.x),
		vec3(v.y, -v.x, 0)
	);
}

mat3 axis_angle_mat(vec3 axis, float theta)
{
	if (abs(theta) < 1E-6)
	{
		return mat3(1);
	}

    float cos_theta = cos(theta);
    float sin_theta = sin(theta);
    return cos_theta*mat3(1) + (1 - cos_theta)*mat3(axis.x*axis, axis.y*axis, axis.z*axis) - sin_theta*cross_mat(axis);
}

#endif