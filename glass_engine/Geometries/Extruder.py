from ..Mesh import Mesh
from ..algorithm import line_intersect_plane, \
    point_mirror_by_plane, polygon_centroid, polygon_normal, cos_angle_of

from glass import Vertex

import glm
import math
from enum import Enum
import copy

class Extruder(Mesh):

    class JoinStyle(Enum):
        MiterJoin = 0
        RoundJoin = 1
        BevelJoin = 2

    def __init__(self, section, path, join_style:JoinStyle=JoinStyle.MiterJoin,
                 color:(glm.vec3,glm.vec4)=glm.vec4(0.396, 0.74151, 0.69102, 1), back_color:(glm.vec3,glm.vec4)=None,
                 n_corner_divide:int=100,
                 normalize_tex_coord:bool=False,
                 name:str="", block:bool=True, surf_type:Mesh.SurfType=Mesh.SurfType.Auto):
        Mesh.__init__(self, color=color, back_color=back_color, name=name, block=block, surf_type=surf_type)
        self.__section = section
        self.__path = path
        self.__join_style = join_style
        self.__n_corner_divide = n_corner_divide
        self.__normalize_tex_coord = normalize_tex_coord
        self.start_building()

    def build(self):
        section = self.__section
        path = copy.copy(self.__path)
        i = 1

        len_path = len(path)
        while i < len_path:
            while glm.length(path[i]-path[i-1]) < 1E-6:
                del path[i]
                len_path -= 1

            i += 1

        if len_path < 2:
            self.vertices.clear()
            self.indices.clear()
            return
        
        centroid = polygon_centroid(section)
        normal = -polygon_normal(section, centroid=centroid)
        section = self.__used_section

        dem = math.sqrt(normal.x**2 + normal.y**2)
        current_yaw = 0
        current_pitch = math.pi/2 if normal.z > 0 else -math.pi/2
        if dem > 1E-6:
            current_pitch = math.atan(normal.z/dem)
            current_yaw = -math.atan2(normal.x, normal.y)

        d2 = path[1] - path[0]
        dem = math.sqrt(d2.x**2 + d2.y**2)
        dest_yaw = 0
        dest_pitch = math.pi/2 if d2.z > 0 else -math.pi/2
        if dem > 1E-6:
            dest_pitch = math.atan(d2.z/dem)
            dest_yaw = -math.atan2(d2.x, d2.y)
        
        delta_yaw = dest_yaw - current_yaw
        delta_pitch = dest_pitch - current_pitch

        quat1 = glm.quat(math.cos(delta_yaw/2), 0, 0, math.sin(delta_yaw/2))
        quat2 = glm.quat(math.cos(delta_pitch/2), math.sin(delta_pitch/2), 0, 0)
        quat = quat1 * quat2

        section_offset = []
        current_section = []
        accumulate_length = [0]
        for j in range(len(section)):
            current_section.append(quat * (section[j]-centroid) + path[0])
            section_offset.append(glm.dot(section[j]-centroid, normal))
            if j > 0:
                accumulate_length.append(accumulate_length[-1] + glm.length(section[j] - section[j-1]))

        if self.__join_style == Extruder.JoinStyle.MiterJoin:
            yield from self.miter_join_build(current_section, accumulate_length, section_offset, path)
        elif self.__join_style == Extruder.JoinStyle.RoundJoin:
            yield from self.round_join_build(current_section, accumulate_length, section_offset, path)
        elif self.__join_style == Extruder.JoinStyle.BevelJoin:
            yield from self.bevel_join_build(current_section, accumulate_length, section_offset, path)

    def bevel_join_build(self, current_section, accumulate_length, section_offset, path):
        vertices = self.vertices
        indices = self.indices
        normalize_tex_coord = self.__normalize_tex_coord
        len_section = len(current_section)

        i_vertex = 0
        i_index = 0

        L = 0
        longest_distance = None
        next_section = []
        span_distances = []
        center_length = []
        d1, d2 = None, None
        len_path = len(path)
        for i in range(len_path):
            should_add_corner = True
            if i == 0:
                d1 = glm.normalize(path[i+1] - path[i])
                should_add_corner = False
            else:
                d1 = path[i] - path[i-1]
                len_d1 = glm.length(d1)
                d1 = d1 / len_d1

                L += len_d1
                if i < len_path-1:
                    d2 = glm.normalize(path[i+1] - path[i])
                    cos_theta = glm.dot(d1, d2)
                    if cos_theta > 0.9:
                        should_add_corner = False

                    half_way = glm.normalize(-d1 + d2)
                    plane_normal = None
                    if glm.length(-d1 + d2) < 1E-6:
                        plane_normal = glm.normalize(d1 + d2)
                    else:
                        up = glm.normalize(glm.cross(d1, d2))
                        plane_normal = glm.normalize(glm.cross(half_way, up))

                    section_on_bisection = []
                    for j in range(len_section):
                        point_on_bisection = line_intersect_plane(current_section[j], d1, path[i], plane_normal)
                        section_on_bisection.append(point_on_bisection)

                    if should_add_corner:
                        next_section = []
                        span_distances = []
                        center_length = [0]
                        last_center = None
                        longest_distance = -float("inf")
                        for j in range(len_section):
                            point_on_pendicular = line_intersect_plane(current_section[j], d1, path[i], d1)
                            point_on_bisection = section_on_bisection[j]

                            bisection_point_projection = glm.dot((point_on_bisection - path[i]), d1)
                            pendicular_point_projection = glm.dot((point_on_pendicular - path[i]), d1)

                            current_center = None
                            if bisection_point_projection < pendicular_point_projection:
                                current_section[j] = point_on_bisection
                                next_section.append(point_on_bisection)
                                span_distances.append(0)
                                current_center = point_on_bisection
                            else:
                                current_section[j] = point_on_pendicular
                                next_point = point_mirror_by_plane(point_on_pendicular, path[i], plane_normal)
                                next_section.append(next_point)
                                current_distance = glm.length(next_point - current_section[j])
                                span_distances.append(current_distance)
                                if current_distance > longest_distance:
                                    longest_distance = current_distance
                                current_center = 0.5*(next_point + current_section[j])
                            if j > 0:
                                center_length.append(center_length[-1] + glm.length(current_center - last_center))

                            last_center = current_center
                    else:
                        for j in range(len_section):
                            current_section[j] = section_on_bisection[j]
                else:
                    should_add_corner = False
                    for j in range(len_section):
                        current_section[j] = line_intersect_plane(current_section[j], d1, path[i], d1) + section_offset[j]*d1

            for j in range(len_section):
                t = accumulate_length[j]
                s = L + glm.dot(current_section[j] - path[i], d1)
                if normalize_tex_coord:
                    s /= accumulate_length[-1]
                    t /= accumulate_length[-1]

                vertex = Vertex()
                vertex.position = current_section[j]
                vertex.tex_coord = glm.vec3(s, t, 0)
                vertices[i_vertex] = vertex
                i_vertex += 1

                if j > 0 and i > 0:
                    triangle = glm.uvec3(0, 0, 0)
                    triangle[0] = i_vertex - 1
                    triangle[1] = i_vertex - 2 - len_section
                    triangle[2] = i_vertex - 2
                    indices[i_index] = triangle
                    i_index += 1
                    self.generate_temp_TBN(vertices[triangle[0]], vertices[triangle[1]], vertices[triangle[2]])

                    triangle = glm.uvec3(0, 0, 0)
                    triangle[0] = i_vertex - 1
                    triangle[1] = i_vertex - 1 - len_section
                    triangle[2] = i_vertex - 2 - len_section
                    indices[i_index] = triangle
                    i_index += 1
                    self.generate_temp_TBN(vertices[triangle[0]], vertices[triangle[1]], vertices[triangle[2]])

                    yield

            if should_add_corner:
                for j in range(len_section):
                    s = L-span_distances[j]/2
                    t = center_length[j]
                    if normalize_tex_coord:
                        s /= center_length[-1]
                        t /= center_length[-1]

                    vertex = Vertex()
                    vertex.position = current_section[j]
                    vertex.tex_coord = glm.vec3(s, t, 0)
                    vertices[i_vertex] = vertex
                    i_vertex += 1

                for j in range(len_section):
                    s = L+span_distances[j]/2
                    t = center_length[j]
                    if normalize_tex_coord:
                        s /= center_length[-1]
                        t /= center_length[-1]

                    vertex = Vertex()
                    vertex.position = next_section[j]
                    vertex.tex_coord = glm.vec3(s, t, 0)
                    vertices[i_vertex] = vertex
                    i_vertex += 1

                    if j > 0 and i > 0:
                        triangle = glm.uvec3(0, 0, 0)
                        triangle[0] = i_vertex - 1
                        triangle[1] = i_vertex - 2 - len_section
                        triangle[2] = i_vertex - 2
                        indices[i_index] = triangle
                        i_index += 1
                        self.generate_temp_TBN(vertices[triangle[0]], vertices[triangle[1]], vertices[triangle[2]])

                        triangle = glm.uvec3(0, 0, 0)
                        triangle[0] = i_vertex - 1
                        triangle[1] = i_vertex - 1 - len_section
                        triangle[2] = i_vertex - 2 - len_section
                        indices[i_index] = triangle
                        i_index += 1
                        self.generate_temp_TBN(vertices[triangle[0]], vertices[triangle[1]], vertices[triangle[2]])
                    
                        yield

                for j in range(len_section):
                    s = L + glm.dot(next_section[j] - path[i], d2)
                    t = accumulate_length[j]
                    if normalize_tex_coord:
                        s /= accumulate_length[-1]
                        t /= accumulate_length[-1]

                    vertex = Vertex()
                    vertex.position = next_section[j]
                    vertex.tex_coord = glm.vec3(s, t, 0)
                    vertices[i_vertex] = vertex
                    i_vertex += 1

                current_section = section_on_bisection

        del vertices[i_vertex:]
        del indices[i_index:]
            
    def round_join_build(self, current_section, accumulate_length, section_offset, path):
        vertices = self.vertices
        indices = self.indices
        n_corner_divide = self.__n_corner_divide
        normalize_tex_coord = self.__normalize_tex_coord
        len_section = len(current_section)

        i_vertex = 0
        i_index = 0

        L = 0
        up = None
        first_hit_point = None
        distance_first_hit_to_corner = None
        theta = None
        backup_section = None
        last_should_add_corner = False
        len_path = len(path)
        for i in range(len_path):
            should_add_corner = True
            if i == 0:
                d1 = glm.normalize(path[i+1] - path[i])
                should_add_corner = False
            else:
                d1 = path[i] - path[i-1]
                len_d1 = glm.length(d1)
                d1 = d1 / len_d1
                
                if last_should_add_corner:
                    len_d1 -= distance_first_hit_to_corner*math.sin(theta/2)

                L += len_d1
                if i < len_path-1:
                    d2 = glm.normalize(path[i+1] - path[i])
                    cos_theta = glm.dot(d1, d2)
                    if cos_theta > 0.9:
                        should_add_corner = False
                    else:
                        theta = math.acos(cos_theta)

                    half_way = glm.normalize(-d1 + d2)
                    plane_normal = None
                    if glm.length(-d1 + d2) < 1E-6:
                        plane_normal = glm.normalize(d1 + d2)
                    else:
                        up = glm.normalize(glm.cross(d1, d2))
                        plane_normal = glm.normalize(glm.cross(half_way, up))

                    backup_section = []
                    for j in range(len_section):
                        backup_section.append(line_intersect_plane(current_section[j], d1, path[i], plane_normal))

                    if should_add_corner:
                        min_length = float("inf")
                        first_hit_point = None
                        for j in range(len_section):
                            current_point = backup_section[j]
                            current_length = glm.dot(current_point - path[i], d1)
                            if current_length < min_length:
                                min_length = current_length
                                first_hit_point = current_point
                        distance_first_hit_to_corner = glm.length(first_hit_point - path[i])
                        
                        for j in range(len_section):
                            current_section[j] = line_intersect_plane(current_section[j], d1, first_hit_point, d1)
                    
                    else:
                        for j in range(len_section):
                            current_section[j] = backup_section[j]
                else:
                    should_add_corner = False

                    for j in range(len_section):
                        current_section[j] = line_intersect_plane(current_section[j], d1, path[i], d1) + section_offset[j]*d1

            quat = None

            if should_add_corner:
                L -= distance_first_hit_to_corner*math.sin(theta/2)
                max_k = min(n_corner_divide, int(theta/0.05))
                for k in range(max_k):
                    current_theta = theta * k / (max_k - 1)
                    quat = glm.quat(math.cos(current_theta/2), math.sin(current_theta/2)*up)

                    H = first_hit_point - glm.dot(first_hit_point, up) * up # 原点到轴的垂足

                    for j in range(len_section):
                        point = current_section[j]
                        pos = quat * (point - H) + H

                        s = L + distance_first_hit_to_corner*current_theta
                        t = accumulate_length[j]
                        if normalize_tex_coord:
                            s /= accumulate_length[-1]
                            t /= accumulate_length[-1]

                        vertex = Vertex()
                        vertex.position = pos
                        vertex.tex_coord = glm.vec3(s, t, 0)

                        vertices[i_vertex] = vertex
                        i_vertex += 1

                        if i > 0 and j > 0:
                            triangle = glm.uvec3(0, 0, 0)
                            triangle[0] = i_vertex - 1
                            triangle[1] = i_vertex - 2 - len_section
                            triangle[2] = i_vertex - 2
                            indices[i_index] = triangle
                            i_index += 1
                            self.generate_temp_TBN(vertices[triangle[0]], vertices[triangle[1]], vertices[triangle[2]])

                            triangle = glm.uvec3(0, 0, 0)
                            triangle[0] = i_vertex - 1
                            triangle[1] = i_vertex - 1 - len_section
                            triangle[2] = i_vertex - 2 - len_section
                            indices[i_index] = triangle
                            i_index += 1
                            self.generate_temp_TBN(vertices[triangle[0]], vertices[triangle[1]], vertices[triangle[2]])
                    
                            yield

                current_section = backup_section
                L += distance_first_hit_to_corner*theta
            else:
                for j in range(len_section):
                    t = accumulate_length[j]
                    s = L + glm.dot(current_section[j]-path[i], d1)                    
                    if normalize_tex_coord:
                        t /= accumulate_length[-1]
                        s /= accumulate_length[-1]
                    
                    vertex = Vertex()
                    vertex.position = current_section[j]
                    vertex.tex_coord = glm.vec3(s, t, 0)
                    vertices[i_vertex] = vertex
                    i_vertex += 1

                    if i > 0 and j > 0:
                        triangle = glm.uvec3(0, 0, 0)
                        triangle[0] = i_vertex-1
                        triangle[1] = i_vertex-2-len_section
                        triangle[2] = i_vertex-2
                        indices[i_index] = triangle
                        i_index += 1
                        self.generate_temp_TBN(vertices[triangle[0]], vertices[triangle[1]], vertices[triangle[2]])

                        triangle = glm.uvec3(0, 0, 0)
                        triangle[0] = i_vertex-1
                        triangle[1] = i_vertex-1-len_section
                        triangle[2] = i_vertex-2-len_section
                        indices[i_index] = triangle
                        i_index += 1
                        self.generate_temp_TBN(vertices[triangle[0]], vertices[triangle[1]], vertices[triangle[2]])

                        yield

            last_should_add_corner = should_add_corner

        del vertices[i_vertex:]
        del indices[i_index:]

    def miter_join_build(self, current_section, accumulate_length, section_offset, path):
        vertices = self.vertices
        indices = self.indices
        normalize_tex_coord = self.__normalize_tex_coord
        len_section = len(current_section)

        i_vertex = 0
        i_index = 0

        L = 0
        d1, d2 = None, None
        len_path = len(path)
        for i in range(len_path):
            should_add_corner = True
            if i == 0:
                d1 = glm.normalize(path[i+1]-path[i])
                should_add_corner = False
            else:
                d1 = path[i] - path[i-1]
                len_d1 = glm.length(d1)
                L += len_d1
                d1 /= len_d1
                
                if i < len_path-1:
                    d2 = glm.normalize(path[i+1] - path[i])
                    half_way = glm.normalize(-d1 + d2)
                    up = glm.normalize(glm.cross(d1, d2))
                    cos_theta = glm.dot(d1, d2)

                    plane_normal = d1
                    if cos_theta > 0.9:
                        should_add_corner = False
                    else:
                        plane_normal = glm.normalize(glm.cross(half_way, up))

                    for j in range(len_section):
                        current_section[j] = line_intersect_plane(current_section[j], d1, path[i], plane_normal)
                else:
                    should_add_corner = False
                    for j in range(len_section):
                        current_section[j] = line_intersect_plane(current_section[j], d1, path[i], d1) + section_offset[j]*d1

            for j in range(len_section):
                t = accumulate_length[j]
                s = L + glm.dot(current_section[j] - path[i], d1)

                if normalize_tex_coord:
                    t /= accumulate_length[-1]
                    s /= accumulate_length[-1]

                vertex = Vertex()
                vertex.position = current_section[j]
                vertex.tex_coord = glm.vec3(s, t, 0)
                vertices[i_vertex] = vertex
                i_vertex += 1

                if i > 0 and j > 0:
                    triangle = glm.uvec3(0, 0, 0)
                    triangle[0] = i_vertex - 1
                    triangle[1] = i_vertex - 2 - len_section
                    triangle[2] = i_vertex - 2
                    indices[i_index] = triangle
                    i_index += 1
                    self.generate_temp_TBN(vertices[triangle[0]], vertices[triangle[1]], vertices[triangle[2]])

                    triangle = glm.uvec3(0, 0, 0)
                    triangle[0] = i_vertex - 1
                    triangle[1] = i_vertex - 1 - len_section
                    triangle[2] = i_vertex - 2 - len_section
                    indices[i_index] = triangle
                    i_index += 1
                    self.generate_temp_TBN(vertices[triangle[0]], vertices[triangle[1]], vertices[triangle[2]])

                    yield

            if should_add_corner:
                for j in range(len_section):
                    t = accumulate_length[j]
                    s = L - glm.dot(current_section[j] - path[i], d1)
                    if normalize_tex_coord:
                        t /= accumulate_length[-1]
                        s /= accumulate_length[-1]

                    vertex = Vertex()
                    vertex.position = current_section[j]
                    vertex.tex_coord = glm.vec3(s, t, 0)
                    vertices[i_vertex] = vertex
                    i_vertex += 1

        del vertices[i_vertex:]
        del indices[i_index:]

    @property
    def section(self):
        return self.__section
    
    @section.setter
    def section(self, section):
        self.__section = section
        self.start_building()

    @property
    def __used_section(self):
        should_duplicate_indices = set()
        for i in range(1, len(self.__section)-1):
            v1 = self.__section[i-1] - self.__section[i]
            v2 = self.__section[i+1] - self.__section[i]
            cos_angle = cos_angle_of(v1, v2)
            if cos_angle > -0.9:
                should_duplicate_indices.add(i)

        used_section = []
        for i in range(len(self.__section)):
            used_section.append(self.__section[i])
            if i in should_duplicate_indices:
                used_section.append(self.__section[i])

        return used_section

    @property
    def path(self):
        return self.__path
    
    @path.setter
    def path(self, path):
        self.__path = path
        self.start_building()

    @property
    def join_style(self):
        return self.__join_style
    
    @join_style.setter
    @Mesh.param_setter
    def join_style(self, join_style:JoinStyle):
        self.__join_style = join_style

    @property
    def n_corner_divide(self):
        return self.__n_corner_divide
    
    @n_corner_divide.setter
    @Mesh.param_setter
    def n_corner_divide(self, n:int):
        self.__n_corner_divide = n

    @property
    def normalize_tex_coord(self):
        return self.__normalize_tex_coord

    @normalize_tex_coord.setter
    @Mesh.param_setter
    def normalize_tex_coord(self, flag:bool):
        self.__normalize_tex_coord = flag