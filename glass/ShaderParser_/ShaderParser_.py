import sys
import os
import glob
import tree_sitter
import zipfile
import platform

from ..GLInfo import GLInfo
from .ShaderSyntaxTokens import Var, Attribute, Func, FuncCall, Struct, SimpleVar
from .ShaderBuiltins import ShaderBuiltins

from ..utils import resolve_array
from ..helper import greater_type, type_list_distance, subscript_type

from OpenGL import GL
from tree_sitter import Language, Parser
from typing import List, Dict, Union


class ShaderParser_:

    __glsl_parser = None

    def __init__(self, shader_type):
        self.ins: Dict[str, Var] = {}
        self.outs: Dict[str, Var] = {}
        self.attributes: Dict[str, Attribute] = {}
        self.hidden_vars: Dict[str, Var] = {}
        self.global_vars: Dict[str, Var] = {}
        self.structs: Dict[str, Struct] = {}
        self.uniforms: Dict[str, Var] = {}
        self.uniform_blocks: Dict[str, Var] = {}
        self.shader_storage_blocks: Dict[str, Var] = {}
        self.functions: Dict[str, Func] = {}
        self.function_groups: Dict[str, List[Func]] = {}
        self.geometry_in: str = ""

        self.accum_location = {"in": 0, "out": 0}
        self.shader_type = shader_type

    @staticmethod
    def glsl_parser():
        if ShaderParser_.__glsl_parser is not None:
            return ShaderParser_.__glsl_parser

        self_folder = os.path.dirname(os.path.abspath(__file__))
        platform_system = platform.system()
        if platform_system == "Linux":
            dll_suffix = "so"
        elif platform_system == "Darwin":
            dll_suffix = "dylib"
        else:
            dll_suffix = "dll"

        machine = platform.machine()
        bits = platform.architecture()[0]

        dll_file = f"{self_folder}/tree-sitter-glsl/lib/{machine}/{platform_system}/{bits}/glsl.{dll_suffix}"
        dll_folder = os.path.dirname(dll_file)
        if not os.path.isdir(dll_folder):
            os.makedirs(dll_folder)

        if not os.path.isfile(dll_file):
            if not os.path.isfile(self_folder + "/tree-sitter-glsl/src/parser.c"):
                zip_file = zipfile.ZipFile(self_folder + "/tree-sitter-glsl/src.zip")
                zip_file.extractall(self_folder + "/tree-sitter-glsl/src")
                zip_file.close()

            Language.build_library(dll_file, [self_folder + "/tree-sitter-glsl"])
            trash_files = glob.glob(f"{dll_folder}/glsl.*")
            for trash_file in trash_files:
                if os.path.abspath(trash_file) != os.path.abspath(dll_file):
                    os.remove(trash_file)

        GLSL_LANGUAGE = Language(dll_file, "glsl")
        ShaderParser_.__glsl_parser = Parser()
        ShaderParser_.__glsl_parser.set_language(GLSL_LANGUAGE)
        return ShaderParser_.__glsl_parser

    @staticmethod
    def parse_struct_declaration_list(
        struct_declaration_list: tree_sitter.Node,
    ) -> Dict[str, Var]:
        members: Dict[str, Var] = {}
        for struct_declaration in struct_declaration_list.children:
            if struct_declaration.type != "struct_declaration":
                continue

            type_specifier = struct_declaration.children[0]
            struct_declarator_list = struct_declaration.children[1]
            if type_specifier.type == "type_qualifier_list":
                type_specifier = struct_declaration.children[1]
                struct_declarator_list = struct_declaration.children[2]

            type_ = type_specifier.text.decode("utf-8")
            for struct_declarator in struct_declarator_list.children:
                if struct_declarator.type != "struct_declarator":
                    continue

                name = struct_declarator.text.decode("utf-8")
                member: Var = Var(name=name, type=type_)
                members[name] = member

        return members

    def parse_qualifiers(self, type_qualifier_list: tree_sitter.Node):
        layout_args: List[str] = []
        layout_kwargs: Dict[str, str] = {}
        other_qualifiers: List[str] = []
        in_out: str = ""
        for type_qualifier in type_qualifier_list.children:
            if type_qualifier.type != "type_qualifier":
                continue

            if type_qualifier.type == "layout_qualifier":
                for layout_qualifier_id in type_qualifier.children:
                    if layout_qualifier_id.type != "layout_qualifier_id":
                        continue

                    key = layout_qualifier_id.children[0].text.decode("utf-8")
                    if layout_qualifier_id.child_count == 1:
                        layout_args.append(key)
                    elif layout_qualifier_id.child_count == 2:
                        layout_kwargs[key] = layout_qualifier_id.children[
                            2
                        ].text.decode("utf-8")
            else:
                qualifier: str = type_qualifier.text.decode("utf-8")
                if qualifier in ["in", "out"]:
                    in_out: str = qualifier
                other_qualifiers.append(qualifier)

        if "location" in layout_kwargs and (in_out != ""):
            self.accum_location[in_out] = int(layout_kwargs["location"])

        return layout_args, layout_kwargs, other_qualifiers, in_out

    def parse_single_value_declaration(self, declaration: tree_sitter.Node):
        var_names = []
        for var_name in declaration.children:
            if var_name.type in ["identifier", "array_declarator"]:
                var_names.append(var_name)

        fully_specified_type = declaration.children[0]

        has_qualifier = False
        is_uniform = False
        if (
            fully_specified_type.child_count == 2
            and fully_specified_type.children[0].type == "type_qualifier_list"
            and fully_specified_type.children[1].type == "type_specifier"
        ):
            type_qualifier_list = fully_specified_type.children[0]
            type_specifier = fully_specified_type.children[1]
            has_qualifier = True
        elif (
            fully_specified_type.child_count == 1
            and fully_specified_type.children[0].type == "type_specifier"
        ):
            type_specifier = fully_specified_type.children[0]
            has_qualifier = False

        if has_qualifier:
            layout_args, layout_kwargs, other_qualifiers, in_out = (
                self.parse_qualifiers(type_qualifier_list)
            )
            is_attribute = (
                (layout_kwargs or "attribute" in other_qualifiers)
                and in_out == "in"
                and self.shader_type == GL.GL_VERTEX_SHADER
            )

            for var_name in var_names:
                var: Var = Var(
                    name=var_name.text.decode("utf-8"),
                    type=type_specifier.text.decode("utf-8"),
                    layout_args=layout_args,
                    layout_kwargs=layout_kwargs,
                    other_qualifiers=other_qualifiers,
                )
                if in_out != "":
                    var.location = self.accum_location[in_out]

                if var_name.type == "identifier":
                    if is_attribute:
                        attribute: Attribute = Attribute(var)
                        self.attributes[attribute.name] = attribute
                        self.attributes[attribute.location] = attribute

                    if in_out in ["in", "out"]:
                        self.accum_location[in_out] += 1
                elif var_name.type == "array_declarator":
                    pure_name = var_name.children[0].text.decode("utf-8")
                    if is_attribute:
                        length = eval(var_name.children[2].text.decode("utf-8"))
                        for i in range(length):
                            attribute = Attribute(
                                name=pure_name + f"[{i}]",
                                type=var.type,
                                location=self.accum_location[in_out],
                            )
                            self.attributes[attribute.name] = attribute
                            self.attributes[attribute.location] = attribute
                            self.accum_location[in_out] += 1
                    else:
                        if in_out in ["in", "out"]:
                            self.accum_location[in_out] += 1

                if in_out == "in":
                    self.ins[var.name] = var
                elif in_out == "out":
                    self.outs[var.name] = var
                elif "uniform" in other_qualifiers:
                    self.uniforms[var.name] = var

        else:
            type_ = type_specifier.text.decode("utf-8")
            for var_name in var_names:
                name = var_name.text.decode("utf-8")
                var = Var(name=name, type=type_)
                if is_uniform:
                    self.uniforms[var.name] = var
                else:
                    var.start_index = declaration.start_byte
                    var.end_index = declaration.end_byte
                    self.global_vars[var.name] = var

    def parse_block_declaration(self, declaration):
        var_names = []
        for var_name in declaration.children[5:]:
            if var_name.type in ["identifier", "array_declarator"]:
                var_names.append(var_name)

        block_name = declaration.children[1]

        type_qualifier_list = declaration.children[0]
        struct_declaration_list = declaration.children[3]

        layout_args, layout_kwargs, other_qualifiers, in_out = self.parse_qualifiers(
            type_qualifier_list
        )

        type_ = block_name.text.decode("utf-8")
        struct = Struct(
            name=type_,
            members=ShaderParser_.parse_struct_declaration_list(
                struct_declaration_list
            ),
        )
        self.structs[type_] = struct

        for var_name in var_names:
            name = var_name.text.decode("utf-8")
            var = Var(
                name=name,
                type=type_,
                layout_args=layout_args,
                layout_kwargs=layout_kwargs,
                other_qualifiers=other_qualifiers,
            )
            if in_out in self.accum_location:
                var.location = self.accum_location[in_out]

            if in_out == "in":
                self.ins[var.name] = var
            elif in_out == "out":
                self.outs[var.name] = var
            elif "uniform" in other_qualifiers:
                self.uniform_blocks[var.name] = var
            elif "buffer" in other_qualifiers:
                self.shader_storage_blocks[var.name] = var

            self.accum_location[in_out] += 1

        if "uniform" in other_qualifiers or "buffer" in other_qualifiers:
            var = Var(
                name=type_,
                type=type_,
                layout_args=layout_args,
                layout_kwargs=layout_kwargs,
                other_qualifiers=other_qualifiers,
            )

            if "uniform" in other_qualifiers:
                self.uniform_blocks[type_] = var
            elif "buffer" in other_qualifiers:
                self.shader_storage_blocks[type_] = var

        if not var_names:
            for member in struct.members.values():
                self.hidden_vars[member.name] = member

    @staticmethod
    def is_single_value_declaration(declaration):
        return (
            declaration.child_count >= 2
            and declaration.children[0].type == "fully_specified_type"
            and declaration.children[1].type in ["identifier", "array_declarator"]
        )

    @staticmethod
    def is_block_declaration(declaration):
        return (
            declaration.child_count >= 5
            and declaration.children[0].type == "type_qualifier_list"
            and declaration.children[1].type == "identifier"
            and declaration.children[2].type == "{"
            and declaration.children[3].type == "struct_declaration_list"
            and declaration.children[4].type == "}"
        )

    @staticmethod
    def is_struct_declaration(declaration):
        return (
            declaration.child_count == 2
            and declaration.children[0].type == "fully_specified_type"
            and declaration.children[0].child_count == 1
            and declaration.children[0].children[0].type == "type_specifier"
            and declaration.children[0].children[0].child_count == 5
            and declaration.children[0].children[0].children[0].type == "struct"
            and declaration.children[0].children[0].children[1].type == "identifier"
            and declaration.children[0].children[0].children[2].type == "{"
            and declaration.children[0].children[0].children[3].type
            == "struct_declaration_list"
            and declaration.children[0].children[0].children[4].type == "}"
            and declaration.children[1].type == ";"
        )

    def parse_struct(self, declaration: tree_sitter.Node):
        type_specifier = declaration.children[0].children[0]
        struct_declaration_list = type_specifier.children[3]
        struct_name = type_specifier.children[1].text.decode("utf-8")
        struct = Struct(
            name=struct_name,
            members=ShaderParser_.parse_struct_declaration_list(
                struct_declaration_list
            ),
            start_index=declaration.start_byte,
            end_index=declaration.end_byte,
        )
        self.structs[struct_name] = struct

    @staticmethod
    def is_only_qualifiers(declaration):
        return (
            declaration.child_count >= 2
            and declaration.children[0].type == "type_qualifier_list"
            and declaration.children[0].child_count >= 2
            and declaration.children[0].children[1].text in [b"in", b"out"]
            and declaration.children[1].type == ";"
        )

    def parse_only_qualifiers(self, declaration):
        layout_args, layout_kwargs, other_qualifiers, in_out = self.parse_qualifiers(
            declaration.children[0]
        )

        if self.shader_type == GL.GL_GEOMETRY_SHADER:
            for arg in layout_args:
                if arg in GLInfo.geometry_ins:
                    self.geometry_in = arg
                    break

        location = (
            -1 if "location" not in layout_kwargs else eval(layout_kwargs["location"])
        )
        var = Var(
            name="",
            type="",
            location=location,
            layout_args=layout_args,
            layout_kwargs=layout_kwargs,
            other_qualifiers=other_qualifiers,
        )

        if in_out == "in":
            self.ins[""] = var
        elif in_out == "out":
            self.outs[""] = var

    def find_func_calls_and_local_vars(self, node: tree_sitter.Node, func: Func):
        if node.type == "call_expression":
            func_call = FuncCall(call_expression=node)
            func.func_calls[func_call.signature] = func_call
        elif node.type == "declaration":
            declaration = node
            fully_specified_type = declaration.children[0]
            type_specifier = fully_specified_type.children[0]
            if type_specifier.type != "type_specifier":
                type_specifier = fully_specified_type.children[1]
            type_ = type_specifier.text.decode("utf-8")
            for identifier in declaration.children:
                if identifier.type != "identifier":
                    continue

                var = Var(name=identifier.text.decode("utf-8"), type=type_)
                func.local_vars.append(var)

        for child in node.children:
            self.find_func_calls_and_local_vars(child, func)

    def parse_function(self, function_definition: tree_sitter.Node):
        function_declaration = function_definition.children[0].children[0]
        statement_list = function_definition.children[1].children[1]

        fully_specified_type = function_declaration.children[0]
        identifier = function_declaration.children[1]
        has_args = False
        if function_declaration.child_count >= 4:
            function_parameter_list = function_declaration.children[3]
            has_args = True

        func = Func(
            return_type=fully_specified_type.text.decode("utf-8"),
            name=identifier.text.decode("utf-8"),
            start_index=function_definition.start_byte,
            end_index=function_definition.end_byte,
        )

        # args
        if has_args:
            for parameter_declaration in function_parameter_list.children:
                if parameter_declaration.type != "parameter_declaration":
                    continue

                parameter_declarator = parameter_declaration.children[0]
                if parameter_declarator.type != "parameter_declarator":
                    parameter_declarator = parameter_declaration.children[1]

                type_specifier = parameter_declarator.children[0]
                identifier = parameter_declarator.children[1]
                arg = Var(
                    name=identifier.text.decode("utf-8"),
                    type=type_specifier.text.decode("utf-8"),
                )
                func.args.append(arg)

        # local vars and func calls
        self.find_func_calls_and_local_vars(statement_list, func)

        self.functions[func.signature] = func
        if func.name not in self.function_groups:
            self.function_groups[func.name] = []
        self.function_groups[func.name].append(func)

    def parse(self, clean_code: str):
        self.clean_code = clean_code

        self.ins: Dict[str, Var] = {}
        self.outs: Dict[str, Var] = {}
        self.attributes: Dict[str, Attribute] = {}
        self.global_vars: Dict[str, Var] = {}
        self.functions: Dict[str, Func] = {}
        self.function_groups: Dict[str, List[Func]] = {}
        self.structs: Dict[str, Struct] = {}
        self.uniforms: Dict[str, Var] = {}
        self.uniform_blocks: Dict[str, Var] = {}
        self.shader_storage_blocks: Dict[str, Var] = {}
        self.geometry_in: str = ""

        self.accum_location = {"in": 0, "out": 0}

        parser = ShaderParser_.glsl_parser()
        tree = parser.parse(bytes(clean_code, sys.getdefaultencoding()))
        root_node = tree.root_node

        for child in root_node.children:
            if child.type == "declaration":
                declaration = child
                if ShaderParser_.is_single_value_declaration(declaration):
                    self.parse_single_value_declaration(declaration)
                elif ShaderParser_.is_block_declaration(
                    declaration
                ):  # block declaration
                    self.parse_block_declaration(declaration)
                elif ShaderParser_.is_only_qualifiers(declaration):  # only qualifiers
                    self.parse_only_qualifiers(declaration)
                elif ShaderParser_.is_struct_declaration(
                    declaration
                ):  # struct definition
                    self.parse_struct(declaration)

            elif child.type == "function_definition":
                function_definition = child
                self.parse_function(function_definition)

        self.resolve()

    def resolve_var(
        self,
        current_var: Var,
        parent: Union[Struct, Func, None] = None,
        mark_as_used: bool = False,
    ):
        if current_var.atoms:
            return

        rear_stack = [SimpleVar(name=current_var.name, type=current_var.type)]
        while rear_stack:
            var = rear_stack.pop()
            current_var.resolved.append(var)
            if var.type in GLInfo.atom_type_names:
                current_var.atoms.append(var)
                continue

            pos_bracket = var.type.find("[")
            if pos_bracket != -1:
                pure_type = var.type[:pos_bracket]
                suffix = var.type[pos_bracket:]
                sub_suffixies = resolve_array(suffix)
                for sub_suffix in sub_suffixies:
                    rear_stack.append(
                        SimpleVar(name=var.name + sub_suffix, type=pure_type)
                    )

                continue

            if var.type in self.structs:
                used_struct = self.structs[var.type]
            elif var.type in ShaderBuiltins.structs:
                used_struct = ShaderBuiltins.structs[var.type]
            else:
                raise TypeError(f"type '{var.type}' is not defined in current shader")

            if parent is not None:
                parent.used_structs.append(used_struct)

            if mark_as_used:
                used_struct.is_used = True

            if used_struct.is_resolved:
                for atom in used_struct.atoms:
                    current_var.atoms.append(
                        SimpleVar(name=var.name + "." + atom.name, type=atom.type)
                    )

                for atom in used_struct.resolved:
                    current_var.resolved.append(
                        SimpleVar(name=var.name + "." + atom.name, type=atom.type)
                    )
            else:
                for member in used_struct.members.values():
                    rear_stack.append(
                        SimpleVar(name=var.name + "." + member.name, type=member.type)
                    )

    def resolve_structs(self):
        for struct in self.structs.values():
            if struct.is_resolved:
                continue

            for member in struct.members.values():
                self.resolve_var(member, struct)

            struct.is_resolved = True

        if not ShaderBuiltins.is_resolved:
            for struct in ShaderBuiltins.structs.values():
                if struct.is_resolved:
                    continue

                for member in struct.members.values():
                    self.resolve_var(member, struct)

                struct.is_resolved = True

    def resolve_vars(self):
        for var in self.uniforms.values():
            self.resolve_var(var, mark_as_used=True)

        for var in self.uniform_blocks.values():
            self.resolve_var(var, mark_as_used=True)

        for var in self.shader_storage_blocks.values():
            self.resolve_var(var, mark_as_used=True)

        for var in self.ins.values():
            if var.name:
                self.resolve_var(var)

        for var in self.outs.values():
            if var.name:
                self.resolve_var(var)

        for var in self.global_vars.values():
            self.resolve_var(var, mark_as_used=True)

        for var in self.hidden_vars.values():
            self.resolve_var(var, mark_as_used=True)

        if not ShaderBuiltins.is_resolved:
            for var in ShaderBuiltins.uniforms.values():
                self.resolve_var(var)

            for ins_info in ShaderBuiltins.ins.values():
                for var in ins_info.values():
                    if var.name:
                        self.resolve_var(var)

            for outs_info in ShaderBuiltins.outs.values():
                for var in outs_info.values():
                    if var.name:
                        self.resolve_var(var)

            for var in ShaderBuiltins.global_vars.values():
                self.resolve_var(var)

            ShaderBuiltins.is_resolved = True

    def find_best_match_function(
        self, func_call: FuncCall, func: Func
    ) -> Union[Func, None]:
        arg_types = []
        for arg in func_call.args:
            type_ = self.analyse_type(arg, func)
            arg_types.append(type_)

        min_distance = None
        best_mached_func = None
        candidate_funcs = []
        for candidate_func in self.candidate_functions(func_call.name):
            if candidate_func.argc != len(arg_types):
                continue

            current_distance = type_list_distance(arg_types, candidate_func.arg_types)
            if isinstance(current_distance, int):
                if current_distance == 0:
                    min_distance = 0
                    best_mached_func = candidate_func
                    break

                if min_distance is None or current_distance < min_distance:
                    min_distance = current_distance
                    best_mached_func = candidate_func
            else:
                if current_distance == "inf":
                    continue

                candidate_funcs.append(candidate_func)

        return best_mached_func if best_mached_func is not None else candidate_funcs

    def resolve_functions(self):
        if not ShaderBuiltins.function_groups:
            for func in ShaderBuiltins.functions.values():
                if func.name not in ShaderBuiltins.function_groups:
                    ShaderBuiltins.function_groups[func.name] = []
                ShaderBuiltins.function_groups[func.name].append(func)

        for func in self.functions.values():
            for arg in func.args:
                self.resolve_var(arg, func)

            for var in func.local_vars:
                self.resolve_var(var, func)

            for key, func_call in func.func_calls.items():
                if isinstance(func_call, Func):
                    continue

                best_match_func = self.find_best_match_function(func_call, func)
                if best_match_func:
                    func.func_calls[key] = best_match_func

    def candidate_functions(self, func_name: str):
        if func_name in self.function_groups:
            yield from self.function_groups[func_name]

        if func_name in ShaderBuiltins.function_groups:
            yield from ShaderBuiltins.function_groups[func_name]

    @staticmethod
    def get_return_type(func_list):
        if isinstance(func_list, Func):
            return func_list.return_type

        if isinstance(func_list, list):
            common_return_type = ""
            for func in func_list:
                if common_return_type == "":
                    common_return_type = func.return_type
                else:
                    if common_return_type != func.return_type:
                        return ""

            return common_return_type

        return ""

    def analyse_type(self, expression: tree_sitter.Node, func: Func) -> str:
        if expression.type == "number_literal":
            text = expression.text.decode("utf-8")
            if (
                expression.next_sibling is not None
                and expression.next_sibling.type == "ERROR"
            ):
                text += expression.next_sibling.text.decode("utf-8")
            number = eval(text)
            return "float" if isinstance(number, float) else "int"
        elif expression.type == "identifier":
            text = expression.text.decode("utf-8")
            for var in func.local_vars:
                if var.name == text:
                    return var.type

            for var in func.args:
                if var.name == text:
                    return var.type

            if text in self.global_vars:
                return self.global_vars[text].type

            if text in self.hidden_vars:
                return self.hidden_vars[text].type

            if text in self.ins:
                return self.ins[text].type

            if text in self.outs:
                return self.outs[text].type

            if text in self.uniforms:
                return self.uniforms[text].type

            if text in self.uniform_blocks:
                return self.uniform_blocks[text].type

            if text in self.shader_storage_blocks:
                return self.shader_storage_blocks[text].type

            if text in ShaderBuiltins.ins[self.shader_type]:
                return ShaderBuiltins.ins[self.shader_type][text].type

            if text in ShaderBuiltins.outs[self.shader_type]:
                return ShaderBuiltins.outs[self.shader_type][text].type

            if text in ShaderBuiltins.uniforms:
                return ShaderBuiltins.uniforms[text].type

            if text in ShaderBuiltins.global_vars:
                return ShaderBuiltins.global_vars[text].type

            return ""
        elif expression.type == "field_expression":
            prefix_expression = expression.children[0]
            suffix_expression = expression.children[2]
            suffix_text = suffix_expression.text.decode("utf-8")
            prefix_type = self.analyse_type(prefix_expression, func)

            if not prefix_type:
                return ""

            if prefix_type in [
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
            ]:
                if len(suffix_text) == 1:
                    if prefix_type[0] == "b":
                        return "bool"
                    elif prefix_type[0] == "i":
                        return "int"
                    elif prefix_type[0] == "u":
                        return "uint"
                    elif prefix_type[0] == "v":
                        return "float"
                    elif prefix_type[0] == "d":
                        return "double"
                else:
                    return prefix_type[:-1] + str(len(suffix_text))

            if prefix_type in self.structs:
                struct = self.structs[prefix_type]
                if suffix_text in struct.members:
                    member = struct.members[suffix_text]
                    return member.type

            if prefix_type in ShaderBuiltins.structs:
                struct = self.structs[prefix_type]
                if suffix_text in struct.members:
                    member = struct.members[suffix_text]
                    return member.type

            return ""
        elif expression.type == "call_expression":
            func_call_name = expression.children[0].text.decode("utf-8")
            if (
                func_call_name in GLInfo.atom_type_names
                or func_call_name in self.structs
                or func_call_name in ShaderBuiltins.structs
            ):
                if func_call_name in self.structs:
                    func.used_structs.append(self.structs[func_call_name])

                return func_call_name

            func_call_key = FuncCall.get_signature(expression)
            func_call = func.func_calls[func_call_key]
            if isinstance(func_call, (Func, list)):
                return ShaderParser_.get_return_type(func_call)

            if isinstance(func_call, FuncCall):
                best_match_func = self.find_best_match_function(func_call, func)
                if best_match_func:
                    func.func_calls[func_call_key] = best_match_func
                return ShaderParser_.get_return_type(best_match_func)

            return ""
        elif expression.type == "binary_expression":
            operant1 = expression.children[0]
            operant1_type = self.analyse_type(operant1, func)
            offset = 0
            if expression.children[1].type == "ERROR":
                offset = 1
            operant2 = expression.children[offset + 2]
            operant2_type = self.analyse_type(operant2, func)

            return greater_type(operant1_type, operant2_type)
        elif expression.type in ["parenthesized_expression", "unary_expression"]:
            content = expression.children[1]
            if content.type == "ERROR":
                content = expression.children[2]
            return self.analyse_type(content, func)
        elif expression.type == "subscript_expression":
            prefix_expression = expression.children[0]
            prefix_type = self.analyse_type(prefix_expression, func)
            result = subscript_type(prefix_type)
            return result
        elif expression.type == "conditional_expression":
            operant1 = expression.children[2]
            operant1_type = self.analyse_type(operant1, func)
            operant2 = expression.children[4]
            operant2_type = self.analyse_type(operant2, func)

            return greater_type(operant1_type, operant2_type)
        elif expression.type in ["false", "true"]:
            return "bool"

        return ""

    def resolve(self):
        self.resolve_structs()
        self.resolve_vars()
        self.resolve_functions()

    def treeshake(self) -> str:
        if "main()" not in self.functions:
            return self.clean_code

        self.functions["main()"].is_used = True

        segments_to_be_removed = []
        for func in self.functions.values():
            if not func.is_used:
                segments_to_be_removed.append((func.start_index, func.end_index))

        for struct in self.structs.values():
            if (
                not struct.is_used
                and struct.start_index != -1
                and struct.end_index != -1
            ):
                segments_to_be_removed.append((struct.start_index, struct.end_index))

        if not segments_to_be_removed:
            return self.clean_code

        segments_to_be_removed.sort(key=lambda x: x[0])
        result = self.clean_code[: segments_to_be_removed[0][0]]
        for i in range(len(segments_to_be_removed)):
            if i + 1 < len(segments_to_be_removed):
                result += self.clean_code[
                    segments_to_be_removed[i][1] : segments_to_be_removed[i + 1][0]
                ]
            else:
                result += self.clean_code[segments_to_be_removed[i][1] :]

        return result
