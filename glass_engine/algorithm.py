import glm
import math
import copy
import numpy as np
from glass.AttrList import AttrList


def fzero(f, interval):
    lower = interval[0]
    upper = interval[1]
    f_lower = f(lower)

    f_upper = None
    if math.isinf(upper):
        d = 1
        upper = lower + d
        f_upper = f(upper)
        times = 0
        while np.sign(f_lower) == np.sign(f_upper):
            d *= 2
            upper = lower + d
            f_upper = f(upper)
            times += 1
            if times > 20:
                return None
    else:
        f_upper = f(upper)

    if np.sign(f_lower) == np.sign(f_upper):
        return None

    while upper - lower > 1e-6:
        middle = (lower + upper) / 2
        f_middle = f(middle)
        if np.sign(f_middle) == np.sign(f_lower):
            f_lower = f_middle
            lower = middle
        else:
            f_upper = f_middle
            upper = middle

    return (lower + upper) / 2


def angle_of(v1, v2):
    len_v1 = math.sqrt(v1[0] ** 2 + v1[1] ** 2 + v1[2] ** 2)
    len_v2 = math.sqrt(v2[0] ** 2 + v2[1] ** 2 + v2[2] ** 2)
    if len_v1 < 1e-6 or len_v2 < 1e-6:
        return 0

    cos_theta = (v1[0] * v2[0] + v1[1] * v2[1] + v1[2] * v2[2]) / (len_v1 * len_v2)
    if cos_theta < -1:
        cos_theta = -1
    if cos_theta > 1:
        cos_theta = 1

    return math.acos(cos_theta)


def cos_angle_of(v1, v2):
    len_v1 = glm.length(v1)
    len_v2 = glm.length(v2)
    if len_v1 < 1e-6 or len_v2 < 1e-6:
        return 0

    cos_theta = glm.dot(v1, v2) / (len_v1 * len_v2)
    if cos_theta < -1:
        cos_theta = -1
    if cos_theta > 1:
        cos_theta = 1

    return cos_theta


def approx_pos(pos, precision: int = 7):
    return glm.vec3(
        round(pos.x, precision), round(pos.y, precision), round(pos.z, precision)
    )


def hash_pos(pos):
    negtive_zero = "-0.0000000"
    zero = "0.0000000"

    x_str = f"{pos[0]:.7f}"
    if x_str == negtive_zero:
        x_str = zero

    y_str = f"{pos[1]:.7f}"
    if y_str == negtive_zero:
        y_str = zero

    z_str = f"{pos[2]:.7f}"
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

    return not points_map


def normalize(arr):
    if len(arr.shape) == 2:
        lens = np.sqrt(arr[:, 0] ** 2 + arr[:, 1] ** 2 + arr[:, 2] ** 2)
        good_lens_it = lens > 1e-6

        normalized_arr = arr[:]
        normalized_arr[:, 0][good_lens_it] /= lens[good_lens_it]
        normalized_arr[:, 1][good_lens_it] /= lens[good_lens_it]
        normalized_arr[:, 2][good_lens_it] /= lens[good_lens_it]
        return normalized_arr
    else:
        len_arr = np.linalg.norm(arr)
        if len_arr > 1e-6:
            return arr / len_arr
        else:
            return arr[:]


def generate_TBN(vertices, indices):
    position_view = vertices["position"].ndarray[indices.ndarray.flat, :]
    position0_view = position_view[0::3, :]
    position1_view = position_view[1::3, :]
    position2_view = position_view[2::3, :]

    tex_coord_view = vertices["tex_coord"].ndarray[indices.ndarray.flat, :]
    tex_coord0_view = tex_coord_view[0::3, :]
    tex_coord1_view = tex_coord_view[1::3, :]
    tex_coord2_view = tex_coord_view[2::3, :]

    v01 = position1_view - position0_view
    v02 = position2_view - position0_view

    st01 = tex_coord1_view - tex_coord0_view
    st02 = tex_coord2_view - tex_coord0_view

    det = st01[:, 0] * st02[:, 1] - st02[:, 0] * st01[:, 0]
    good_det_id = abs(det) > 1e-6
    det = det.reshape(st01.shape[0], 1)

    normal = normalize(np.cross(v01, v02))
    tangent = (
        st02[:, 1].reshape(v01.shape[0], 1) * v01
        - st01[:, 1].reshape(v01.shape[0], 1) * v02
    )
    bitangent = (
        st01[:, 0].reshape(v01.shape[0], 1) * v02
        - st02[:, 0].reshape(v01.shape[0], 1) * v01
    )

    tangent[good_det_id, :] /= det[good_det_id, :]
    bitangent[good_det_id, :] /= det[good_det_id, :]

    return tangent, bitangent, normal


def generate_auto_TBN(vertices, indices, calculate_normal=True):
    if "tangent" not in vertices._attr_list_map:
        vertices._attr_list_map["tangent"] = AttrList(dtype=glm.vec3)

    if "bitangent" not in vertices._attr_list_map:
        vertices._attr_list_map["bitangent"] = AttrList(dtype=glm.vec3)

    if "normal" not in vertices._attr_list_map:
        vertices._attr_list_map["normal"] = AttrList(dtype=glm.vec3)

    points_list = []
    for i in range(vertices["position"].ndarray.shape[0]):
        points_list.append(
            {
                "tangent": np.array([0, 0, 0], dtype=np.float32),
                "bitangent": np.array([0, 0, 0], dtype=np.float32),
                "normal": np.array([0, 0, 0], dtype=np.float32),
                "num": 0,
                "index": set(),
            }
        )

    tangent, bitangent, normal = generate_TBN(vertices, indices)

    for i in range(len(indices.ndarray.flat)):
        index = indices.ndarray.flat[i]
        info = points_list[index]
        info["num"] += 1
        info["tangent"] += tangent[i // 3, :]
        info["bitangent"] += bitangent[i // 3, :]
        info["normal"] += normal[i // 3, :]
        info["index"].add(index)

    for info in points_list:
        if info["num"] == 0:
            continue

        info["tangent"] = info["tangent"] / info["num"]
        info["bitangent"] = info["bitangent"] / info["num"]
        len_normal = np.linalg.norm(info["normal"])
        if len_normal > 1e-6:
            info["normal"] = info["normal"] / len_normal

        for index in info["index"]:
            vertices["tangent"].ndarray[index, :] = info["tangent"]
            vertices["bitangent"].ndarray[index, :] = info["bitangent"]
            if calculate_normal:
                vertices["normal"].ndarray[index, :] = info["normal"]


def generate_smooth_TBN(vertices, indices, calculate_normal=True):
    if "tangent" not in vertices._attr_list_map:
        vertices._attr_list_map["tangent"] = AttrList(dtype=glm.vec3)

    if "bitangent" not in vertices._attr_list_map:
        vertices._attr_list_map["bitangent"] = AttrList(dtype=glm.vec3)

    if "normal" not in vertices._attr_list_map:
        vertices._attr_list_map["normal"] = AttrList(dtype=glm.vec3)

    points_map = {}
    pos_keys = []
    for i in range(vertices["position"].ndarray.shape[0]):
        pos = vertices["position"].ndarray[i]
        pos_key = hash_pos(pos)
        pos_keys.append(pos_key)
        if pos_key not in points_map:
            points_map[pos_key] = {
                "tangent": np.array([0, 0, 0], dtype=np.float32),
                "bitangent": np.array([0, 0, 0], dtype=np.float32),
                "normal": np.array([0, 0, 0], dtype=np.float32),
                "num": 0,
                "index": set(),
            }

    tangent, bitangent, normal = generate_TBN(vertices, indices)

    for i in range(len(indices.ndarray.flat)):
        index = indices.ndarray.flat[i]
        pos_key = pos_keys[index]
        info = points_map[pos_key]
        info["num"] += 1
        info["tangent"] += tangent[i // 3, :]
        info["bitangent"] += bitangent[i // 3, :]
        info["normal"] += normal[i // 3, :]
        info["index"].add(index)

    for info in points_map.values():
        if info["num"] == 0:
            continue

        info["tangent"] = info["tangent"] / info["num"]
        info["bitangent"] = info["bitangent"] / info["num"]
        len_normal = np.linalg.norm(info["normal"])
        if len_normal > 1e-6:
            info["normal"] = info["normal"] / len_normal

        for index in info["index"]:
            vertices["tangent"].ndarray[index, :] = info["tangent"]
            vertices["bitangent"].ndarray[index, :] = info["bitangent"]
            if calculate_normal:
                vertices["normal"].ndarray[index, :] = info["normal"]


def line_intersect_plane(
    line_start: glm.vec3,
    line_direction: glm.vec3,
    plane_start: glm.vec3,
    plane_normal: glm.vec3,
):
    A = plane_start
    B = line_start
    d = line_direction
    n = plane_normal
    AB = B - A

    return B - glm.dot(AB, n) / glm.dot(d, n) * d


def point_distance_to_line(
    point: glm.vec3, line_start: glm.vec3, line_direction: glm.vec3
):
    A = line_start
    d = line_direction
    B = point

    AB = B - A
    return glm.length(glm.cross(AB, d))


def point_mirror_by_plane(
    point: glm.vec3, plane_start: glm.vec3, plane_normal: glm.vec3
):
    d = plane_start - point
    return point + 2 * glm.dot(d, plane_normal) * plane_normal


def polygon_centroid(polygon):
    polygon = copy.copy(polygon)

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
    for i in range(1, len_polygon + 1):
        point0 = polygon[i - 1]
        point1 = polygon[i] if i < len_polygon else polygon[0]
        center = (O + point0 + point1) / 3
        weight = glm.length(glm.cross(point0 - O, point1 - O)) / 2
        weight_sum += weight
        if centroid is None:
            centroid = weight * center
        else:
            centroid += weight * center

    return centroid / weight_sum


def polygon_normal(polygon, centroid=None):
    if centroid is None:
        centroid = polygon_centroid(polygon)

    normal = glm.vec3(0)
    weight_sum = 0
    len_polygon = len(polygon)
    for i in range(1, len_polygon + 1):
        point0 = polygon[i - 1]
        point1 = polygon[i] if i < len_polygon else polygon[0]

        v0 = point0 - centroid
        v1 = point1 - centroid

        n = glm.cross(v0, v1)
        len_n = glm.length(n)
        if len_n < 1e-6:
            continue
        n /= len_n

        weight = angle_of(v0, v1)
        weight_sum += weight
        normal += weight * n

    return glm.normalize(normal)


def is_even(num: int):
    return num % 2 == 0


def is_odd(num: int):
    return num % 2 != 0


def factorial(n: int):
    return np.math.factorial(n)


def Zernike_coeff(n: int, m: int, k: int):
    sgn = 1 if is_even(k) else -1
    C = factorial(n - k) / (
        factorial(k) * factorial((n + m) // 2 - k) * factorial((n - m) // 2 - k)
    )
    return sgn * C


def Zernike_eval(n: int, m: int, r: float, theta: float):
    use_cos = m >= 0
    m = abs(m)

    if n < 0 or is_odd(n - m):
        return 0

    R = 0
    ub = (n - m) // 2
    for k in range(ub + 1):
        R += Zernike_coeff(n, m, k) * r ** (n - 2 * k)

    if use_cos:
        return R * np.cos(m * theta)
    else:
        return R * np.sin(m * theta)


def associated_Legendre_coeff(l: int, m: int, k: int):
    sgn = 1 if is_even(k) else -1
    C = factorial(2 * (l - k)) / (
        2**l * factorial(k) * factorial(l - k) * factorial(l - 2 * k - m)
    )
    return sgn * C


def associated_Legendre_eval(l: int, m: int, x: float):
    if l < 0 or l < abs(m):
        return 0

    if m < 0:
        m = abs(m)
        sgn = 1 if is_even(m) else -1
        C = factorial(l - m) / factorial(l + m)
        return sgn * C * associated_Legendre_eval(l, m, x)

    P = 0
    ub = (l - m) // 2
    for k in range(ub + 1):
        P += associated_Legendre_coeff(l, m, k) * x ** (l - 2 * k - m)

    P *= (1 - x**2) ** (m / 2)
    return P


def spherical_harmonics_coeff(l: int, m: int):
    sgn = 1 if is_even(m) else -1
    return sgn * math.sqrt(
        (2 * l + 1) / (4 * math.pi) * factorial(l - m) / factorial(l + m)
    )


def spherical_harmonics_eval(l: int, m: int, theta: float, phi: float):
    A = spherical_harmonics_coeff(l, m)
    P = associated_Legendre_eval(l, m, np.cos(theta))
    return A * P * np.exp(m * phi * 1j)
