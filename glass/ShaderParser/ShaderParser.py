import re
from itertools import product
from OpenGL import GL
from typing import List, Dict, Union, Tuple, Set, Optional

from ..GLInfo import GLInfo
from .ShaderSyntaxTokens import Var, Attribute, Func, FuncCall, Struct
from .ShaderBuiltins import ShaderBuiltins
from .ShaderSyntaxTree import ShaderSyntaxTree
from .minifyc import minifyc, macros_expand_file


class ShaderParser:

    def __init__(self, shader_type):
        self.file_name:str = ""
        self.clean_code:str = ""
        self.compressed_code:str = ""
        self.line_map:Dict[int, Tuple[str, int]] = {}
        self.related_files:Set[str] = set()
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
        self.syntax_tree: ShaderSyntaxTree = ShaderSyntaxTree()

        self.accum_location = {"in": 0, "out": 0}
        self.shader_type = shader_type
        self._is_empty = True

    def clear(self):
        self.file_name:str = ""
        self.clean_code:str = ""
        self.compressed_code:str = ""
        self.line_map.clear()
        self.related_files.clear()
        self.ins.clear()
        self.outs.clear()
        self.attributes.clear()
        self.hidden_vars.clear()
        self.global_vars.clear()
        self.structs.clear()
        self.uniforms.clear()
        self.uniform_blocks.clear()
        self.shader_storage_blocks.clear()
        self.functions.clear()
        self.function_groups.clear()
        self.geometry_in: str = ""
        self.syntax_tree.clear()

        self.accum_location["in"] = 0
        self.accum_location["out"] = 0
        self._is_empty = True

    @staticmethod
    def __parse_field_declaration_list(field_declaration_list: ShaderSyntaxTree.Node) -> Dict[str, Var]:
        members: Dict[str, Var] = {}
        for field_declaration in field_declaration_list.children:
            if field_declaration.type != "field_declaration":
                continue

            var_names = []
            type_identifier = None
            qualifier = ""
            for var_name in field_declaration.children:
                if var_name.type in ["field_identifier", "array_declarator"]:
                    var_names.append(var_name)

            if field_declaration.children[0].type in ["primitive_type", "type_identifier"]:
                type_identifier = field_declaration.children[0]
            elif field_declaration.children[1].type in ["primitive_type", "type_identifier"]:
                type_identifier = field_declaration.children[1]
                qualifier = field_declaration.children[0].type

            type_ = type_identifier.text
            for var_name in var_names:
                var: Var = Var(
                    name=var_name.text,
                    type=type_,
                    is_declare=True,
                    access_chain=[("getattr", var_name.text)],
                    qualifier=qualifier
                )

                members[var.name] = var

        return members

    def __parse_layout(self, layout_qualifiers: ShaderSyntaxTree.Node):
        layout_args: List[str] = []
        layout_kwargs: Dict[str, str] = {}
        for qualifier in layout_qualifiers.children:
            if qualifier.type != "qualifier":
                continue

            if qualifier.child_count == 3:
                layout_kwargs[qualifier.children[0].text] = qualifier.children[2].text
            else:
                layout_args.append(qualifier.text)

        return layout_args, layout_kwargs

    def __parse_single_value_declaration(self, declaration: ShaderSyntaxTree.Node):
        var_names = []
        for var_name in declaration.children:
            if var_name.type in ["identifier", "array_declarator"]:
                var_names.append(var_name)

        layout_qualifiers = None
        qualifier = ""
        type_identifier = None
        if (
            declaration.child_count >= 4
            and declaration.children[0].type == "layout_specification"
            and declaration.children[1].type in ["in", "out", "uniform", "attribute"]
            and declaration.children[2].type in ["type_identifier", "primitive_type"]
            and declaration.children[3].type == "identifier"
        ):
            layout_qualifiers = declaration.children[0].children[1]
            qualifier = declaration.children[1].type
            type_identifier = declaration.children[2]
        elif (
            declaration.child_count >= 3
            and declaration.children[0].type in ["in", "out", "uniform", "attribute"]
            and declaration.children[1].type in ["type_identifier", "primitive_type"]
            and declaration.children[2].type in ["identifier", "array_declarator"]
        ):
            qualifier = declaration.children[0].type
            type_identifier = declaration.children[1]
        elif (
            declaration.child_count >= 2
            and declaration.children[0].type in ["type_identifier", "primitive_type"]
            and declaration.children[1].type in ["identifier", "array_declarator"]
        ):
            type_identifier = declaration.children[0]

        is_attribute = (
            qualifier in ["in", "attribute"]
            and self.shader_type == GL.GL_VERTEX_SHADER
        )

        if layout_qualifiers is not None:
            layout_args, layout_kwargs = (
                self.__parse_layout(layout_qualifiers)
            )
            if qualifier in ["in", "out"] and "location" in layout_kwargs:
                self.accum_location[qualifier] = int(layout_kwargs["location"])

            for var_name in var_names:
                var: Var = Var(
                    name=var_name.text,
                    type=type_identifier.text,
                    is_declare=True,
                    layout_args=layout_args,
                    layout_kwargs=layout_kwargs,
                    qualifier=qualifier,
                )
                if qualifier in ["in", "out"]:
                    var.location = self.accum_location[qualifier]

                if var_name.type == "identifier":
                    if is_attribute:
                        attribute: Attribute = Attribute(var)
                        self.attributes[attribute.name] = attribute
                        self.attributes[attribute.location] = attribute

                    if qualifier in ["in", "out"]:
                        self.accum_location[qualifier] += 1
                elif var_name.type == "array_declarator":
                    pure_name = var_name.children[0].text
                    if is_attribute:
                        length = eval(var_name.children[2].text)
                        for i in range(length):
                            attribute: Attribute = Attribute(
                                name=pure_name + f"[{i}]",
                                type=var.type,
                                location=self.accum_location[qualifier],
                            )
                            self.attributes[attribute.name] = attribute
                            self.attributes[attribute.location] = attribute
                            self.accum_location[qualifier] += 1
                    else:
                        if qualifier in ["in", "out"]:
                            self.accum_location[qualifier] += 1

                if qualifier == "in":
                    self.ins[var.name] = var
                elif qualifier == "out":
                    self.outs[var.name] = var
                elif qualifier == "uniform":
                    self.uniforms[var.name] = var

        else:
            type_ = type_identifier.text
            for var_name in var_names:
                name = var_name.text
                var = Var(name=name, type=type_, is_declare=True)
                if qualifier == "uniform":
                    self.uniforms[var.name] = var
                else:
                    var.start_index = declaration.start_byte
                    var.end_index = declaration.end_byte
                    self.global_vars[var.name] = var

    def __parse_block_declaration(self, declaration: ShaderSyntaxTree.Node):
        block_name = None
        field_declaration_list = None
        var_names = []
        for i in range(declaration.child_count):
            var_name = declaration.children[i]
            if (
                var_name.type == "identifier"
                and i + 1 < declaration.child_count
                and declaration.children[i+1].type == "field_declaration_list"
            ):
                block_name = var_name
                

            if var_name.type == "field_declaration_list":
                field_declaration_list = var_name

            if field_declaration_list is not None and var_name.type in ["identifier", "array_declarator"]:
                var_names.append(var_name)

        layout_args = []
        layout_kwargs = {}
        layout_specification = None
        qualifier = ""
        if declaration.children[0].type == "layout_specification":
            layout_specification = declaration.children[0]
            qualifier = declaration.children[1].type
            layout_args, layout_kwargs = self.__parse_layout(
                layout_specification
            )
            if qualifier in ["in", "out"] and "location" in layout_kwargs:
                self.accum_location[qualifier] = int(layout_kwargs["location"])

        elif declaration.children[0].type in ["in", "out", "uniform", "buffer", "struct"]:
            qualifier = declaration.children[0].type

        type_ = block_name.text
        struct = Struct(
            name=type_,
            members=ShaderParser.__parse_field_declaration_list(
                field_declaration_list
            )
        )
        self.structs[type_] = struct

        for var_name in var_names:
            name = var_name.text
            var = Var(
                name=name,
                type=type_,
                is_declare=True,
                layout_args=layout_args,
                layout_kwargs=layout_kwargs,
                qualifier=qualifier,
            )
            if qualifier in ["in", "out"]:
                var.location = self.accum_location[qualifier]

            if qualifier == "in":
                self.ins[var.name] = var
            elif qualifier == "out":
                self.outs[var.name] = var
            elif qualifier == "uniform":
                self.uniform_blocks[var.name] = var
            elif qualifier == "buffer":
                self.shader_storage_blocks[var.name] = var

            self.accum_location[qualifier] += 1

        if qualifier in ["uniform", "buffer"]:
            var = Var(
                name=type_,
                type=type_,
                is_declare=True,
                layout_args=layout_args,
                layout_kwargs=layout_kwargs,
                qualifier=qualifier,
            )

            if qualifier == "uniform":
                self.uniform_blocks[type_] = var
            elif qualifier == "buffer":
                self.shader_storage_blocks[type_] = var

        if not var_names and qualifier != "struct":
            for member in struct.members.values():
                self.hidden_vars[member.name] = member

    @staticmethod
    def __is_single_value_declaration(declaration):
        return (
            declaration.child_count >= 4
            and declaration.children[0].type == "layout_specification"
            and declaration.children[1].type in ["in", "out", "uniform", "attribute"]
            and declaration.children[2].type in ["type_identifier", "primitive_type"]
            and declaration.children[3].type == "identifier"
        ) or (
            declaration.child_count >= 3
            and declaration.children[0].type in ["in", "out", "uniform", "attribute"]
            and declaration.children[1].type in ["type_identifier", "primitive_type"]
            and declaration.children[2].type in ["identifier", "array_declarator"]
        ) or (
            declaration.child_count >= 2
            and declaration.children[0].type in ["type_identifier", "primitive_type"]
            and declaration.children[1].type in ["identifier", "array_declarator"]
        )

    @staticmethod
    def __is_block_declaration(declaration):
        for i in range(declaration.child_count):
            if (
                declaration.children[i].type == "identifier"
                and i + 1 < declaration.child_count
                and declaration.children[i + 1].type == "field_declaration_list"
            ):
                return True

        return False

    def __parse_struct(self, struct_specifier: ShaderSyntaxTree.Node):
        type_identifier = struct_specifier.children[1]
        field_declaration_list = struct_specifier.children[2]
        struct_name = type_identifier.text
        struct = Struct(
            name=struct_name,
            members=ShaderParser.__parse_field_declaration_list(
                field_declaration_list
            ),
            start_index=struct_specifier.start_byte,
            end_index=struct_specifier.end_byte,
        )
        self.structs[struct_name] = struct

    @staticmethod
    def __get_layout_qualifiers(content):
        if content is None:
            return [], {}

        items = content.split(",")
        args = []
        kwargs = {}
        for item in items:
            item = item.strip()
            if "=" in item:
                key_value = item.split("=")
                key = key_value[0].strip()
                value = key_value[1].strip()
                kwargs[key] = value
            else:
                args.append(item)

        return args, kwargs

    def __parse_geometry_in(self):
        regx = r"^\s*layout\s*\((?P<layout_qualifiers>[^\n]*?)\)\s*in\s*;"

        def append_geometry_in(match):
            layout_qualifiers = match.group("layout_qualifiers")
            args, kwargs = ShaderParser.__get_layout_qualifiers(layout_qualifiers)
            for arg in args:
                if arg in GLInfo.geometry_ins:
                    self.geometry_in = arg
                    return

        re.sub(regx, append_geometry_in, self.clean_code, flags=re.M)

    def __replace_only_in_out(self):
        regx = r"^\s*layout\s*\(([^\n]*?)\)\s*(in|out)\s*;"

        def replacement(match):
            matched_text = match.group(0)
            return ' ' * len(matched_text)
        
        return re.sub(regx, replacement, self.clean_code, flags=re.M)

    def __find_func_calls_and_local_vars(self, node: ShaderSyntaxTree.Node, func: Func):
        if node.type == "call_expression":
            func_call = FuncCall(call_expression=node)
            func.func_calls[func_call.signature] = func_call
        elif node.type == "declaration":
            declaration = node
            type_identifier = None
            for child in declaration.children:
                if child.type in ["type_identifier", "primitive_type"]:
                    type_identifier = child

                if child.type in ["identifier", "array_declarator"]:
                    identifier = child
                    var = Var(
                        name=identifier.text,
                        type=type_identifier.text,
                        is_declare=True,
                    )
                    func.local_vars.append(var)

                if child.type == "init_declarator":
                    identifier = child.children[0]
                    var = Var(
                        name=identifier.text,
                        type=type_identifier.text,
                        is_declare=True
                    )
                    func.local_vars.append(var)

        for child in node.children:
            self.__find_func_calls_and_local_vars(child, func)

    def __parse_function(self, function_definition: ShaderSyntaxTree.Node):
        type_identifier = function_definition.children[0]
        function_declarator = function_definition.children[1]
        statement_list = function_definition.children[2]

        identifier = function_declarator.children[0]
        parameter_list = function_declarator.children[1]

        func = Func(
            return_type=type_identifier.text,
            name=identifier.text,
            start_index=function_definition.start_byte,
            end_index=function_definition.end_byte,
        )

        # args
        for parameter_declaration in parameter_list.children:
            if parameter_declaration.type != "parameter_declaration":
                continue

            type_identifier = None
            identifier = None
            for child in parameter_declaration.children:
                if child.type in ["type_identifier", "primitive_type"]:
                    type_identifier = child

                if child.type in ["identifier", "array_declarator"]:
                    identifier = child
            
            if type_identifier is not None and identifier is not None:
                arg = Var(
                    name=identifier.text,
                    type=type_identifier.text,
                    is_declare=True
                )
                func.args.append(arg)

        # local vars and func calls
        self.__find_func_calls_and_local_vars(statement_list, func)

        self.functions[func.signature] = func
        if func.name not in self.function_groups:
            self.function_groups[func.name] = []
        self.function_groups[func.name].append(func)

    def parse(self, file_name: str, include_paths: Optional[List[str] ] = None, defines: Optional[Dict[str, str] ] = None):
        self.file_name:str = file_name
        (
            self.clean_code,
            self.line_map,
            self.related_files
        ) = macros_expand_file(file_name, include_paths, defines)
        self.compressed_code:str = ""
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

        if self.shader_type == GL.GL_GEOMETRY_SHADER:
            self.__parse_geometry_in()
        clean_code = self.__replace_only_in_out()

        self.syntax_tree.parse(clean_code)
        root_node = self.syntax_tree.root

        for child in root_node.children:
            if child.type == "declaration":
                declaration = child
                if ShaderParser.__is_single_value_declaration(declaration):
                    self.__parse_single_value_declaration(declaration)
                elif ShaderParser.__is_block_declaration(declaration):  # block declaration
                    self.__parse_block_declaration(declaration)

            elif child.type == "function_definition":
                function_definition = child
                self.__parse_function(function_definition)

            elif child.type == "struct_specifier":
                struct_specifier = child
                self.__parse_struct(struct_specifier)

        self.__resolve()
        self._is_empty = False

    @property
    def is_empty(self):
        return self._is_empty

    @staticmethod
    def __resolve_array(arr_def):
        name_match = re.match(r'^(\w+)\[', arr_def)
        arr_name = ""
        if name_match:
            arr_name = name_match.group(1)
        
        dim_matches = re.findall(r'\[(.*?)\]', arr_def)
        if not dim_matches:
            raise ValueError(f"not found array dimension: {arr_def}")
        
        index_ranges = []
        empty_dims = []
        
        for i, dim_content in enumerate(dim_matches):
            if dim_content.strip() in ["", "{0}"]:
                empty_dims.append(i)
                index_ranges.append([None])
            else:
                dim_size = int(dim_content)
                index_ranges.append(range(dim_size))
        
        all_indices = product(*index_ranges)
        
        elements = []
        for indices in all_indices:
            index_parts = []
            access_chain = []
            for i, idx in enumerate(indices):
                if i in empty_dims:
                    index_parts.append("[{0}]")
                    access_chain.append(("getitem", "{0}"))
                else:
                    index_parts.append(f"[{idx}]")
                    access_chain.append(("getitem", idx))
            index_str = ''.join(index_parts)
            elements.append((f"{arr_name}{index_str}", access_chain))
        
        return elements

    def __resolve_var(
        self,
        current_var: Var,
        parent: Optional[Union[Struct, Func]] = None,
        mark_as_used: bool = False,
    ):
        if current_var.is_resolved:
            return
        
        if current_var.type in GLInfo.atom_types:
            current_var.atoms.append(current_var.simple_var)
            current_var.is_resolved = True
            return

        pos_bracket = current_var.type.find("[")
        if pos_bracket != -1:
            pure_type = current_var.type[:pos_bracket]
            suffix = current_var.type[pos_bracket:]
            elements = ShaderParser.__resolve_array(suffix)
            for element in elements:
                child_var:Var = Var(
                    name=current_var.name + element[0],
                    type=pure_type,
                    is_declare=False,
                    access_chain=current_var.access_chain + element[1]
                )
                current_var.children[child_var.name] = child_var
                self.__resolve_var(child_var)

            current_var.collect_descendants()
            current_var.is_resolved = True
            return

        if current_var.type in self.structs:
            used_struct = self.structs[current_var.type]
        elif current_var.type in ShaderBuiltins.structs:
            used_struct = ShaderBuiltins.structs[current_var.type]
        else:
            raise TypeError(f"type '{current_var.type}' is not defined in current shader")

        if parent is not None:
            parent.used_structs.append(used_struct)

        if mark_as_used:
            used_struct.is_used = True
        
        for member in used_struct.members.values():
            child_var = Var(
                name=current_var.name + "." + member.name,
                type=member.type,
                is_declare=False,
                access_chain=current_var.access_chain + [("getattr", member.name)]
            )
            current_var.children[child_var.name] = child_var
            self.__resolve_var(child_var)

        current_var.collect_descendants()
        current_var.is_resolved = True

    def __resolve_structs(self):
        for struct in self.structs.values():
            if struct.is_resolved:
                continue

            for member in struct.members.values():
                self.__resolve_var(member, struct)

            struct.is_resolved = True

        if not ShaderBuiltins.is_resolved:
            for struct in ShaderBuiltins.structs.values():
                if struct.is_resolved:
                    continue

                for member in struct.members.values():
                    self.__resolve_var(member, struct)

                struct.is_resolved = True

    def __resolve_vars(self):
        for var in self.uniforms.values():
            self.__resolve_var(var, mark_as_used=True)

        for var in self.uniform_blocks.values():
            self.__resolve_var(var, mark_as_used=True)

        for var in self.shader_storage_blocks.values():
            self.__resolve_var(var, mark_as_used=True)

        for var in self.ins.values():
            if var.name:
                self.__resolve_var(var)

        for var in self.outs.values():
            if var.name:
                self.__resolve_var(var)

        for var in self.global_vars.values():
            self.__resolve_var(var, mark_as_used=True)

        for var in self.hidden_vars.values():
            self.__resolve_var(var, mark_as_used=True)

        if not ShaderBuiltins.is_resolved:
            for var in ShaderBuiltins.uniforms.values():
                self.__resolve_var(var)

            for ins_info in ShaderBuiltins.ins.values():
                for var in ins_info.values():
                    if var.name:
                        self.__resolve_var(var)

            for outs_info in ShaderBuiltins.outs.values():
                for var in outs_info.values():
                    if var.name:
                        self.__resolve_var(var)

            for var in ShaderBuiltins.global_vars.values():
                self.__resolve_var(var)

            ShaderBuiltins.is_resolved = True

    def __find_best_match_function(self, func_call: FuncCall, func: Func) -> Union[Func, None]:
        arg_types = []
        for arg in func_call.args:
            type_ = self.__analyse_type(arg, func)
            arg_types.append(type_)

        min_distance = None
        best_mached_func = None
        candidate_funcs = []
        for candidate_func in self.__candidate_functions(func_call.name):
            if candidate_func.argc != len(arg_types):
                continue

            current_distance = ShaderParser.__type_list_distance(arg_types, candidate_func.arg_types)
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

        if best_mached_func is not None:
            return best_mached_func
        else:
            return candidate_funcs

    def __resolve_functions(self):
        if not ShaderBuiltins.function_groups:
            for func in ShaderBuiltins.functions.values():
                if func.name not in ShaderBuiltins.function_groups:
                    ShaderBuiltins.function_groups[func.name] = []
                ShaderBuiltins.function_groups[func.name].append(func)

        for func in self.functions.values():
            for arg in func.args:
                self.__resolve_var(arg, func)

            for var in func.local_vars:
                self.__resolve_var(var, func)

            for key, func_call in func.func_calls.items():
                if isinstance(func_call, Func):
                    continue

                best_match_func = self.__find_best_match_function(func_call, func)
                if best_match_func:
                    func.func_calls[key] = best_match_func

    def __candidate_functions(self, func_name: str):
        if func_name in self.function_groups:
            yield from self.function_groups[func_name]

        if func_name in ShaderBuiltins.function_groups:
            yield from ShaderBuiltins.function_groups[func_name]

    @staticmethod
    def __get_return_type(func_list):
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

    def __analyse_type(self, expression: ShaderSyntaxTree.Node, func: Func) -> str:
        if expression.type == "number_literal":
            text = expression.text
            if (
                expression.next_sibling is not None
                and expression.next_sibling.type == "ERROR"
            ):
                text += expression.next_sibling.text
            number = eval(text)
            return "float" if isinstance(number, float) else "int"
        elif expression.type == "identifier":
            text = expression.text
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
            suffix_text = suffix_expression.text
            prefix_type = self.__analyse_type(prefix_expression, func)

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
                struct = ShaderBuiltins.structs[prefix_type]
                if suffix_text in struct.members:
                    member = struct.members[suffix_text]
                    return member.type

            return ""
        elif expression.type == "call_expression":
            func_call_name = expression.children[0].text
            if (
                func_call_name in GLInfo.atom_types
                or func_call_name in self.structs
                or func_call_name in ShaderBuiltins.structs
            ):
                if func_call_name in self.structs:
                    func.used_structs.append(self.structs[func_call_name])

                return func_call_name

            func_call_key = FuncCall.get_signature(expression)
            func_call = func.func_calls[func_call_key]
            if isinstance(func_call, (Func, list)):
                return ShaderParser.__get_return_type(func_call)

            if isinstance(func_call, FuncCall):
                best_match_func = self.__find_best_match_function(func_call, func)
                if best_match_func:
                    func.func_calls[func_call_key] = best_match_func
                return ShaderParser.__get_return_type(best_match_func)

            return ""
        elif expression.type == "binary_expression":
            operant1 = expression.children[0]
            operant1_type = self.__analyse_type(operant1, func)
            offset = 0
            if expression.children[1].type == "ERROR":
                offset = 1
            operant2 = expression.children[offset + 2]
            operant2_type = self.__analyse_type(operant2, func)

            return ShaderParser.__greater_type(operant1_type, operant2_type)
        elif expression.type in ["parenthesized_expression", "unary_expression"]:
            content = expression.children[1]
            if content.type == "ERROR":
                content = expression.children[2]
            return self.__analyse_type(content, func)
        elif expression.type == "subscript_expression":
            prefix_expression = expression.children[0]
            prefix_type = self.__analyse_type(prefix_expression, func)
            result = ShaderParser.__subtype(prefix_type)
            return result
        elif expression.type == "conditional_expression":
            operant1 = expression.children[2]
            operant1_type = self.__analyse_type(operant1, func)
            operant2 = expression.children[4]
            operant2_type = self.__analyse_type(operant2, func)

            return ShaderParser.__greater_type(operant1_type, operant2_type)
        elif expression.type in ["false", "true"]:
            return "bool"

        return ""

    def __resolve(self):
        self.__resolve_structs()
        self.__resolve_vars()
        self.__resolve_functions()

    def __treeshake(self) -> str:
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

    def compress(self)->str:
        if self.compressed_code:
            return self.compressed_code

        self.compressed_code:str = minifyc(self.__treeshake())
        return self.compressed_code

    @staticmethod
    def array_basename(name: str)->str:
        pos_bracket = name.rfind("[")
        if pos_bracket == -1:
            return name
        else:
            return name[:pos_bracket].strip(" \t")
        
    @staticmethod
    def array_index(name: str)->int:
        pos_bracket = name.rfind("[")
        if pos_bracket == -1:
            return 0
        else:
            return int(name[pos_bracket+1:-1].strip(" \t"))

    @staticmethod
    def __type_distance(type1: str, type2: str):
        if type1 == type2:
            return 0

        if type1 == "" or type2 == "":
            return "unknown"

        def type_index(type_, types):
            for i, target_type in enumerate(types):
                if isinstance(target_type, tuple):
                    if type_ in target_type:
                        return i
                else:
                    if type_ == target_type:
                        return i
            return -1

        all_types = [
            GLInfo.basic_types,
            GLInfo.gvec2_types,
            GLInfo.gvec3_types,
            GLInfo.gvec4_types,
            GLInfo.gmat2x2_types,
            GLInfo.gmat3x2_types,
            GLInfo.gmat3x3_types,
            GLInfo.gmat3x4_types,
            GLInfo.gmat4x2_types,
            GLInfo.gmat4x3_types,
            GLInfo.gmat4x4_types,
        ]

        for target_types in all_types:
            type1_index = type_index(type1, target_types)
            type2_index = type_index(type2, target_types)
            if type1_index != -1 and type2_index != -1:
                return abs(type1_index - type2_index)

        return "inf"

    @staticmethod
    def __type_list_distance(type_list1, type_list2):
        for type1, type2 in zip(type_list1, type_list2):
            current_distance = ShaderParser.__type_distance(type1, type2)
            if current_distance == "inf":
                return "inf"

        full_distance = 0
        for type1, type2 in zip(type_list1, type_list2):
            current_distance = ShaderParser.__type_distance(type1, type2)
            if current_distance == "unknown":
                return "unknown"
            full_distance += current_distance

        return full_distance

    @staticmethod
    def __nitems(element_type):
        str_element_type = str(element_type)
        if "vec2" in str_element_type:
            return 2
        elif "vec3" in str_element_type:
            return 3
        elif "vec4" in str_element_type or "mat2x2" in str_element_type:
            return 4
        elif "mat2x3" in str_element_type or "mat3x2" in str_element_type:
            return 6
        elif "mat3x3" in str_element_type:
            return 9
        elif "mat2x4" in str_element_type or "mat4x2" in str_element_type:
            return 8
        elif "mat3x4" in str_element_type or "mat4x3" in str_element_type:
            return 12
        elif "mat4x4" in str_element_type:
            return 16
        else:
            return 1

    @staticmethod
    def __greater_type(type1: str, type2: str):
        if type1 == "":
            return type2

        if type2 == "":
            return type1

        if type1 == type2:
            return type1

        type1_struct = GLInfo.atom_type_map[type1][2]
        type1_dtype = GLInfo.atom_type_map[type1][1]
        type1_index = GLInfo.basic_types.index(type1_dtype)
        type1_nitems = ShaderParser.__nitems(type1)

        type2_struct = GLInfo.atom_type_map[type2][2]
        type2_dtype = GLInfo.atom_type_map[type2][1]
        type2_index = GLInfo.basic_types.index(type2_dtype)
        type2_nitems = ShaderParser.__nitems(type2)

        result_dtype = type1_dtype if type1_index >= type2_index else type2_dtype
        result_struct = type1_struct if type1_nitems >= type2_nitems else type2_struct
        if not result_struct:
            return result_dtype

        if result_dtype == "bool":
            return "b" + result_struct
        elif result_dtype == "int":
            return "i" + result_struct
        elif result_dtype == "uint":
            return "u" + result_struct
        elif result_dtype == "float":
            return result_struct
        elif result_dtype == "double":
            return "d" + result_struct

    @staticmethod
    def __subtype(type_str: str):
        pos_bracket = type_str.rfind("[")
        if pos_bracket != -1:
            return type_str[:pos_bracket]

        if type_str in ["bvec2", "bvec3", "bvec4"]:
            return "bool"

        if type_str in ["ivec2", "ivec3", "ivec4"]:
            return "int"

        if type_str in ["uvec2", "uvec3", "uvec4"]:
            return "uint"

        if type_str in ["vec2", "vec3", "vec4"]:
            return "float"

        if type_str in ["dvec2", "dvec3", "dvec4"]:
            return "double"

        if type_str in ["mat2", "mat2x2", "mat2x3", "mat2x4"]:
            return "vec2"

        if type_str in ["mat3", "mat3x2", "mat3x3", "mat3x4"]:
            return "vec3"

        if type_str in ["mat4", "mat4x2", "mat4x3", "mat4x4"]:
            return "vec4"

        if type_str in ["dmat2", "dmat2x2", "dmat2x3", "dmat2x4"]:
            return "dvec2"

        if type_str in ["dmat3", "dmat3x2", "dmat3x3", "dmat3x4"]:
            return "dvec3"

        if type_str in ["dmat4", "dmat4x2", "dmat4x3", "dmat4x4"]:
            return "dvec4"

        return ""
    
    @staticmethod
    def access(var, subscript_chain:List[Tuple[str, Union[str,int]]], feed_index: int = None):
        for operator, operant in subscript_chain:
            if operator == "getattr":
                var = getattr(var, operant)
            else:
                used_index = operant if operant != "{0}" else feed_index
                var = var[used_index]

        return var

    @staticmethod
    def access_set(
        var, subscript_chain:List[Tuple[str, Union[str,int]]], value, feed_index: int = None, compare_before_set: bool = True
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