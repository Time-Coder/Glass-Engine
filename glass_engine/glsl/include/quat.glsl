struct quat
{
	float w;
	float x;
	float y;
	float z;
};

quat vec3_to_quat(vec3 v)
{
	quat q;
	q.w = 0;
	q.x = v.x;
	q.y = v.y;
	q.z = v.z;
	return q;
}

quat vec4_to_quat(vec4 v)
{
	quat q;
	q.w = v[0];
	q.x = v[1];
	q.y = v[2];
	q.z = v[3];
	return q;
}

quat quat_conj(quat q)
{
	quat p;
	p.w = q.w;
	p.x = -q.x;
	p.y = -q.y;
	p.z = -q.z;
	return p;
}

quat quat_mult(quat p, quat q)
{
    quat pq;
    pq.w = p.w*q.w - p.x*q.x - p.y*q.y - p.z*q.z;
	pq.x = p.w*q.x + p.x*q.w + p.y*q.z - p.z*q.y;
	pq.y = p.w*q.y - p.x*q.z + p.y*q.w + p.z*q.x;
	pq.z = p.w*q.z + p.x*q.y - p.y*q.x + p.z*q.w;
    return pq;
}

float quat_norm(quat q)
{
	return sqrt(q.w*q.w + q.x*q.x + q.y*q.y + q.z*q.z);
}

quat quat_normalize(quat q)
{
	quat result;
	float norm = quat_norm(q);
	result.w = q.w / norm;
	result.x = q.x / norm;
	result.y = q.y / norm;
	result.z = q.z / norm;
	return result;
}

vec3 quat_apply(quat q, vec3 v)
{
    quat result = quat_mult(quat_mult(q, vec3_to_quat(v)), quat_conj(q));
    return vec3(result.x, result.y, result.z);
}

mat3 quat_to_mat3(quat q)
{
    return mat3(1.0-2.0*(q.y*q.y + q.z*q.z), 2.0*(q.x*q.y + q.w*q.z), 2.0*(q.x*q.z - q.w*q.y),
                2.0*(q.x*q.y - q.w*q.z), 1.0-2.0*(q.x*q.x + q.z*q.z), 2.0*(q.y*q.z + q.w*q.x),
                2.0*(q.x*q.z + q.w*q.y), 2.0*(q.y*q.z - q.w*q.x), 1.0-2.0*(q.x*q.x + q.y*q.y));
}

mat4 quat_to_mat4(quat q)
{
	return mat4(1.0-2.0*(q.y*q.y + q.z*q.z), 2.0*(q.x*q.y + q.w*q.z), 2.0*(q.x*q.z - q.w*q.y), 0.0,
                2.0*(q.x*q.y - q.w*q.z), 1.0-2.0*(q.x*q.x + q.z*q.z), 2.0*(q.y*q.z + q.w*q.x), 0.0,
                2.0*(q.x*q.z + q.w*q.y), 2.0*(q.y*q.z - q.w*q.x), 1.0-2.0*(q.x*q.x + q.y*q.y), 0.0,
                0.0,                     0.0,                     0.0,                         1.0);
}