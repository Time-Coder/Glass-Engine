import sys
import os
self_folder = os.path.dirname(os.path.abspath(__file__))
glass_folder = os.path.abspath(self_folder + '/../../').replace("\\", "/")

sys.path.insert(0, glass_folder)

import subprocess
import re
import warnings
from glass.CodeCompressor.minifyc import macros_expand_file


class CompileError(Exception):
    pass

class CompileWarning(Warning):
    pass

def short_file_name(file_name):
    abs_file_name = os.path.abspath(file_name).replace("\\", "/")
    rel_file_name = os.path.relpath(abs_file_name).replace("\\", "/")
    if len(rel_file_name) > len(abs_file_name):
        return abs_file_name
    else:
        return rel_file_name


def format_error_warning(message, line_map):
    def _replace_message(match):
        message_type = match.group("message_type").lower()
        line_number = int(match.group("line_number"))
        file_name = line_map[line_number][0]
        new_line_number = line_map[line_number][1]
        return file_name + ":" + str(new_line_number) + ": " + message_type + ": "

    message_prefix1 = re.compile(
        r"^0\((?P<line_number>\d+)\) : (?P<message_type>\w+) ", flags=re.M
    )
    message_prefix2 = re.compile(
        r"^(?P<message_type>\w+): 0:(?P<line_number>\d+): ", flags=re.M
    )
    message_prefix3 = re.compile(
        r"^(?P<message_type>\w+): ([a-zA-Z]:[/\\]+)?[/\\]*([^<>:\"/\\|?*]+[/\\]+)*([^<>:\"/\\|?*]+)?:(?P<line_number>\d+): ",
        flags=re.M,
    )

    message = message_prefix1.sub(_replace_message, message)
    message = message_prefix2.sub(_replace_message, message)
    message = message_prefix3.sub(_replace_message, message)
    message = message.replace("syntax error syntax error", "syntax error")
    message = message.replace("'' : ", "")
    message = message.strip(" \t\n\r")

    warning_messages = []
    error_messages = []
    last = ""

    lines = message.split("\n")
    for line in lines:
        line = line.strip(" \t\n\r")
        if not line:
            continue

        if "error" in line.lower():
            error_messages.append(line)
            last = "error"
        elif "warning" in line.lower():
            warning_messages.append(line)
            last = "warning"
        elif last == "error":
            error_messages.append(line)
        elif last == "warning":
            warning_messages.append(line)

    return error_messages, warning_messages

define_keys = [
    "USE_DYNAMIC_ENV_MAPPING",
    "USE_DIR_LIGHT",
    "USE_DIR_LIGHT_SHADOW",
    "USE_POINT_LIGHT",
    "USE_POINT_LIGHT_SHADOW",
    "USE_SPOT_LIGHT",
    "USE_SPOT_LIGHT_SHADOW",
    "USE_FOG",
    "USE_SHADING_MODEL_FLAT",
    "USE_SHADING_MODEL_GOURAUD",
    "USE_SHADING_MODEL_PHONG",
    "USE_SHADING_MODEL_PHONG_BLINN",
    "USE_SHADING_MODEL_TOON",
    "USE_SHADING_MODEL_OREN_NAYAR",
    "USE_SHADING_MODEL_MINNAERT",
    "USE_SHADING_MODEL_COOK_TORRANCE",
    "USE_SHADING_MODEL_UNLIT",
    "USE_SHADING_MODEL_FRESNEL",
    "USE_BINDLESS_TEXTURE",
    "USE_SHADER_STORAGE_BLOCK"
]
defines = {"CSM_LEVELS":5, "FILE_NAME": "\"lut.glsl\""}
for i in range(len(define_keys)):
    defines[define_keys[i]] = 1


for root, dirs, files in os.walk(self_folder):
    for file in files:
        ext_name = file.split(".")[-1]
        if ext_name in ["vert", "frag", "geom", "tesc", "tese", "comp"]:
            file_name = f"{root}/{file}".replace("\\", "/")
            if "/temp/" in file_name:
                continue

            used_file_name = short_file_name(file_name)
            print("checking", used_file_name)
            target_file_name = self_folder + "/temp/" + os.path.relpath(file_name, self_folder).replace("\\", "/")
            target_folder = os.path.dirname(target_file_name)
            if not os.path.exists(target_folder):
                os.makedirs(target_folder)
            code, line_map = macros_expand_file(file_name, defines=defines, with_line_map=True)
            with open(target_file_name, "w") as f:
                f.write(code)
            
            result = subprocess.run(
                ["glslangValidator", target_file_name],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )
            error_messages, warning_messages = format_error_warning(result.stdout.strip(), line_map)

            if warning_messages:
                warning_message = (
                    f"\nWarning when compiling: {used_file_name}:\n"
                    + "\n".join(warning_messages)
                )
                warnings.warn(warning_message, category=CompileWarning)

            if error_messages:
                error_message = f"\nError when compiling: {used_file_name}:\n" + "\n".join(
                    error_messages
                )
                raise CompileError(error_message)
            
            if result.returncode != 0:
                raise CompileError(result.stdout.strip())