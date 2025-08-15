from typing import Union, List, Dict, Tuple, Optional

import tree_sitter

from ..helper import type_from_str, sizeof


class SimpleVar:

    def __init__(self, name: str = "", type: str = "", location:int = -2, binding_point:int = -2, access_chain: Optional[List[Tuple[str, Union[str,int]]]] = None):
        self.name: str = name
        self.type: str = type
        self.location: int = location
        self.binding_point: int = binding_point
        self.index: int = -2
        self.offset: int = -2
        self.stride: int = -2

        if access_chain is None:
            access_chain = []

        self.access_chain: List[Tuple[str, Union[str,int]]] = access_chain

    def __repr__(self):
        return f"SimpleVar(name='{self.name}', type='{self.type}')"


class Var:

    def __init__(
        self,
        name: str = "",
        type: str = "",
        access_chain: Optional[List[Tuple[str, Union[str,int]]]] = None,
        layout_args: Optional[List[str]] = None,
        layout_kwargs: Optional[Dict[str, str]] = None,
        qualifier: str = "",
        start_index: int = -1,
        end_index: int = -1,
    ):
        self.name: str = name
        self.type: str = type
        self.size: int = -2
        self.index: int = -2
        self._location: int = -2
        self._binding_point: int = -2

        if access_chain is None:
            access_chain = []

        self.access_chain: List[Tuple[str, Union[str,int]]] = access_chain

        self.layout_args: List[str] = [] if layout_args is None else layout_args
        self.layout_kwargs: Dict[str, str] = (
            {} if layout_kwargs is None else layout_kwargs
        )
        self.qualifier: str = qualifier
        self.atoms: List[SimpleVar] = []
        self.resolved: List[SimpleVar] = []
        self.start_index: int = start_index
        self.end_index: int = end_index
        self.is_used: bool = False

        pos_bracket = name.find("[")
        if pos_bracket != -1:
            self.type += name[pos_bracket:]
            self.name = name[:pos_bracket]
            if self.access_chain:
                self.access_chain[-1] = ("getattr", self.name)

    def __repr__(self):
        return f"Var(name='{self.name}', type='{self.type}')"
    
    @property
    def location(self)->int:
        if "location" in self.layout_kwargs:
            return int(self.layout_kwargs["location"])
        else:
            return self._location
        
    @location.setter
    def location(self, location:int):
        self._location = location

    @property
    def binding_point(self)->int:
        if "binding" in self.layout_kwargs:
            return int(self.layout_kwargs["binding"])
        else:
            return self._binding_point
        
    @binding_point.setter
    def binding_point(self, binding_point:int):
        self._binding_point = binding_point


class Attribute:
    
    def __init__(self, var:Optional[Var]=None, name: str = "", type: str = "", location: int = -1):
        if var is None:
            self.name: str = name
            self.location: int = location
            self.type: str = type
        else:
            self.name: str = var.name
            self.location: int = var.location
            self.type: str = var.type

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, type: str):
        self._type = type
        self.python_type = object if type == "" else type_from_str(type)
        self.size: int = 0 if type == "" else sizeof(self.python_type)

    def __repr__(self):
        return f"Attribute(name='{self.name}', type='{self.type}')"


class Struct:

    def __init__(
        self, name: str = "", members=None, start_index: int = -1, end_index: int = -1
    ):
        self.name: str = name
        self.members: Dict[str, Var] = {} if members is None else members
        self.start_index: int = start_index
        self.end_index: int = end_index
        self.used_structs: List[Struct] = []
        self.is_resolved: bool = False
        self._is_used: bool = False

    def _get_atoms(self):
        for member in self.members.values():
            yield from member.atoms

    def _get_resolved(self):
        for member in self.members.values():
            yield from member.resolved

    @property
    def atoms(self):
        return self._get_atoms()

    @property
    def resolved(self):
        return self._get_resolved()

    @property
    def is_used(self):
        return self._is_used

    @is_used.setter
    def is_used(self, flag: bool):
        self._is_used = flag
        for struct in self.used_structs:
            struct.is_used = flag

    def __repr__(self):
        return f"Struct(name='{self.name}')"


class FuncCall:

    def __init__(
        self,
        name: str = "",
        args: Optional[List[tree_sitter.Node]] = None,
        call_expression: Optional[tree_sitter.Node] = None,
    ):
        if call_expression is None:
            self.name: str = name
            self.args: List[tree_sitter.Node] = [] if args is None else args
        else:
            identifier = call_expression.children[0]
            argument_list = call_expression.children[1]
            self.name: str = identifier.text.decode("utf-8")
            self.args: List[tree_sitter.Node] = []
            for arg in argument_list.children:
                if arg.type not in [",", "ERROR", "(", ")"]:
                    self.args.append(arg)

    @property
    def signature(self) -> str:
        return (
            self.name
            + "("
            + ", ".join([arg.text.decode("utf-8") for arg in self.args])
            + ")"
        )

    @staticmethod
    def get_signature(call_expression: tree_sitter.Node):
        identifier = call_expression.children[0]
        argument_list = call_expression.children[1]

        name = identifier.text.decode("utf-8")
        args = []
        for arg in argument_list.children:
            if arg.type not in [",", "ERROR", "(", ")"]:
                args.append(arg)

        return name + "(" + ", ".join([arg.text.decode("utf-8") for arg in args]) + ")"

    def __repr__(self):
        return f"FuncCall(name='{self.name}')"


class Func:
    
    def __init__(
        self,
        return_type: str = "void",
        name: str = "",
        args=None,
        start_index: int = -1,
        end_index: int = -1,
    ):
        self.return_type: str = return_type
        self.name: str = name
        self.args: List[Var] = [] if args is None else args
        self.local_vars: List[Var] = []
        self.used_structs: List[Struct] = []
        self.used_global_vars: List[Var] = []
        self.func_calls: Dict[str, Union[FuncCall, Func]] = {}
        self._is_used: bool = False
        self.start_index: int = start_index
        self.end_index: int = end_index

    @property
    def signature(self):
        arg_types = []
        for arg in self.args:
            arg_types.append(arg.type)

        signature: str = f"{self.name}({', '.join(arg_types)})"
        return signature

    @property
    def argc(self) -> int:
        return len(self.args)

    @property
    def arg_types(self) -> List[str]:
        arg_types: List[str] = []
        for arg in self.args:
            arg_types.append(arg.type)

        return arg_types

    @property
    def is_used(self) -> bool:
        return self._is_used

    @is_used.setter
    def is_used(self, flag: bool):
        self._is_used = flag
        for func_call in self.func_calls.values():
            if isinstance(func_call, Func):
                func_call.is_used = flag
            elif isinstance(func_call, list):
                for sub_func_call in func_call:
                    sub_func_call.is_used = flag

        for struct in self.used_structs:
            struct.is_used = flag

    def __repr__(self):
        return f"{self.return_type} {self.signature}"

    def __bool__(self):
        return True
