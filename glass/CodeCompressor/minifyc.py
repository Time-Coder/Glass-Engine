from .pcpp import pcmd
import io
import re
import os
from typing import Tuple, Dict, Optional, List, Set


def is_space(char):
    return char in [" ", "\t", "\n", "\r", "\v", "\f"]


def is_identifier_part(char):
    return (
        "a" <= char <= "z"
        or "A" <= char <= "Z"
        or "0" <= char <= "9"
        or char in ["$", "_"]
    )


def cut(s, lef, rig, ind):
    return s[lef[ind] : rig[ind] + 1]


def safe_index_of(s, ch, ind):
    while ind != len(s) and not is_space(s[ind]):
        if s[ind] == ch:
            return ind
        ind += 1
    return -1


def process_trigraph(str):
    trigraphs = {
        "=": "#",
        "/": "\\",
        "'": "^",
        "(": "[",
        ")": "]",
        "<": "{",
        ">": "}",
        "!": "|",
        "-": "~",
    }
    for ch, replacement in trigraphs.items():
        ret = ""
        lst = 0
        pattern = "??" + ch
        while lst != len(str):
            ind = str.find(pattern, lst)
            if ind == -1:
                break
            ret += str[lst:ind] + replacement
            lst = ind + len(pattern)
        ret += str[lst:]
        str = ret
    return str


def process_line_break(str):
    lines = str.split("\n")
    ret = ""
    for line in lines:
        j = len(line)
        while j > 0 and is_space(line[j - 1]):
            j -= 1
        if line[j - 1 : j] == "\\":
            ret += line[: j - 1]
        else:
            ret += line + "\n"
    if ret and ret[-1] == "\n":
        ret = ret[:-1]
    return ret


def process_multiline_comment_and_replace_mark(str):
    ret = ""
    string_begin, esc = None, False
    in_string = False
    lst = 0
    i = 0
    while i < len(str):
        if in_string:
            if not esc and str[i] == string_begin:
                in_string = False
        elif str[i] in ["'", '"']:
            in_string = True
            string_begin = str[i]
        elif i + 1 < len(str):
            if str[i : i + 2] == "/*":
                ret += str[lst:i] + " "
                i = str.find("*/", i + 2) + 2
                lst = i
                if i == -1:
                    break
            elif str[i : i + 2] == "%:":
                ret += str[lst:i] + "#"
                i += 2
                lst = i
        esc = str[i] == "\\"
        i += 1
    ret += str[lst:]
    return ret


def minifyc(str):
    return _compress(_compress(str))


def _compress(str):
    ret = ""
    lst = 0
    pattern_s = 'R"('
    pattern_t = ')"'
    while lst < len(str):
        ind = str.find(pattern_s, lst)
        if ind == -1:
            break
        ret += compress_single(str[lst:ind])
        rig = str.find(pattern_t, ind + len(pattern_s))
        if rig == -1:
            ret += str[ind:]
            lst = len(str)
            break
        lst = rig + len(pattern_t)
        ret += str[ind:lst]
    ret += compress_single(str[lst:])
    return ret


def compress_single(str):
    str = process_trigraph(str)
    str = process_line_break(str)
    str = process_multiline_comment_and_replace_mark(str)

    arr = str.split("\n")
    ret = ""
    force_newline = True
    last = "\0"
    for line in arr:
        if not line:
            continue

        i = 0
        lef, rig = [], []

        while True:
            while i < len(line) and is_space(line[i]):
                i += 1
            if i == len(line):
                break
            lef.append(i)
            in_string = False
            string_begin, esc = None, False
            break_lex = False
            while i < len(line) and (in_string or not is_space(line[i])):
                if in_string:
                    if not esc and line[i] == string_begin:
                        in_string = False
                elif line[i] in ['"', "'"]:
                    in_string = True
                    string_begin = line[i]
                elif line[i] == "/" and i < len(line) - 1 and line[i + 1] == "/":
                    rig.append(i - 1)
                    lef.append(i)
                    rig.append(len(line) - 1)
                    break_lex = True
                    break
                i += 1
                if i == len(line):
                    break
                esc = line[i] == "\\"
            if break_lex:
                break
            rig.append(i - 1)

        n = len(lef)
        if not n:
            continue

        origin_force_newline = force_newline
        origin_last = last

        if last != "\0":
            if force_newline:
                ret += "\n"
            elif check(last, line[lef[0]]):
                ret += " "

        last = line[rig[n - 1]]
        j = 0

        if line[lef[0]] == "#":
            if not force_newline:
                ret += "\n"
            force_newline = True
            if not line[lef[0] + 1]:
                j = 1
                lef[1] -= 1
                line = line[: lef[1]] + "#" + line[lef[1] + 1 :]
            ret += cut(line, lef, rig, j)
            if line[lef[j] + 1] == "d" and safe_index_of(line, "(", lef[j + 1]) == -1:
                j += 1
                ret += " " + cut(line, lef, rig, j)
                if j + 1 < n:
                    j += 1
                    ret += " " + cut(line, lef, rig, j)

            j += 1
        else:
            force_newline = False

        while j < n:
            if lef[j] + 2 <= len(line) and line[lef[j] : lef[j] + 2] == "//":
                if j == 0:
                    force_newline = origin_force_newline
                break
            if j and check(line[rig[j - 1]], line[lef[j]]):
                ret += " "
            ret += cut(line, lef, rig, j)
            j += 1

        last = line[rig[j - 1]] if j else origin_last

    return ret


def check(a, b):
    return (
        (is_identifier_part(a) and is_identifier_part(b))
        or ((a in [" + ", "-"]) and a == b)
        or (a == "/" and b == "*")
    )

def short_file_name(file_name):
    abs_file_name = os.path.abspath(file_name).replace("\\", "/")
    rel_file_name = os.path.relpath(abs_file_name).replace("\\", "/")
    if len(rel_file_name) > len(abs_file_name):
        return abs_file_name
    else:
        return rel_file_name

def process_line_directives(code):
    line_pattern = re.compile(r'^\s*#line\s+(\d+)\s+(?:"(?P<file_name>[^"]*)"|(\S+)).*$', re.MULTILINE)
    lines = code.split('\n')
    processed_lines = []
    line_mapping = {}
    current_file = None
    current_original_line = 1
    processed_line_number = 1
    
    for line in lines:
        match = line_pattern.match(line)
        if match:
            original_line = int(match.group(1))
            file_name = match.group(2) or match.group(3) or ""
            current_file = file_name
            current_original_line = original_line
        else:
            processed_lines.append(line)
            if current_file is not None:
                line_mapping[processed_line_number] = (short_file_name(current_file), current_original_line)
            processed_line_number += 1
            current_original_line += 1

    related_files = set()
    def add_related_file(match):
        file_name = os.path.abspath(match.group("file_name")).replace("\\", "/")
        related_files.add(file_name)
        return ""
    
    line_pattern.sub(add_related_file, code)
    
    return '\n'.join(processed_lines), line_mapping, related_files


def macros_expand(file, include_paths: Optional[List[str] ] = None, defines: Optional[Dict[str, str] ] = None)->Tuple[str, Dict[int, Tuple[str, int] ], Set[str]]:
    output = io.StringIO()

    if defines is None:
        defines = {}

    if include_paths is None:
        include_paths = []

    cmds = ["", ""]

    for path in include_paths:
        cmds.append(f"-I{path}")

    for name, value in defines.items():
        arg = f"-D{name}"
        if value is not None:
            arg += f"={value}"
        cmds.append(arg)

    pcmd.CmdPreprocessor(cmds, file, output)
    return process_line_directives(output.getvalue())


def macros_expand_code(code: str, include_paths: Optional[List[str] ] = None, defines: Optional[Dict[str, str] ] = None)->Tuple[str, Dict[int, Tuple[str, int] ], Set[str]]:
    input = io.StringIO(code)
    input.name = "<string>"

    return macros_expand(input, include_paths, defines)

def macros_expand_file(filename: str, include_paths: Optional[List[str] ] = None, defines: Optional[Dict[str, str] ] = None)->Tuple[str, Dict[int, Tuple[str, int] ], Set[str]]:
    input = open(filename, 'r', encoding='utf-8')

    return macros_expand(input, include_paths, defines)
