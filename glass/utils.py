from functools import wraps
import ctypes
import re
import math
import glm
import os
import types
import cProfile
import hashlib
import pickle
import subprocess
import sys
import chardet
from _ctypes import PyObj_FromPtr

from .GlassConfig import GlassConfig
from typeguard import typechecked

profiler = cProfile.Profile()


def run_exe(exe_path, *args):
    cmd = [exe_path, *args]
    result = subprocess.run(cmd, capture_output=True, text=True)
    stdout = result.stdout.strip()
    stderr = result.stderr.strip()
    return stdout, stderr


def cat(file_name):
    in_file = open(file_name, "r", encoding=sys.getdefaultencoding(), errors="ignore")
    content = in_file.read()
    in_file.close()
    return content


def bincat(file_name):
    in_file = open(file_name, "rb")
    content = in_file.read()
    in_file.close()
    return content


def uint64_to_uvec2(uint64_value):
    result = glm.uvec2()
    bytes_data = uint64_value.to_bytes(8, byteorder="little", signed=False)
    result.x = int.from_bytes(bytes_data[:4], byteorder="little", signed=False)
    result.y = int.from_bytes(bytes_data[4:], byteorder="little", signed=False)
    return result


def same_type(var1, var2):
    return isinstance(var1, type(var2)) and isinstance(var2, type(var1))

def checktype(func):
    if not GlassConfig.debug:
        return func
    
    try:
        func._typechecked_func = typechecked(func)
    except:
        pass

    @wraps(func)
    def wrapper(*args, **kwargs):
        if not GlassConfig.debug:
            return func(*args, **kwargs)

        try:
            typechecked_func = func._typechecked_func
        except:
            typechecked_func = typechecked(func)

        return typechecked_func(*args, **kwargs)

    return wrapper


def is_overridden(method):
    cls = method.__self__.__class__
    mro = cls.__mro__
    code = method.__code__
    method_name = method.__name__
    for i, base_cls in enumerate(mro):
        if method_name in base_cls.__dict__:
            base_method = base_cls.__dict__[method_name]
            if (
                isinstance(base_method, types.FunctionType)
                and base_method.__code__ is not code
            ):
                return True
    return False


def delete(method):
    @wraps(method)
    def wrapper(*args, **kwargs):
        self = args[0]
        raise AttributeError(
            f"'{self.__class__.__name__}' object has no attribute '{method.__name__}'"
        )

    return wrapper


def extname(filename):
    return os.path.splitext(filename)[1][1:].lower()


def has_valid(content):
    its = list(re.finditer(r"\S", content))
    return bool(its)


def array_basename(name: str):
    pos_bracket = name.find("[")
    if pos_bracket == -1:
        return name
    else:
        return name[:pos_bracket].strip(" \t")


def extract_array_indices(var_name: str):
    if "[" not in var_name:
        return []

    indices = []
    len_var_name = len(var_name)
    pos_start = len_var_name
    while True:
        pos_end = var_name.rfind("]", 0, pos_start)
        if pos_end == -1:
            break

        str_mid = var_name[pos_end + 1 : pos_start]
        if (
            pos_end >= 0
            and pos_end < len_var_name
            and pos_start >= 0
            and pos_start < len_var_name
            and has_valid(str_mid)
        ):
            break

        pos_start = var_name.rfind("[", 0, pos_end)
        if pos_start == -1:
            break

        index = "{0}"
        if pos_end - pos_start > 1:
            index = int(var_name[pos_start + 1 : pos_end].strip(" \t"))

        indices.insert(0, index)

    return indices


def next_index(current_index, indices):
    if not current_index:
        for index in indices:
            if isinstance(index, int):
                current_index.append(0)
            else:
                current_index.append("{0}")
        return True

    i = len(current_index) - 1
    while True:
        if i < 0:
            return False
        while i >= 0 and isinstance(indices[i], str):
            i -= 1
        if i < 0:
            return False
        current_index[i] += 1
        if current_index[i] >= indices[i]:
            current_index[i] = 0
            i -= 1
        else:
            return True


def resolve_array(var_name):
    if "[" not in var_name:
        return [var_name]

    indices = extract_array_indices(var_name)
    base_name = array_basename(var_name)

    element_names = []
    current_index = []
    while next_index(current_index, indices):
        element_name = base_name
        for index in current_index:
            element_name += "[" + str(index) + "]"
        element_names.append(element_name)

    return element_names


def rget_token(content, i):
    token = {}

    if i < 0 or i >= len(content):
        return "", -1

    i = rskip_space(content, i)
    if i < 0:
        return "", -1

    pos_start = i
    i = rskip_valid(content, i)
    pos_end = i

    token["span"] = (pos_end + 1, pos_start + 1)
    token["word"] = content[pos_end + 1 : pos_start + 1]

    return token, i


def reg_rfind(content, pattern, pos_start, pos_end):
    str_index, comment_index = get_invalid_index(content)

    its = list(re.finditer(pattern, content[pos_start:pos_end]))
    if not its:
        return -1

    for it in reversed(its):
        if it.start() not in str_index and it.start() not in comment_index:
            return it.start()

    return it.start()


def rskip_space(content, i):
    if i < 0 or i >= len(content):
        return -1

    while True:
        if i < 0 or content[i] not in " \t\r.":
            break
        i -= 1

    return i


def rskip_valid(content, i):
    if i < 0 or i >= len(content):
        return -1

    if content[i] in "+-*/%!=<>,":
        i -= 1
        return i

    str_index, comment_index = get_invalid_index(content)
    while i >= 0:
        if i not in str_index and i not in comment_index:
            if content[i] in "\n\t+-*/%!=<>,([{":
                break

            if content[i] in " \t":
                j = rskip_space(content, i)
                if j == -1:
                    break

                if content[j] not in ")]}":
                    break
                else:
                    i = rfind_pair(content, j)

            elif content[i] in ")]}":
                i = rfind_pair(content, i)

        i -= 1

    return i


def find_pair(content, i):
    len_content = len(content)
    if i < 0 or i >= len_content or content[i] not in "([{":
        return -1

    start_pair = content[i]
    end_pair = None
    if content[i] == "(":
        end_pair = ")"
    elif content[i] == "[":
        end_pair = "]"
    elif content[i] == "{":
        end_pair = "}"

    n_start_pair = 0
    str_index, comment_index = get_invalid_index(content)
    while i < len_content:
        if i not in str_index and i not in comment_index:
            if content[i] == start_pair:
                n_start_pair += 1
            elif content[i] == end_pair:
                n_start_pair -= 1

            if n_start_pair == 0:
                break

        i += 1

    return i


def printable_size(content):
    len_content = len(content)
    KB = 1024
    MB = 1024 * KB
    GB = 1024 * MB
    TB = 1024 * GB
    PB = 1024 * TB

    if len_content < KB:
        return f"{len_content}B"
    elif len_content < MB:
        return f"{round(len_content/KB, 2)}KB"
    elif len_content < GB:
        return f"{round(len_content/MB, 2)}MB"
    elif len_content < TB:
        return f"{round(len_content/GB, 2)}GB"
    elif len_content < PB:
        return f"{round(len_content/TB, 2)}TB"
    else:
        return f"{round(len_content/PB, 2)}PB"


def is_text_file(file_path):
    if extname(file_path) in ["exr", "hdr"]:
        return False

    try:
        with open(file_path, "rb") as f:
            result = chardet.detect(f.read(1024))
            return result["encoding"] is not None
    except:
        return False


def is_url(line: str) -> bool:
    pattern = re.compile(
        r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
    )
    return bool(pattern.match(line))


def md5s(content):
    md5_hash = hashlib.md5()
    if isinstance(content, str):
        md5_hash.update(content.encode("utf-8"))
    elif isinstance(content, (bytes, bytearray)):
        md5_hash.update(content)
    else:
        md5_hash.update(pickle.dumps(content))

    return md5_hash.hexdigest()


def modify_time(file_name):
    if not os.path.isfile(file_name):
        return 0

    return os.path.getmtime(file_name)


def relative_path(file_name, start_path="."):
    try:
        return os.path.relpath(file_name, start_path).replace("\\", "/")
    except:
        return os.path.abspath(file_name).replace("\\", "/")


def printable_path(file_name):
    site_packages = os.path.abspath(
        os.path.dirname(os.path.abspath(__file__)) + "/../"
    ).replace("\\", "/")
    name1 = relative_path(file_name, site_packages)
    name2 = relative_path(file_name)
    name3 = os.path.abspath(file_name).replace("\\", "/")

    result = name1 if len(name1) < len(name2) else name2
    result = result if len(result) < len(name3) else name3
    return result


def save_var(var, file_path):
    folder_path = os.path.dirname(os.path.abspath(file_path))
    if not os.path.isdir(folder_path):
        os.makedirs(folder_path)

    with open(file_path, "wb") as file:
        pickle.dump(var, file)


def load_var(file_path):
    with open(file_path, "rb") as file:
        var = pickle.load(file)
    return var


def subscript(var, subscript_chain, feed_index: int = None):
    for operator, operant in subscript_chain:
        if operator == "getattr":
            var = getattr(var, operant)
        else:
            used_index = operant if operant != "{0}" else feed_index
            var = var[used_index]

    return var


def subscript_set(
    var, subscript_chain, value, feed_index: int = None, compare_before_set: bool = True
):
    len_chain = len(subscript_chain)
    last_index = len_chain - 1
    for i in range(len_chain):
        item = subscript_chain[i]
        operator = item[0]
        operant = item[1]

        if operator == "getattr":
            old_value = getattr(var, operant)
            if i != last_index:
                var = old_value
            elif not compare_before_set or old_value != value:
                setattr(var, operant, value)
        else:
            used_index = operant if operant != "{0}" else feed_index
            old_value = var[used_index]
            if i != last_index:
                var = old_value
            elif not compare_before_set or old_value != value:
                var[used_index] = value


def get_subscript_chain(suffix):
    subscript_chain = []
    len_suffix = len(suffix)
    pos_start = 0
    while pos_start < len_suffix:
        start_char = suffix[pos_start]
        if start_char == "." or "a" <= start_char <= "z" or "A" <= start_char <= "Z":
            if start_char == ".":
                pos_start += 1

            pos_point = suffix.find(".", pos_start)
            if pos_point == -1:
                pos_point = len_suffix

            pos_braket = suffix.find("[", pos_start)
            if pos_braket == -1:
                pos_braket = len_suffix

            pos_end = min(pos_point, pos_braket)
            attr_name = suffix[pos_start:pos_end]
            subscript_chain.append(("getattr", attr_name))
            pos_start = pos_end
        elif start_char == "[":
            pos_end = find_pair(suffix, pos_start)
            if pos_end == -1:
                pos_end = len_suffix

            index = int(suffix[pos_start + 1 : pos_end])
            subscript_chain.append(("getitem", index))
            pos_start = pos_end + 1

    return subscript_chain


def rfind_pair(content, i):
    len_content = len(content)
    if i < 0 or i >= len_content or content[i] not in ")]}":
        return -1

    start_pair = content[i]
    end_pair = None
    if content[i] == ")":
        end_pair = "("
    elif content[i] == "]":
        end_pair = "["
    elif content[i] == "}":
        end_pair = "{"

    n_start_pair = 0
    str_index, comment_index = get_invalid_index(content)
    while i < len_content:
        if i not in str_index and i not in comment_index:
            if content[i] == start_pair:
                n_start_pair += 1
            elif content[i] == end_pair:
                n_start_pair -= 1

            if n_start_pair == 0:
                break

        i -= 1

    return i


__str_index_dict = {}
__comment_index_dict = {}


def get_invalid_index(content):
    if content in __str_index_dict:
        return __str_index_dict[content], __comment_index_dict[content]

    str_index = set()
    comment_index = set()
    in_comment = False
    in_str = False
    str_start_char = None
    last_is_slash = False
    i = 0
    len_content = len(content)
    while i < len_content:
        should_add = True
        if content[i] == "'" and not last_is_slash:
            if not in_str:
                should_add = False
                in_str = True
                str_start_char = "'"
            elif str_start_char == "'":
                in_str = False
                str_start_char = None
        elif content[i] == '"' and not last_is_slash:
            if not in_str:
                should_add = False
                in_str = True
                str_start_char = '"'
            elif str_start_char == '"':
                in_str = False
                str_start_char = None
        elif content[i] in "#\\" and not in_str:
            in_comment = True
        elif content[i] == "\n" and in_comment:
            in_comment = False

        if content[i] == "\\" and in_str:
            last_is_slash = not last_is_slash
        else:
            last_is_slash = False

        if should_add:
            if in_str:
                str_index.add(i)
            if in_comment:
                comment_index.add(i)

        i += 1

    __str_index_dict[content] = str_index
    __comment_index_dict[content] = comment_index

    return str_index, comment_index


def delete_python_comments(content):
    i = 0

    str_index, _ = get_invalid_index(content)
    len_content = len(content)

    while i < len_content:
        if i not in str_index:
            if content[i] == "#":
                pos_endl = content.find("\n", i)
                if pos_endl == -1:
                    pos_endl = len_content
                content = content[:i] + content[pos_endl:]
            elif content[i] == "\\":
                pos_endl = content.find("\n", i)
                if pos_endl == -1:
                    pos_endl = len_content
                else:
                    pos_endl += 1

                content = content[:i] + content[pos_endl:]

        i += 1

    return content


def split_var_str(var_str):
    pos = len(var_str) - 1
    if var_str[pos] in ")]}":
        while pos >= 0 and var_str[pos] in ")]}":
            pos = rfind_pair(var_str, pos)
            pos -= 1
            pos = rskip_space(var_str, pos)
        return var_str[: pos + 1], var_str[pos + 1 :]
    else:
        pos = var_str.rfind(".")
        if pos != -1:
            return var_str[:pos], var_str[pos:]
        else:
            return "", ""


def di(id_var):
    return PyObj_FromPtr(id_var)


def LP_LP_c_char(str_list):
    lp_c_char = ctypes.POINTER(ctypes.c_char)
    len_str_list = len(str_list)
    result = (lp_c_char * len_str_list)()
    for i in range(len_str_list):
        result[i] = ctypes.create_string_buffer(str_list[i].encode("utf-8"))
    return result


def capacity_of(length):
    if length <= 0:
        return 2
    else:
        return int(math.pow(2, math.floor(1 + math.log2(length))))


@checktype
def quat_to_mat4(q: glm.quat):
    w = q.w
    x = q.x
    y = q.y
    z = q.z

    return glm.mat4(
        1 - 2 * (y**2 + z**2),
        2 * (x * y + w * z),
        2 * (x * z - w * y),
        0,
        2 * (x * y - w * z),
        1 - 2 * (x**2 + z**2),
        2 * (y * z + w * x),
        0,
        2 * (x * z + w * y),
        2 * (y * z - w * x),
        1 - 2 * (x**2 + y**2),
        0,
        0,
        0,
        0,
        1,
    )


@checktype
def quat_to_mat3(q: glm.quat):
    w = q.w
    x = q.x
    y = q.y
    z = q.z

    return glm.mat3(
        1 - 2 * (y**2 + z**2),
        2 * (x * y + w * z),
        2 * (x * z - w * y),
        2 * (x * y - w * z),
        1 - 2 * (x**2 + z**2),
        2 * (y * z + w * x),
        2 * (x * z + w * y),
        2 * (y * z - w * x),
        1 - 2 * (x**2 + y**2),
    )


def scale_to_mat4(s: glm.vec3):
    return glm.mat4(s.x, 0, 0, 0, 0, s.y, 0, 0, 0, 0, s.z, 0, 0, 0, 0, 1)


def scale_to_mat3(s: glm.vec3):
    return glm.mat3(s.x, 0, 0, 0, s.y, 0, 0, 0, s.z)


def translate_to_mat4(t: glm.vec3):
    return glm.mat4(1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, t.x, t.y, t.z, 1)


def defines_key(*args):
    shader_type_defines = {
        "VERTEX_SHADER",
        "TESS_CONTROL_SHADER",
        "TESS_EVALUATION_SHADER",
        "GEOMETRY_SHADER",
        "FRAGMENT_SHADER",
        "COMPUTE_SHADER",
    }

    defines = {}
    for arg in args:
        defines.update(arg)

    keys = list(defines.keys())
    keys.sort()
    defines_str = ""
    for key in keys:
        if key in shader_type_defines:
            continue

        part = key
        if defines[key] is not None:
            part += f"={defines[key]}"
        defines_str += ":" + part

    return defines_str
