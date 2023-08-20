#ifndef _LINGLG_GLSL__
#define _LINGLG_GLSL__

void qr(mat3 A, out mat3 Q, out mat3 R)
{
    Q[0] = normalize(A[0]);

    Q[1] = A[1] - dot(A[1], Q[0]) * Q[0];
    Q[1] = normalize(Q[1]);

    Q[2] = A[2] - dot(A[2], Q[0]) * Q[0] - dot(A[2], Q[1]) * Q[1];
    Q[2] = normalize(Q[2]);
    
    R[0] = vec3(dot(Q[0], A[0]), 0, 0);
    R[1] = vec3(dot(Q[0], A[1]), dot(Q[1], A[1]), 0);
    R[2] = vec3(dot(Q[0], A[2]), dot(Q[1], A[2]), dot(Q[2], A[2]));
}

#endif