import glm
import math
import copy
import numpy as np
from cacheout import Cache

cache = Cache(maxsize=100)

def fzero(f, interval):
    lower = interval[0]
    upper = interval[1]
    f_lower = f(lower)
    f_upper = f(upper)
    if np.sign(f_lower) == np.sign(f_upper):
        return None
    
    while upper - lower > 1E-6:
        middle = (lower + upper)/2
        f_middle = f(middle)
        if np.sign(f_middle) == np.sign(f_lower):
            f_lower = f_middle
            lower = middle
        else:
            f_upper = f_middle
            upper = middle

    return (lower + upper)/2

def angle_of(v1, v2):
    len_v1 = glm.length(v1)
    len_v2 = glm.length(v2)
    if len_v1 < 1E-6 or len_v2 < 1E-6:
        return 0

    cos_theta = glm.dot(v1, v2) / (len_v1 * len_v2)
    if cos_theta < -1:
        cos_theta = -1
    if cos_theta > 1:
        cos_theta = 1

    return math.acos(cos_theta)

def cos_angle_of(v1, v2):
    len_v1 = glm.length(v1)
    len_v2 = glm.length(v2)
    if len_v1 < 1E-6 or len_v2 < 1E-6:
        return 0

    cos_theta = glm.dot(v1, v2) / (len_v1 * len_v2)
    if cos_theta < -1:
        cos_theta = -1
    if cos_theta > 1:
        cos_theta = 1
        
    return cos_theta

def approx_pos(pos, precision:int=7):
    return glm.vec3(round(pos.x, precision), round(pos.y, precision), round(pos.z, precision))

def hash_pos(pos, precision:int=7):
    negtive_zero = "-0." + "0"*precision
    zero = "0." + "0"*precision

    x_str = eval('f"{pos.x:.'+str(precision)+'f}"')
    if x_str == negtive_zero:
        x_str = zero

    y_str = eval('f"{pos.y:.'+str(precision)+'f}"')
    if y_str == negtive_zero:
        y_str = zero

    z_str = eval('f"{pos.z:.'+str(precision)+'f}"')
    if z_str == negtive_zero:
        z_str = zero

    return f"({x_str}, {y_str}, {z_str})"

def bounding_box(vertices):
    x_min = float("inf")
    x_max = -float("inf")
    y_min = float("inf")
    y_max = -float("inf")
    z_min = float("inf")
    z_max = -float("inf")

    if not vertices:
        return (x_min, x_max, y_min, y_max, z_min, z_max)
    
    for vertex in vertices:
        if vertex.position.x < x_min:
            x_min = vertex.position.x
        if vertex.position.x > x_max:
            x_max = vertex.position.x

        if vertex.position.y < y_min:
            y_min = vertex.position.y
        if vertex.position.y > y_max:
            y_max = vertex.position.y

        if vertex.position.z < z_min:
            z_min = vertex.position.z
        if vertex.position.z > z_max:
            z_max = vertex.position.z

    return (x_min, x_max, y_min, y_max, z_min, z_max)

def is_closed(vertices, indices):
    if not indices:
        return False
    
    points_map = {}
    for index in indices:
        vertex0 = vertices[index[0]]
        vertex1 = vertices[index[1]]
        vertex2 = vertices[index[2]]

        hash_pos0 = hash_pos(vertex0.position)
        hash_pos1 = hash_pos(vertex1.position)
        hash_pos2 = hash_pos(vertex2.position)

        v01 = glm.normalize(vertex1.position - vertex0.position)
        v10 = -v01
        v02 = glm.normalize(vertex2.position - vertex0.position)
        v20 = -v02
        v12 = glm.normalize(vertex2.position - vertex1.position)
        v21 = -v12

        hash_v01 = hash_pos(v01)
        hash_v10 = hash_pos(v10)
        hash_v02 = hash_pos(v02)
        hash_v20 = hash_pos(v20)
        hash_v12 = hash_pos(v12)
        hash_v21 = hash_pos(v21)

        # 0
        if hash_pos0 not in points_map:
            points_map[hash_pos0] = set()

        if hash_v01 not in points_map[hash_pos0]:
            points_map[hash_pos0].add(hash_v01)
        else:
            points_map[hash_pos0].remove(hash_v01)
            if not points_map[hash_pos0]:
                del points_map[hash_pos0]

        if hash_v02 not in points_map[hash_pos0]:
            points_map[hash_pos0].add(hash_v02)
        else:
            points_map[hash_pos0].remove(hash_v02)
            if not points_map[hash_pos0]:
                del points_map[hash_pos0]

        # 1
        if hash_pos1 not in points_map:
            points_map[hash_pos1] = set()

        if hash_v10 not in points_map[hash_pos1]:
            points_map[hash_pos1].add(hash_v10)
        else:
            points_map[hash_pos1].remove(hash_v10)
            if not points_map[hash_pos1]:
                del points_map[hash_pos1]

        if hash_v12 not in points_map[hash_pos1]:
            points_map[hash_pos1].add(hash_v12)
        else:
            points_map[hash_pos1].remove(hash_v12)
            if not points_map[hash_pos1]:
                del points_map[hash_pos1]

        # 2
        if hash_pos2 not in points_map:
            points_map[hash_pos2] = set()

        if hash_v20 not in points_map[hash_pos2]:
            points_map[hash_pos2].add(hash_v20)
        else:
            points_map[hash_pos2].remove(hash_v20)
            if not points_map[hash_pos2]:
                del points_map[hash_pos2]

        if hash_v21 not in points_map[hash_pos2]:
            points_map[hash_pos2].add(hash_v21)
        else:
            points_map[hash_pos2].remove(hash_v21)
            if not points_map[hash_pos2]:
                del points_map[hash_pos2]
    
    return (not points_map)

def generate_auto_TBN(vertices, indices, calculate_normal=True):

    points_map = {}

    for index in indices:
        vertex0 = vertices[index[0]]
        vertex1 = vertices[index[1]]
        vertex2 = vertices[index[2]]
        vertex = [vertex0, vertex1, vertex2]

        pos0_key = hash_pos(vertex0.position)
        pos1_key = hash_pos(vertex1.position)
        pos2_key = hash_pos(vertex2.position)
        pos_keys = [pos0_key, pos1_key, pos2_key]

        v01 = vertex1.position - vertex0.position
        v02 = vertex2.position - vertex0.position
        v12 = vertex2.position - vertex1.position
        v10 = -v01
        v20 = -v02
        v21 = -v12

        weight0 = angle_of(v01, v02)
        weight1 = angle_of(v10, v12)
        weight2 = angle_of(v20, v21)
        weight = [weight0, weight1, weight2]

        normal = glm.cross(v01, v02)
        len_normal = glm.length(normal)
        if len_normal < 1E-6:
            continue
        normal /= len_normal

        st01 = vertex1.tex_coord - vertex0.tex_coord
        st02 = vertex2.tex_coord - vertex0.tex_coord
        det = st01.s * st02.t - st02.s * st01.t

        tangent = st02.t*v01 - st01.t*v02
        bitangent = st01.s*v02 - st02.s*v01
        if abs(det) < 1E-6:
            continue
        tangent /= det
        bitangent /= det

        for i in range(3):
            if pos_keys[i] not in points_map:
                points_map[pos_keys[i]] = \
                [
                    {
                        "tangent": tangent,
                        "bitangent": bitangent,
                        "normal": normal,
                        "weight": weight[i],
                        "vertices": {vertex[i]}
                    }
                ]
                vertex[i].tangent = tangent
                vertex[i].bitangent = bitangent
                if calculate_normal:
                    vertex[i].normal = normal
            else:
                nearest_info = None
                min_difference = float("inf")
                in_some_group = False
                for info in points_map[pos_keys[i]]:
                    old_normal = info["normal"]
                    old_tangent = info["tangent"]
                    old_bitangent = info["bitangent"]

                    normal_difference = angle_of(normal, old_normal)**2
                    tangent_difference = angle_of(tangent, old_tangent)**2 + abs(glm.length2(tangent) - glm.length2(old_tangent))
                    bitangent_difference = angle_of(bitangent, old_bitangent)**2 + abs(glm.length2(bitangent) - glm.length2(old_bitangent))
                    current_difference = normal_difference + tangent_difference + bitangent_difference

                    if current_difference < min_difference:
                        min_difference = current_difference
                        nearest_info = info

                    if vertex[i] in info["vertices"]:
                        in_some_group = True
                
                if min_difference < 0.01:
                    if vertex[i] not in nearest_info["vertices"]:
                        old_tangent = nearest_info["tangent"]
                        old_bitangent = nearest_info["bitangent"]
                        old_normal = nearest_info["normal"]
                        old_weight = nearest_info["weight"]

                        new_weight = old_weight + weight[i]
                        new_tangent = (old_weight*old_tangent + weight[i]*tangent)/new_weight
                        new_bitangent = (old_weight*old_bitangent + weight[i]*bitangent)/new_weight
                        new_normal = glm.normalize(old_weight * old_normal + weight[i] * normal)
                        new_vertex = copy.deepcopy(vertex[i]) if in_some_group else vertex[i]

                        new_vertex.tangent = new_tangent
                        new_vertex.bitangent = new_bitangent
                        if calculate_normal:
                            new_vertex.normal = new_normal

                        nearest_info["tangent"] = new_tangent
                        nearest_info["bitangent"] = new_bitangent
                        nearest_info["normal"] = new_normal
                        nearest_info["weight"] = new_weight
                        nearest_info["vertices"].add(new_vertex)
                        
                        if in_some_group:
                            new_index = len(vertices)
                            vertices.append(new_vertex)
                            index[i] = new_index
                else:
                    new_vertex = copy.deepcopy(vertex[i]) if in_some_group else vertex[i]
                    new_info = \
                    {
                        "tangent": tangent,
                        "bitangent": bitangent,
                        "normal": normal,
                        "weight": weight[i],
                        "vertices": {new_vertex}
                    }
                    points_map[pos_keys[i]].append(new_info)

                    new_vertex.tangent = tangent
                    new_vertex.bitangent = bitangent
                    if calculate_normal:
                        new_vertex.normal = normal

                    if in_some_group:
                        new_index = len(vertices)
                        vertices.append(new_vertex)
                        index[i] = new_index

            yield

    for infos in points_map.values():
        for info in infos:
            tangent = info["tangent"]
            bitangent = info["bitangent"]
            normal = info["normal"]
            for vertex in info["vertices"]:
                vertex.tangent = tangent
                vertex.bitangent = bitangent
                if calculate_normal:
                    vertex.normal = normal
                yield

    for vertex in vertices:
        pos_key = None
        if "tangent" not in vertex:
            pos_key = hash_pos(vertex.position)
            vertex.tangent = points_map[pos_key][0]["tangent"]

        if "bitangent" not in vertex:
            if pos_key is None:
                pos_key = hash_pos(vertex.position)
            vertex.bitangent = points_map[pos_key][0]["bitangent"]

        if calculate_normal and "normal" not in vertex:
            if pos_key is None:
                pos_key = hash_pos(vertex.position)
            vertex.normal = points_map[pos_key][0]["normal"]
            
def generate_smooth_TBN(vertices, indices, calculate_normal=True):

    points_map = {}

    for index in indices:
        vertex0 = vertices[index[0]]
        vertex1 = vertices[index[1]]
        vertex2 = vertices[index[2]]
        vertex = [vertex0, vertex1, vertex2]

        pos0_key = hash_pos(vertex0.position)
        pos1_key = hash_pos(vertex1.position)
        pos2_key = hash_pos(vertex2.position)
        pos_keys = [pos0_key, pos1_key, pos2_key]

        v01 = vertex1.position - vertex0.position
        v02 = vertex2.position - vertex0.position
        v12 = vertex2.position - vertex1.position
        v10 = -v01
        v20 = -v02
        v21 = -v12

        st01 = vertex1.tex_coord - vertex0.tex_coord
        st02 = vertex2.tex_coord - vertex0.tex_coord

        det = st01.s * st02.t - st02.s * st01.t

        weight0 = angle_of(v01, v02)
        weight1 = angle_of(v10, v12)
        weight2 = angle_of(v20, v21)
        weight = [weight0, weight1, weight2]

        normal = glm.cross(v01, v02)
        len_normal = glm.length(normal)
        if len_normal < 1E-6:
            continue
        normal /= len_normal

        tangent = st02.t*v01 - st01.t*v02
        bitangent = st01.s*v02 - st02.s*v01
        if abs(det) < 1E-6:
            continue
        tangent /= det
        bitangent /= det

        for i in range(3):
            if pos_keys[i] not in points_map:
                points_map[pos_keys[i]] = \
                {
                    "tangent": tangent,
                    "bitangent": bitangent,
                    "normal": normal,
                    "weight": weight[i],
                    "vertices": {vertex[i]}
                }
                vertex[i].tangent = tangent
                vertex[i].bitangent = bitangent
                if calculate_normal:
                    vertex[i].normal = normal
            else:
                nearest_info = points_map[pos_keys[i]]
                old_tangent = nearest_info["tangent"]
                old_bitangent = nearest_info["bitangent"]
                old_normal = nearest_info["normal"]
                old_weight = nearest_info["weight"]

                new_weight = old_weight + weight[i]
                if new_weight > 1E-6:
                    new_tangent = (old_weight * old_tangent + weight[i] * tangent)/new_weight
                    new_bitangent = (old_weight * old_bitangent + weight[i] * bitangent)/new_weight
                else:
                    new_tangent = 0.5*(old_tangent + tangent)
                    new_bitangent = 0.5*(old_bitangent + bitangent)
                new_normal = glm.normalize(old_weight * old_normal + weight[i] * normal)
                
                nearest_info["tangent"] = new_tangent
                nearest_info["bitangent"] = new_bitangent
                nearest_info["normal"] = new_normal
                nearest_info["weight"] = new_weight
                nearest_info["vertices"].add(vertex[i])
                vertex[i].tangent = new_tangent
                vertex[i].bitangent = new_bitangent
                if calculate_normal:
                    vertex[i].normal = new_normal
            yield
                
    for info in points_map.values():
        tangent = info["tangent"]
        bitangent = info["bitangent"]
        normal = info["normal"]
        for vertex in info["vertices"]:
            vertex.tangent = tangent
            vertex.bitangent = bitangent
            if calculate_normal:
                vertex.normal = normal
            yield

    for vertex in vertices:
        pos_key = None
        if "tangent" not in vertex:
            pos_key = hash_pos(vertex.position)
            vertex.tangent = points_map[pos_key]["tangent"]
            yield

        if "bitangent" not in vertex:
            if pos_key is None:
                pos_key = hash_pos(vertex.position)
            vertex.bitangent = points_map[pos_key]["bitangent"]
            yield

        if calculate_normal and "normal" not in vertex:
            if pos_key is None:
                pos_key = hash_pos(vertex.position)
            vertex.normal = points_map[pos_key]["normal"]
            yield

def generate_sharp_TBN(vertices, indices, calculate_normal=True):

    already_set_vertices = set()

    for index in indices:
        vertex0 = vertices[index[0]]
        vertex1 = vertices[index[1]]
        vertex2 = vertices[index[2]]
        vertex = [vertex0, vertex1, vertex2]

        v01 = vertex1.position - vertex0.position
        v02 = vertex2.position - vertex0.position

        st01 = vertex1.tex_coord - vertex0.tex_coord
        st02 = vertex2.tex_coord - vertex0.tex_coord

        det = st01.s * st02.t - st02.s * st01.t

        normal = glm.cross(v01, v02)
        len_normal = glm.length(normal)
        if len_normal < 1E-6:
            continue
        normal /= len_normal

        tangent = st02.t*v01 - st01.t*v02
        bitangent = st01.s*v02 - st02.s*v01
        if abs(det) < 1E-6:
            continue
        tangent /= det
        bitangent /= det

        for i in range(3):
            if vertex[i] in already_set_vertices:
                new_vertex = copy.deepcopy(vertex[i])
                new_vertex.tangent = tangent
                new_vertex.bitangent = bitangent
                if calculate_normal:
                    new_vertex.normal = normal
                new_index = len(vertices)
                index[i] = new_index
                vertices.append(new_vertex)
            else:
                vertex[i].tangent = tangent
                vertex[i].bitangent = bitangent
                if calculate_normal:
                    vertex[i].normal = normal
                already_set_vertices.add(vertex[i])

            yield

    for index in indices:
        vertex0 = vertices[index[0]]
        vertex1 = vertices[index[1]]
        vertex2 = vertices[index[2]]

        if "tangent" not in vertex0:
            if "tangent" in vertex1 and "tangent" not in vertex2:
                vertex0["tangent"] = vertex1["tangent"]
                vertex0["bitangent"] = vertex1["bitangent"]
                if calculate_normal:
                    vertex0["normal"] = vertex1["normal"]
            
            if "tangent" in vertex2 and "tangent" not in vertex1:
                vertex0["tangent"] = vertex2["tangent"]
                vertex0["bitangent"] = vertex2["bitangent"]
                if calculate_normal:
                    vertex0["normal"] = vertex2["normal"]

            if "tangent" in vertex1 and "tangent" in vertex2:
                vertex0["tangent"] = 0.5*(vertex1["tangent"] + vertex2["tangent"])
                vertex0["bitangent"] = 0.5*(vertex1["bitangent"] + vertex2["bitangent"])
                if calculate_normal:
                    vertex0["normal"] = glm.normalize(vertex1["normal"] + vertex2["normal"])

            yield

        if "tangent" not in vertex1:
            if "tangent" in vertex0 and "tangent" not in vertex2:
                vertex1["tangent"] = vertex0["tangent"]
                vertex1["bitangent"] = vertex0["bitangent"]
                if calculate_normal:
                    vertex1["normal"] = vertex0["normal"]
            
            if "tangent" in vertex2 and "tangent" not in vertex0:
                vertex1["tangent"] = vertex2["tangent"]
                vertex1["bitangent"] = vertex2["bitangent"]
                if calculate_normal:
                    vertex1["normal"] = vertex2["normal"]

            if "tangent" in vertex0 and "tangent" in vertex2:
                vertex1["tangent"] = 0.5*(vertex0["tangent"] + vertex2["tangent"])
                vertex1["bitangent"] = 0.5*(vertex0["bitangent"] + vertex2["bitangent"])
                if calculate_normal:
                    vertex1["normal"] = glm.normalize(vertex0["normal"] + vertex2["normal"])
                
            yield

        if "tangent" not in vertex2:
            if "tangent" in vertex0 and "tangent" not in vertex1:
                vertex2["tangent"] = vertex0["tangent"]
                vertex2["bitangent"] = vertex0["bitangent"]
                if calculate_normal:
                    vertex2["normal"] = vertex0["normal"]
            
            if "tangent" in vertex1 and "tangent" not in vertex0:
                vertex2["tangent"] = vertex1["tangent"]
                vertex2["bitangent"] = vertex1["bitangent"]
                if calculate_normal:
                    vertex2["normal"] = vertex1["normal"]

            if "tangent" in vertex0 and "tangent" in vertex1:
                vertex2["tangent"] = 0.5*(vertex0["tangent"] + vertex1["tangent"])
                vertex2["bitangent"] = 0.5*(vertex0["bitangent"] + vertex1["bitangent"])
                if calculate_normal:
                    vertex2["normal"] = glm.normalize(vertex0["normal"] + vertex1["normal"])

            yield

def line_intersect_plane(line_start:glm.vec3, line_direction:glm.vec3,
                         plane_start:glm.vec3, plane_normal:glm.vec3):
    A = plane_start
    B = line_start
    d = line_direction
    n = plane_normal
    AB = B - A

    return B - glm.dot(AB, n)/glm.dot(d, n) * d

def point_distance_to_line(point:glm.vec3, line_start:glm.vec3, line_direction:glm.vec3):
    A = line_start
    d = line_direction
    B = point

    AB = B - A
    return glm.length(glm.cross(AB, d))

def point_mirror_by_plane(point:glm.vec3, plane_start:glm.vec3, plane_normal:glm.vec3):
    d = plane_start - point
    return point + 2 * glm.dot(d, plane_normal) * plane_normal

def polygon_centroid(polygon):
    polygon = copy.copy(polygon)

    i = 1
    while i < len(polygon):
        while glm.length(polygon[i]-polygon[i-1]) < 1E-6:
            del polygon[i]

        i += 1

    O = None
    for point in polygon:
        if O is None:
            O = point
        else:
            O = O + point

    len_polygon = len(polygon)
    O /= len_polygon

    centroid = None
    weight_sum = 0
    for i in range(1, len_polygon+1):
        point0 = polygon[i-1]
        point1 = polygon[i] if i < len_polygon else polygon[0]
        center = (O + point0 + point1) / 3
        weight = glm.length(glm.cross(point0-O, point1-O))/2
        weight_sum += weight
        if centroid is None:
            centroid = weight * center
        else:
            centroid += weight * center

    return centroid / weight_sum

def polygon_normal(polygon, centroid=None):
    if centroid is None:
        centroid = polygon_centroid(polygon)

    normal = glm.vec3(0, 0, 0)
    weight_sum = 0
    len_polygon = len(polygon)
    for i in range(1, len_polygon+1):
        point0 = polygon[i-1]
        point1 = polygon[i] if i < len_polygon else polygon[0]

        v0 = point0 - centroid
        v1 = point1 - centroid

        n = glm.cross(v0, v1)
        len_n = glm.length(n)
        if len_n < 1E-6:
            continue
        n /= len_n

        weight = angle_of(v0, v1)
        weight_sum += weight
        normal += weight * n

    return glm.normalize(normal)

def is_even(num:int):
    return num % 2 == 0

def is_odd(num:int):
    return num % 2 != 0

@cache.memoize()
def factorial(n:int):
    return np.math.factorial(n)

@cache.memoize()
def Zernike_coeff(n:int, m:int, k:int):
    sgn = 1 if is_even(k) else -1
    C = factorial(n - k) / (factorial(k) * factorial((n+m)//2 - k) * factorial((n-m)//2 - k))
    return sgn * C

@cache.memoize()
def Zernike_eval(n:int, m:int, theta:float, r:float):
    use_cos = (m >= 0)
    m = abs(m)

    if n < 0 or is_odd(n - m):
        return 0
    
    R = 0
    ub = (n - m) // 2
    for k in range(ub+1):
        R += Zernike_coeff(n, m, k) * r**(n-2*k)

    if use_cos:
        return R * math.cos(m*theta)
    else:
        return R * math.sin(m*theta)

@cache.memoize()
def associated_Legendre_coeff(n:int, m:int, k:int):
    sgn = 1 if is_even(k) else -1
    C = factorial(2*(n - k)) / (2**n * factorial(k) * factorial(n-k) * factorial(n - 2*k - m))
    return sgn * C

@cache.memoize()
def associated_Legendre_eval(n:int, m:int, x:float):
    if n < 0 or n < abs(m):
        return 0

    if m < 0:
        m = abs(m)
        sgn = 1 if is_even(m) else -1
        C = factorial(n - m) / factorial(n + m)
        return sgn * C * associated_Legendre_eval(n, m, x)

    P = 0
    ub = int((n - m)/2)
    for k in range(ub + 1):
        P += associated_Legendre_coeff(n, m, k) * x**(n - 2*k - m)

    P *= (1 - x**2)**(m/2)
    return P

@cache.memoize()
def spherical_harmonics_coeff(n:int, m:int):
    sgn = 1 if is_even(m) else -1
    return sgn * math.sqrt((2*n+1)/(4*math.pi) * factorial(n-m)/factorial(n+m))

@cache.memoize()
def spherical_harmonics_eval(n:int, m:int, theta:float, phi:float):
    A = spherical_harmonics_coeff(n, m)
    P = associated_Legendre_eval(n, m, math.cos(theta))
    return A * P * complex(math.cos(m*phi), math.sin(m*phi))
    