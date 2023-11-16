bool hasnan(float x)
{
    return isnan(x);
}

bool hasnan(double x)
{
    return isnan(x);
}

bool hasnan(vec2 v)
{
    return (isnan(v.x) || isnan(v.y));
}

bool hasnan(dvec2 v)
{
    return (isnan(v.x) || isnan(v.y));
}

bool hasnan(vec3 v)
{
    return (isnan(v.x) || isnan(v.y) || isnan(v.z));
}

bool hasnan(dvec3 v)
{
    return (isnan(v.x) || isnan(v.y) || isnan(v.z));
}

bool hasnan(vec4 v)
{
    return (isnan(v.x) || isnan(v.y) || isnan(v.z) || isnan(v.w));
}

bool hasnan(dvec4 v)
{
    return (isnan(v.x) || isnan(v.y) || isnan(v.z) || isnan(v.w));
}

bool hasinf(float x)
{
    return isinf(x);
}

bool hasinf(double x)
{
    return isinf(x);
}

bool hasinf(vec2 v)
{
    return (isinf(v.x) || isinf(v.y));
}

bool hasinf(dvec2 v)
{
    return (isinf(v.x) || isinf(v.y));
}

bool hasinf(vec3 v)
{
    return (isinf(v.x) || isinf(v.y) || isinf(v.z));
}

bool hasinf(dvec3 v)
{
    return (isinf(v.x) || isinf(v.y) || isinf(v.z));
}

bool hasinf(vec4 v)
{
    return (isinf(v.x) || isinf(v.y) || isinf(v.z) || isinf(v.w));
}

bool hasinf(dvec4 v)
{
    return (isinf(v.x) || isinf(v.y) || isinf(v.z) || isinf(v.w));
}

#define DEFINE_MAT_HAS_NAN_INF(rows, cols) \
bool hasnan(mat##rows##x##cols A)\
{\
    for (int i = 0; i < rows; i++)\
    {\
        for (int j = 0; j < cols; j++)\
        {\
            if (isnan(A[j][i]))\
            {\
                return true;\
            }\
        }\
    }\
    return false;\
}\
bool hasnan(dmat##rows##x##cols A)\
{\
    for (int i = 0; i < rows; i++)\
    {\
        for (int j = 0; j < cols; j++)\
        {\
            if (isnan(A[j][i]))\
            {\
                return true;\
            }\
        }\
    }\
    return false;\
}\
bool hasinf(mat##rows##x##cols A)\
{\
    for (int i = 0; i < rows; i++)\
    {\
        for (int j = 0; j < cols; j++)\
        {\
            if (isinf(A[j][i]))\
            {\
                return true;\
            }\
        }\
    }\
    return false;\
}\
bool hasinf(dmat##rows##x##cols A)\
{\
    for (int i = 0; i < rows; i++)\
    {\
        for (int j = 0; j < cols; j++)\
        {\
            if (isinf(A[j][i]))\
            {\
                return true;\
            }\
        }\
    }\
    return false;\
}

DEFINE_MAT_HAS_NAN_INF(2, 2)
DEFINE_MAT_HAS_NAN_INF(2, 3)
DEFINE_MAT_HAS_NAN_INF(2, 4)
DEFINE_MAT_HAS_NAN_INF(3, 2)
DEFINE_MAT_HAS_NAN_INF(3, 3)
DEFINE_MAT_HAS_NAN_INF(3, 4)
DEFINE_MAT_HAS_NAN_INF(4, 2)
DEFINE_MAT_HAS_NAN_INF(4, 3)
DEFINE_MAT_HAS_NAN_INF(4, 4)