from .genType import genType
from .helper import is_number


def abs(x:genType)->genType:
    result:genType = genType()
    for i in range(len(x._data)):
        current_value = x._data[i]
        if current_value < 0:
            current_value = -current_value
        result._data[i] = current_value
    return result

def sign(x:genType)->genType:
    result:genType = genType()
    for i in range(len(x._data)):
        current_value = x._data[i]
        if current_value > 0:
            result._data[i] = 1
        elif current_value < 0:
            result._data[i] = -1
        else:
            result._data[i] = 0
            
    return result

# floor(genType x) / ceil / trunc / round / roundEven	取整
# fract(genType x)	取小数部分
# mod(genType x, genType y) / mod(genType x, float y)	取模
# min(genType x, genType y) / max	最小、最大
# clamp(genType x, genType minVal, genType maxVal)	区间夹值
# mix(genType x, genType y, genType a) / mix(genType x, genType y, float a)	线性插值
# step(genType edge, genType x) / smoothstep(genType edge0, genType edge1, genType x)	阶梯/平滑阶梯
# sqrt(genType x) / inversesqrt	平方根、反平方根
# pow(genType x, genType y)	幂
# exp(genType x) / exp2 / log / log2	指数/对数
# sin / cos / tan / asin / acos / atan	三角函数
# sinh / cosh / tanh / asinh / acosh / atanh	双曲函数
# length(vecN x)	向量长度
# normalize(vecN x)	单位化
# distance(vecN p0, vecN p1)	两点距离
# dot(vecN x, vecN y)	点积
# cross(vec3 x, vec3 y)	叉积（仅 vec3）
# reflect(vecN I, vecN N)	反射向量
# refract(vecN I, vecN N, float eta)	折射向量
# faceforward(vecN N, vecN I, vecN Nref)	翻转法线
# determinant(matN m)	行列式
# transpose(matC×R m)	转置
# inverse(matN m)