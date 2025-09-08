from .genType import genType
from .genVec import genVec
from .genMat import genMat
from .genQuat import genQuat
from .genVec3 import genVec3
from .helper import is_number
from typing import Callable, Any, Union
import math
import ctypes


def _single_op(x:genType, op:Callable[[Any,Any], Any], op_name:str)->genType:
    if is_number(x):
        return op(x)
    elif isinstance(x, genType):
        result:genType = x.__class__()
        for i in range(len(x._data)):
            result._data[i] = op(x._data[i])
        return result
    else:
        raise TypeError(f"{op_name} not supported for type {x.__class__.__name__}")

def abs(x:genType)->genType:
    return _single_op(x, __builtins__.abs, "abs")

def sign(x:genType)->genType:
    return _single_op(x, lambda x: math.copysign(1, x), "sign")

def floor(x:genType)->genType:
    return _single_op(x, math.floor, "floor")
    
def ceil(x:genType)->genType:
    return _single_op(x, math.ceil, "ceil")

def trunc(x:genType)->genType:
    return _single_op(x, math.trunc, "trunc")

def round(x:genType)->genType:
    return _single_op(x, lambda x: math.floor(x + 0.5) if x >= 0 else math.ceil(x - 0.5), "round")

def roundEven(x:genType)->genType:
    return _single_op(x, round, "roundEven")

def fract(x:genType)->genType:
    return _single_op(x, lambda x: x - math.trunc(x), "roundEven")

def mod(x:genType, y:genType)->genType:
    return x % y

def _bin_op(x:genType, y:genType, op:Callable[[Any,Any], Any], op_name:str)->genType:
    result_type = genType._bin_op_type(op_name, x, y)
    if is_number(x) and is_number(y):
        return op(x, y)
    elif isinstance(x, genType) and is_number(y):
        result:genType = result_type()
        for i in range(len(x._data)):
            result._data[i] = op(x._data[i], y)
        return result
    elif is_number(x) and isinstance(y, genType):
        result:genType = result_type()
        for i in range(len(y._data)):
            result._data[i] = op(x, y._data[i])
        return result
    elif isinstance(x, genType) and isinstance(y, genType):
        if x.math_form != y.math_form or x.shape != y.shape:
            raise TypeError(f"not defined {op_name} between '{x.__class__.__name__}' and '{y.__class__.__name__}'")

        result:genType = result_type()
        for i in range(len(x._data)):
            result._data[i] = op(x._data[i], y._data[i])

        return result
    else:
        raise TypeError(f"not defined {op_name} between '{x.__class__.__name__}' and '{y.__class__.__name__}'")

def min(x:genType, y:genType)->genType:
    return _bin_op(x, y, __builtins__.min, "min")

def max(x:genType, y:genType)->genType:
    return _bin_op(x, y, __builtins__.max, "max")

def clamp(x:genType, min_value:genType, max_value:genType)->genType:
    return min(max(x, min_value), max_value)
    
def mix(x:genType, y:genType, a:genType)->genType:
    return (x * (1.0 - a)) + (y * a)

def step(edge:genType, x:genType)->genType:
    return _bin_op(edge, x, lambda edge, x: float(x >= edge), "step")

def _smoothstep(edge0: float, edge1: float, x: float) -> float:
    if x <= edge0:
        return 0.0
    if x >= edge1:
        return 1.0
    t = (x - edge0) / (edge1 - edge0)
    return t * t * (3.0 - 2.0 * t)

def smoothstep(edge0: genType, edge1: genType, x: genType)->genType:
    if (not (is_number(edge0) and is_number(edge1))) and not edge0._is_homo(edge1):
        raise ValueError('edge0 and edge1 must be same type')
    
    return _bin_op(edge1, x, lambda edge1, x: _smoothstep(edge0, edge1, x), "smoothstep")

def sqrt(x: genType)->genType:
    return _single_op(x, math.sqrt, "sqrt")

def inversesqrt(x: genType)->genType:
    return _single_op(x, lambda x: 1 / math.sqrt(x), "inversesqrt")

def pow(x: genType, y: genType)->genType:
    return x ** y

def exp(x: genType)->genType:
    return _single_op(x, math.exp, "exp")

def exp2(x: genType)->genType:
    return _single_op(x, lambda x: 2 ** x, "exp2")

def exp10(x: genType)->genType:
    return _single_op(x, lambda x: 10 ** x, "exp10")

def log(x: genType)->genType:
    return _single_op(x, math.log, "log")

def log2(x: genType)->genType:
    return _single_op(x, lambda x: math.log(x) / math.log(2), "log2")

def log10(x: genType)->genType:
    return _single_op(x, lambda x: math.log(x) / math.log(10), "log10")

def sin(x: genType)->genType:
    return _single_op(x, math.sin, "sin")

def cos(x: genType)->genType:
    return _single_op(x, math.cos, "cos")

def tan(x: genType)->genType:
    return _single_op(x, math.tan, "tan")

def asin(x: genType)->genType:
    return _single_op(x, math.asin, "asin")

def acos(x: genType)->genType:
    return _single_op(x, math.acos, "acos")

def atan(x: genType)->genType:
    return _single_op(x, math.atan, "atan")

def sinh(x: genType)->genType:
    return _single_op(x, math.sinh, "sinh")

def cosh(x: genType)->genType:
    return _single_op(x, math.cosh, "cosh")

def tanh(x: genType)->genType:
    return _single_op(x, math.tanh, "tanh")

def asinh(x: genType)->genType:
    return _single_op(x, math.asinh, "asinh")

def acosh(x: genType)->genType:
    return _single_op(x, math.acosh, "acosh")

def atanh(x: genType)->genType:
    return _single_op(x, math.atanh, "atanh")

def length(x: genType)->float:
    if is_number(x):
        return abs(x)
    
    sum: float = 0
    for i in range(len(x._data)):
        sum += x._data[i] ** 2

    return math.sqrt(sum)

def normalize(x: genType)->genType:
    return x / length(x)

def distance(x: genType, y: genType)->float:
    return length(x - y)

def dot(x: genType, y: genType)->float:
    if not isinstance(x, genType) or not isinstance(y, genType) or not x._is_homo(y):
        raise TypeError(f"not defined dot between '{x.__class__.__name__}' and '{y.__class__.__name__}'")

    sum: float = 0
    for i in range(len(x._data)):
        sum += x._data[i] * y._data[i]

    return sum

def cross(x: genVec3, y: genVec3)->genVec3:
    if not isinstance(x, genVec3) or not isinstance(y, genVec3):
        raise TypeError(f"not defined cross between '{x.__class__.__name__}' and '{y.__class__.__name__}'")

    result_dtype:type = ctypes.c_double if (x.dtype == ctypes.c_double or y.dtype == ctypes.c_double) else ctypes.c_float
    result_type:type = genVec.vec_type(result_dtype, 3)
    return result_type(x.y * y.z - x.z * y.y, x.z * y.x - x.x * y.z, x.x * y.y - x.y * y.x)

def reflect(I:genVec, N:genVec)->genVec:
    return I - 2 * dot(I, N) * N

def refract(I:genVec, N:genVec, eta:float)->genVec:
    return I - (eta * dot(I, N) + sqrt(1 - eta * eta * (1 - dot(I, N) * dot(I, N)))) * N

def faceforward(N:genVec, I:genVec, Nref:genVec)->genVec:
    return (N if dot(Nref, I) < 0 else -N)

def determinant(m:genMat)->float:
    if not isinstance(m, genMat) or m.rows != m.cols:
        raise TypeError(f'not defined determinant for {m.__class__.__name__}')

    if m.rows == 2:
        return m[0, 0] * m[1, 1] - m[0, 1] * m[1, 0]

    if m.rows == 3:
        return (m[0, 0] * m[1, 1] * m[2, 2] + 
                m[0, 1] * m[1, 2] * m[2, 0] + 
                m[0, 2] * m[1, 0] * m[2, 1] - 
                m[0, 2] * m[1, 1] * m[2, 0] - 
                m[0, 0] * m[1, 2] * m[2, 1] - 
                m[0, 1] * m[1, 0] * m[2, 2])

    if m.rows == 4:
        det = 0.0
        for col in range(4):
            submatrix_data = []
            for i in range(4):
                if i == col:
                    continue
                for j in range(1, 4):
                    submatrix_data.append(m[i, j])
            
            import ctypes
            submatrix_type = genMat.mat_type(ctypes.c_double, 3, 3)
            submatrix = submatrix_type()
            for i in range(3):
                for j in range(3):
                    submatrix[i, j] = submatrix_data[i * 3 + j]
            
            cofactor = ((-1) ** col) * m[col, 0] * determinant(submatrix)
            det += cofactor
            
        return det

def transpose(m:genMat)->genMat:
    if not isinstance(m, genMat):
        raise TypeError(f'not defined transpose for {m.__class__.__name__}')
    
    result_type:type = genMat.mat_type(m.dtype, m.shape[::-1])
    result:genMat = result_type()
    for i in range(result.rows):
        for j in range(result.cols):
            result[j, i] = m[i, j]

    return result

def trace(m:genMat)->float:
    if not isinstance(m, genMat) or m.rows != m.cols:
        raise TypeError(f'not defined trace for {m.__class__.__name__}')
    
    trace:float = 0.0
    for i in range(m.rows):
        trace += m[i, i]
    
    return trace

def conjugate(m:genQuat)->genQuat:
    if not isinstance(m, genQuat):
        raise TypeError(f'not defined conjugate for {m.__class__.__name__}')
    
    return m.__class__(m.w, -m.x, -m.y, -m.z)

def inverse(m:Union[genMat, genQuat])->Union[genMat, genQuat]:
    if isinstance(m, genQuat):
        return conjugate(m) / length(m)
    
    if not isinstance(m, genMat) or m.rows != m.cols:
        raise TypeError(f'not defined inverse for {m.__class__.__name__}')
    
    result_dtype:type = (ctypes.c_double if m.dtype == ctypes.c_double else ctypes.c_float)
    result_type:type = genMat.mat_type(result_dtype, m.shape)

    det = determinant(m)
    if det == 0:
        raise ValueError("Matrix is not invertible (determinant is zero)")

    result = result_type()

    if m.rows == 2:
        result[0, 0] = m[1, 1] / det
        result[1, 1] = m[0, 0] / det
        result[0, 1] = -m[0, 1] / det
        result[1, 0] = -m[1, 0] / det
        return result

    if m.rows == 3:
        result[0, 0] = (m[1, 1] * m[2, 2] - m[1, 2] * m[2, 1]) / det
        result[1, 0] = -(m[1, 0] * m[2, 2] - m[1, 2] * m[2, 0]) / det
        result[2, 0] = (m[1, 0] * m[2, 1] - m[1, 1] * m[2, 0]) / det
        
        result[0, 1] = -(m[0, 1] * m[2, 2] - m[0, 2] * m[2, 1]) / det
        result[1, 1] = (m[0, 0] * m[2, 2] - m[0, 2] * m[2, 0]) / det
        result[2, 1] = -(m[0, 0] * m[2, 1] - m[0, 1] * m[2, 0]) / det
        
        result[0, 2] = (m[0, 1] * m[1, 2] - m[0, 2] * m[1, 1]) / det
        result[1, 2] = -(m[0, 0] * m[1, 2] - m[0, 2] * m[1, 0]) / det
        result[2, 2] = (m[0, 0] * m[1, 1] - m[0, 1] * m[1, 0]) / det
        
        return result

    if m.rows == 4:
        for i in range(4):
            for j in range(4):
                submatrix_data = []
                for col in range(4):
                    if col == i:
                        continue
                    for row in range(4):
                        if row == j:
                            continue
                        submatrix_data.append(m[col, row])
                
                submatrix_type = genMat.mat_type(ctypes.c_double, 3, 3)
                submatrix = submatrix_type()
                for col in range(3):
                    for row in range(3):
                        submatrix[col, row] = submatrix_data[col * 3 + row]
                
                cofactor = ((-1) ** (i + j)) * determinant(submatrix)
                result[j, i] = cofactor / det
        
        return result
    
def matrixCompMult(x:genMat, y:genMat)->genMat:
    if not isinstance(x, genMat) or not isinstance(y, genMat) or x.shape != y.shape:
        raise TypeError(f"not defined matrixCompMult between '{x.__class__.__name__}' and '{y.__class__.__name__}'")

    result_type:type = genType._bin_op_type('*', x, y)
    result:genMat = result_type()

    for i in range(x.rows):
        for j in range(y.cols):
            result[j, i] = x[j, i] * y[j, i]

    return result

def outerProduct(x:genVec, y:genVec)->genMat:
    if not isinstance(x, genVec) or not isinstance(y, genVec):
        raise TypeError(f"not defined outerProduct between '{x.__class__.__name__}' and '{y.__class__.__name__}'")
    
    result_dtype:type = genType._bin_op_dtype('*', x.dtype, y.dtype)
    result_type:type = genMat.gen_type(result_dtype, (len(y), len(x)))
    result:genMat = result_type()

    for i in range(len(x)):
        for j in range(len(y)):
            result[j, i] = x._data[i] * y._data[j]

    return result

def lessThan(x:genType, y:genType)->genType:
    return x < y

def lessThanEqual(x:genType, y:genType)->genType:
    return x <= y

def greaterThan(x:genType, y:genType)->genType:
    return x > y

def greaterThanEqual(x:genType, y:genType)->genType:
    return x >= y

def equal(x:genType, y:genType)->genType:
    return x._compare_op("==", y)

def notEqual(x:genType, y:genType)->genType:
    return x._compare_op("!=", y)

def any(x:genType)->bool:
    if not isinstance(x, genType):
        return bool(x)
    
    for i in range(len(x._data)):
        if x._data[i]:
            return True

    return False

def all(x:genType)->bool:
    if not isinstance(x, genType):
        return bool(x)
    
    for i in range(len(x._data)):
        if not x._data[i]:
            return False

    return True

def not_(x:genType):
    if not isinstance(x, genType):
        return (not x)

    result:genType = genType.gen_type(x.math_form, ctypes.c_bool, x.shape)
    for i in range(len(x._data)):
        result._data[i] = not x._data[i]

    return result

def sizeof(x:genType)->int:
    return ctypes.sizeof(x._data)

def value_ptr(x:genType):
    return x._data