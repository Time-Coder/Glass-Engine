from tree_sitter import Language, Parser
import pcpp
import sys
import os
import io

def macros_expand(code:str, defines:dict=None)->str:
    output = io.StringIO()
    input = io.StringIO(code)
    input.name = "<string>"

    if defines is None:
        defines = {}

    cmds = ["", "", "--line-directive"]
    for name, value in defines.items():
        arg = f"-D{name}"
        if value is not None:
            arg += f"={value}"
        cmds.append(arg)

    pcpp.pcmd.CmdPreprocessor(cmds, input, output)
    return output.getvalue()

def _get_funcs_and_structs(node, func_defs:dict, struct_defs:dict):
    if node.grammar_name == "function_definition":
        func_name = str(node.children[1].children[0].text, encoding="utf-8")
        args = []
        arg_types = []
        for child in node.children[1].children[1].children:
            if child.grammar_name == "parameter_declaration":
                arg = {}
                if child.children[0].grammar_name in ["identifier", "type_identifier", "primitive_type"]:
                    arg["modifier"] = "in"
                    arg["type"] = str(child.children[0].text, encoding="utf-8")
                elif child.children[0].grammar_name in ["in", "inout", "out"]:
                    arg["modifier"] = str(child.children[0].text, encoding="utf-8")
                    arg["type"] = str(child.children[1].text, encoding="utf-8")

                args.append(arg)
                arg_types.append(arg["type"])

        func = \
        {
            "signature": f"{func_name}({", ".join(arg_types)})",
            "name": func_name,
            "args": args,
            "start": node.start_byte,
            "end": node.end_byte,
            "body": str(node.children[2].text, encoding="utf-8"),
            "node": node,
            "body_node": node.children[2],
            "used": False
        }
        if func_name not in func_defs:
            func_defs[func_name] = []

        func_defs[func_name].append(func)
        return

    if node.grammar_name == "struct_specifier":
        struct_name = str(node.children[1].text, encoding="utf-8")
        struct = {}
        struct["name"] = struct_name
        struct["start"] = node.start_byte
        struct["end"] = node.end_byte
        struct["used"] = False
        struct_defs[struct_name] = struct
        return

    for child in node.children:
        _get_funcs_and_structs(child, func_defs, struct_defs)

def _find_func_calls(node, func_calls:list):
    if node.grammar_name == "call_expression":
        func_call = {}
        func_call["name"] = str(node.children[0].text, encoding="utf-8")
        func_call["argc"] = 0
        for child in node.children[1].children:
            if child.grammar_name not in "(),":
                func_call["argc"] += 1

        func_calls.append(func_call)

    for child in node.children:
        _find_func_calls(child, func_calls)

def _remove_segments(content, segments):
    segments.sort(reverse=True, key=lambda x: x[0])
    result = content
    for start, end in segments:
        result = result[:start] + result[end:]
    return result

def _find_node_used_structs(node, structs_defs:dict):
    if node.grammar_name == "identifier":
        identifier_name = str(node.text, encoding="utf-8")
        if identifier_name in structs_defs:
            structs_defs[identifier_name]["used"] = True

    for child in node.children:
        _find_node_used_structs(child, structs_defs)

def _find_used_structs(func, structs_defs:dict):
    for arg in func["args"]:
        if arg["type"] in structs_defs:
            structs_defs[arg["type"]]["used"] = True

    body_node = func["body_node"]
    _find_node_used_structs(body_node, structs_defs)

glsl_parser = None
def treeshake(code:str, defines:dict=None)->str:
    global glsl_parser
    if glsl_parser is None:
        self_folder = os.path.dirname(os.path.abspath(__file__))
        GLSL_LANGUAGE = Language(self_folder + "/tree-sitter-glsl/glsl.dll", 'glsl')
        glsl_parser = Parser()
        glsl_parser.set_language(GLSL_LANGUAGE)

    code = macros_expand(code, defines)
    tree = glsl_parser.parse(bytes(code, sys.getdefaultencoding()))
    root_node = tree.root_node
    
    func_defs = {}
    structs_defs = {}
    _get_funcs_and_structs(root_node, func_defs, structs_defs)

    used_funcs = set()

    main_func = func_defs["main"][0]
    main_func["used"] = True
    func_stack = [main_func]
    _find_used_structs(main_func, structs_defs)
    while func_stack:
        parent_func = func_stack.pop()
        body_node = parent_func["body_node"]
        func_calls = []
        _find_func_calls(body_node, func_calls)
        for func_call in func_calls:
            func_name = func_call["name"]
            if func_name not in func_defs:
                continue

            funcs = func_defs[func_name]
            for func in funcs:
                if len(func["args"]) != func_call["argc"]:
                    continue

                signature = func["signature"]
                if signature in used_funcs:
                    continue
                
                func["used"] = True
                _find_used_structs(func, structs_defs)
                func_stack.append(func)
                used_funcs.add(signature)
    
    segments_to_remove = []
    for funcs in func_defs.values():
        for func in funcs:
            if not func["used"]:
                segments_to_remove.append((func["start"], func["end"]))

    return _remove_segments(code, segments_to_remove)
