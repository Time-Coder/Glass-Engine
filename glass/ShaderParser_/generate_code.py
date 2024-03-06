import requests
import requests_cache
import bs4
import os

requests_cache.install_cache()

atom_type_names = [
    "bool",
    "int",
    "uint",
    "uint64_t",
    "float",
    "double",
    "atomic_uint",
    "bvec2",
    "bvec3",
    "bvec4",
    "ivec2",
    "ivec3",
    "ivec4",
    "uvec2",
    "uvec3",
    "uvec4",
    "vec2",
    "vec3",
    "vec4",
    "dvec2",
    "dvec3",
    "dvec4",
    "mat2x2",
    "mat3x2",
    "mat4x2",
    "mat2x3",
    "mat3x3",
    "mat4x3",
    "mat2x4",
    "mat3x4",
    "mat4x4",
    "mat2",
    "mat3",
    "mat4",
    "dmat2x2",
    "dmat3x2",
    "dmat4x2",
    "dmat2x3",
    "dmat3x3",
    "dmat4x3",
    "dmat2x4",
    "dmat3x4",
    "dmat4x4",
    "dmat2",
    "dmat3",
    "dmat4",
    "sampler1D",
    "isampler1D",
    "usampler1D",
    "sampler2D",
    "isampler2D",
    "usampler2D",
    "sampler3D",
    "isampler3D",
    "usampler3D",
    "sampler1DShadow",
    "isampler1DShadow",
    "usampler1DShadow",
    "sampler2DShadow",
    "isampler2DShadow",
    "usampler2DShadow",
    "sampler3DShadow",
    "isampler3DShadow",
    "usampler3DShadow",
    "sampler1DArray",
    "isampler1DArray",
    "usampler1DArray",
    "sampler2DArray",
    "isampler2DArray",
    "usampler2DArray",
    "sampler1DArrayShadow",
    "isampler1DArrayShadow",
    "usampler1DArrayShadow",
    "sampler2DArrayShadow",
    "isampler2DArrayShadow",
    "usampler2DArrayShadow",
    "sampler2DMS",
    "isampler2DMS",
    "usampler2DMS",
    "sampler2DMSArray",
    "isampler2DMSArray",
    "usampler2DMSArray",
    "samplerCube",
    "isamplerCube",
    "usamplerCube",
    "samplerCubeArray",
    "isamplerCubeArray",
    "usamplerCubeArray",
    "samplerCubeShadow",
    "isamplerCubeShadow",
    "usamplerCubeShadow",
    "samplerCubeArrayShadow",
    "isamplerCubeArrayShadow",
    "usamplerCubeArrayShadow",
    "sampler2DRect",
    "isampler2DRect",
    "usampler2DRect",
    "sampler2DRectShadow",
    "isampler2DRectShadow",
    "usampler2DRectShadow",
    "samplerBuffer",
    "isamplerBuffer",
    "usamplerBuffer",
    "image1D",
    "iimage1D",
    "uimage1D",
    "image2D",
    "iimage2D",
    "uimage2D",
    "image3D",
    "iimage3D",
    "uimage3D",
    "imageCube",
    "iimageCube",
    "uimageCube",
    "imageCubeArray",
    "iimageCubeArray",
    "uimageCubeArray",
    "image2DRect",
    "iimage2DRect",
    "iimage2DRect",
    "image2DRect",
    "iimage2DRect",
    "iimage2DRect",
    "image1DArray",
    "iimage1DArray",
    "iimage1DArray",
    "image2DArray",
    "iimage2DArray",
    "uimage2DArray",
    "imageBuffer",
    "iimageBuffer",
    "uimageBuffer",
    "image2DMS",
    "iimage2DMS",
    "uimage2DMS",
    "image2DMSArray",
    "iimage2DMSArray",
    "uimage2DMSArray",
]

func_list = [
    "abs",
    "acos",
    "acosh",
    "all",
    "any",
    "asin",
    "asinh",
    "atan",
    "atanh",
    "atomicAdd",
    "atomicAnd",
    "atomicCompSwap",
    "atomicCounter",
    "atomicCounterDecrement",
    "atomicCounterIncrement",
    "atomicExchange",
    "atomicMax",
    "atomicMin",
    "atomicOr",
    "atomicXor",
    "barrier",
    "bitCount",
    "bitfieldExtract",
    "bitfieldInsert",
    "bitfieldReverse",
    "ceil",
    "clamp",
    "cos",
    "cosh",
    "cross",
    "degrees",
    "determinant",
    "dFdx",
    # "dFdxCoarse",
    # "dFdxFine",
    # "dFdy",
    # "dFdyCoarse",
    # "dFdyFine",
    "distance",
    "dot",
    "EmitStreamVertex",
    "EmitVertex",
    "EndPrimitive",
    "EndStreamPrimitive",
    "equal",
    "exp",
    "exp2",
    "faceforward",
    "findLSB",
    "findMSB",
    "floatBitsToInt",
    # "floatBitsToUint",
    "floor",
    "fma",
    "fract",
    "frexp",
    "fwidth",
    # "fwidthCoarse",
    # "fwidthFine",
    "greaterThan",
    "greaterThanEqual",
    "groupMemoryBarrier",
    "imageAtomicAdd",
    "imageAtomicAnd",
    "imageAtomicCompSwap",
    "imageAtomicExchange",
    "imageAtomicMax",
    "imageAtomicMin",
    "imageAtomicOr",
    "imageAtomicXor",
    "imageLoad",
    "imageSamples",
    "imageSize",
    "imageStore",
    # "imulExtended",
    "intBitsToFloat",
    "interpolateAtCentroid",
    "interpolateAtOffset",
    "interpolateAtSample",
    "inverse",
    "inversesqrt",
    "isinf",
    "isnan",
    "ldexp",
    "length",
    "lessThan",
    "lessThanEqual",
    "log",
    "log2",
    "matrixCompMult",
    "max",
    "memoryBarrier",
    "memoryBarrierAtomicCounter",
    "memoryBarrierBuffer",
    "memoryBarrierImage",
    "memoryBarrierShared",
    "min",
    "mix",
    "mod",
    "modf",
    "noise",
    # "noise1",
    # "noise2",
    # "noise3",
    # "noise4",
    "normalize",
    "not",
    "notEqual",
    "outerProduct",
    "packDouble2x32",
    "packHalf2x16",
    # "packSnorm2x16",
    # "packSnorm4x8",
    "packUnorm",
    # "packUnorm2x16",
    # "packUnorm4x8",
    "pow",
    "radians",
    "reflect",
    "refract",
    "round",
    "roundEven",
    "sign",
    "sin",
    "sinh",
    "smoothstep",
    "sqrt",
    "step",
    "tan",
    "tanh",
    "texelFetch",
    "texelFetchOffset",
    "texture",
    "textureGather",
    "textureGatherOffset",
    "textureGatherOffsets",
    "textureGrad",
    "textureGradOffset",
    "textureLod",
    "textureLodOffset",
    "textureOffset",
    "textureProj",
    "textureProjGrad",
    "textureProjGradOffset",
    "textureProjLod",
    "textureProjLodOffset",
    "textureProjOffset",
    "textureQueryLevels",
    "textureQueryLod",
    "textureSamples",
    "textureSize",
    "transpose",
    "trunc",
    "uaddCarry",
    # "uintBitsToFloat",
    "umulExtended",
    "unpackDouble2x32",
    "unpackHalf2x16",
    # "unpackSnorm2x16",
    # "unpackSnorm4x8",
    "unpackUnorm",
    # "unpackUnorm2x16",
    # "unpackUnorm4x8",
    "usubBorrow",
]

gen_type_map = {
    "genType": ["float", "vec2", "vec3", "vec4"],
    "genDType": ["double", "dvec2", "dvec3", "dvec4"],
    "genIType": ["int", "ivec2", "ivec3", "ivec4"],
    "genUType": ["uint", "uvec2", "uvec3", "uvec4"],
    "genBType": ["bool", "bvec2", "bvec3", "bvec4"],
    "mat": ["mat2", "mat3", "mat4"],
    "dmat": ["dmat2", "dmat3", "dmat4"],
    "gsampler1D": ["sampler1D", "isampler1D", "usampler1D"],
    "gsampler2D": ["sampler2D", "isampler2D", "usampler2D"],
    "gsampler3D": ["sampler3D", "isampler3D", "usampler3D"],
    "gsampler2DMS": ["sampler2DMS", "isampler2DMS", "usampler2DMS"],
    "gsamplerCube": ["samplerCube", "isamplerCube", "usamplerCube"],
    "gsampler1DArray": ["sampler1DArray", "isampler1DArray", "usampler1DArray"],
    "gsampler2DArray": ["sampler2DArray", "isampler2DArray", "usampler2DArray"],
    "gsampler2DMSArray": ["sampler2DMSArray", "isampler2DMSArray", "usampler2DMSArray"],
    "gsamplerCubeArray": ["samplerCubeArray", "isamplerCubeArray", "usamplerCubeArray"],
    "gsampler2DRect": ["sampler2DRect", "isampler2DRect", "usampler2DRect"],
    "gimage1D": ["image1D", "iimage1D", "uimage1D"],
    "gimage2D": ["image2D", "iimage2D", "uimage2D"],
    "gimage3D": ["image3D", "iimage3D", "uimage3D"],
    "gimageCube": ["imageCube", "iimageCube", "uimageCube"],
    "gimageCubeArray": ["imageCubeArray", "iimageCubeArray", "uimageCubeArray"],
    "gimageRect": ["image2DRect", "iimage2DRect", "iimage2DRect"],
    "gimage2DRect": ["image2DRect", "iimage2DRect", "iimage2DRect"],
    "gimage1DArray": ["image1DArray", "iimage1DArray", "iimage1DArray"],
    "gimage2DArray": ["image2DArray", "iimage2DArray", "uimage2DArray"],
    "gimageBuffer": ["imageBuffer", "iimageBuffer", "uimageBuffer"],
    "gbufferImage": ["imageBuffer", "iimageBuffer", "uimageBuffer"],
    "gimage2DMS": ["image2DMS", "iimage2DMS", "uimage2DMS"],
    "gimage2DMSArray": ["image2DMSArray", "iimage2DMSArray", "uimage2DMSArray"],
    "gsamplerBuffer": ["samplerBuffer", "isamplerBuffer", "usamplerBuffer"],
    "gvec2": ["vec2", "ivec2", "uvec2"],
    "gvec3": ["vec3", "ivec3", "uvec3"],
    "gvec4": ["vec4", "ivec4", "uvec4"],
    "bvec": ["bvec2", "bvec3", "bvec4"],
    "vec": ["vec2", "vec3", "vec4"],
    "ivec": ["ivec2", "ivec3", "ivec4"],
    "uvec": ["uvec2", "uvec3", "uvec4"],
    "dvec": ["dvec2", "dvec3", "dvec4"],
}

definition_dict = {}

for func_name in func_list:
    response = requests.get(
        f"https://registry.khronos.org/OpenGL-Refpages/gl4/html/{func_name}.xhtml"
    )
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    code_block = soup.select(f"#{func_name} > div.refsynopsisdiv")
    if not code_block:
        print(func_name, "failed")
        continue

    success = False
    for div in code_block[0].children:
        if not isinstance(div, bs4.element.Tag):
            continue

        if div.name != "div":
            continue

        div_class = div.get("class")
        if not isinstance(div_class, list) or "funcsynopsis" not in div_class:
            continue

        for table in div.children:
            if not isinstance(table, bs4.element.Tag):
                continue

            if table.name != "table":
                continue

            code = table.get_text()
            return_type = code.split(" ")[0].strip(" \t\n")
            func_name_ = code.split("(")[0].split(" ")[1].strip(" \t\n")
            arg_strs = [
                arg.strip(" \t\n\xa0")
                for arg in code.split("(")[1].strip(" \t\n);").split(",")
            ]
            if return_type in gen_type_map:
                return_type = gen_type_map[return_type]

            n_optionals = 0
            n_gen_types = 0
            arg_names = []
            arg_types = []
            for i, arg_str in enumerate(arg_strs):
                items = arg_str.split(" ")
                if len(items) < 2:
                    continue

                arg_type = items[-2]
                arg_name = items[-1]
                if arg_type[0] == "[":
                    n_optionals += 1
                    arg_type = arg_type[1:]
                    arg_name = arg_name[:-1]

                if arg_type in gen_type_map:
                    arg_types.append(gen_type_map[arg_type])
                    n_gen_types = len(gen_type_map[arg_type])
                else:
                    arg_types.append(arg_type)

                arg_names.append(arg_name)

            argc = len(arg_names)
            if n_gen_types == 0:
                n_gen_types = 1

            if not isinstance(return_type, list):
                return_type = [return_type] * n_gen_types

            for i in range(len(arg_types)):
                if not isinstance(arg_types[i], list):
                    arg_types[i] = [arg_types[i]] * n_gen_types

            for j in range(n_gen_types):
                for i in range(n_optionals + 1):
                    local_arg_types = [
                        arg_type[j] for arg_type in arg_types[: argc - i]
                    ]
                    signature = f"{func_name_}({', '.join(local_arg_types)})"
                    definition_dict[signature] = {
                        "name": func_name_,
                        "return_type": return_type[j],
                        "arg_types": local_arg_types,
                        "arg_names": arg_names[: argc - i],
                        "signature": signature,
                    }

            success = True

    if not success:
        print(func_name, "failed")

self_folder = os.path.dirname(os.path.abspath(__file__))
content = open(self_folder + "/ShaderBuiltins.py").read()
pos_func = content.find("functions = ")
if pos_func == -1:
    exit()

content = content[:pos_func] + "functions = {\n"
for func in definition_dict.values():
    content += f'        "{func["signature"]}": Func(\n'
    content += f'            return_type="{func["return_type"]}",\n'
    content += f'            name="{func["name"]}",\n'
    content += "            args=[\n"
    for arg_name, arg_type in zip(func["arg_names"], func["arg_types"]):
        if arg_type not in atom_type_names:
            print(f"not supported type '{arg_type}'", func["name"])

        pos_bracket = arg_name.find("[")
        if pos_bracket != -1:
            arg_type += arg_name[pos_bracket:]
            arg_name = arg_name[:pos_bracket]
        content += f'                Var(name="{arg_name}", type="{arg_type}"),\n'
    content += "            ]\n"
    content += "        ),\n"
content += "    }\n"

out_file = open(self_folder + "/ShaderBuiltins.py", "w")
out_file.write(content)
out_file.close()
