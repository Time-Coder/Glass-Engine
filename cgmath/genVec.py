from __future__ import annotations

from typing import Set, List, Dict, Union, Any, Optional, Tuple, TYPE_CHECKING
from .helper import generate_getter_swizzles, generate_setter_swizzles, is_number
from .genType import genType, MathForm
from abc import abstractmethod

if TYPE_CHECKING:
    from .genMat import genMat


class genVec(genType):

    _attr_index_map:Dict[str, int] = {
        'x': 0,
        'y': 1,
        'z': 2,
        'w': 3,
        'r': 0,
        'g': 1,
        'b': 2,
        'a': 3,
        's': 0,
        't': 1,
        'p': 2,
        'q': 3
    }

    _all_attrs:Set[str] = {
        '_data', '_related_mat', '_mat_start_index', '_on_changed'
    }
    _all_getter_swizzles:Set[str] = set()
    _all_setter_swizzles:Set[str] = set()
    __all_total_swizzles:Set[str] = set()
    __namespaces:List[str] = ['xyzw', 'rgba', 'stpq']

    def __init__(self, *args):
        genType.__init__(self)
        self._related_mat:Optional[genMat] = None
        self._mat_start_index:int = -1

        i: int = 0
        n_data: int = len(self._data)
        n_args: int = len(args)

        if n_args == 0:
            return
        
        if n_args == 1:
            arg = args[0]
            if is_number(arg):
                for i in range(n_data):
                    self._data[i] = arg
                return
        
        for i_arg, arg in enumerate(args):
            if is_number(arg):
                self._data[i] = arg

                i += 1
                if i == n_data:
                    if n_args != 1 and i_arg != n_args - 1:
                        raise ValueError(f"invalid arguments for {self.__class__.__name__}()")
                    
                    return

            elif isinstance(arg, genVec):
                sub_n_arg: int = len(arg._data)
                for sub_i_arg, value in enumerate(arg._data):
                    self._data[i] = value

                    i += 1
                    if i == n_data:
                        if n_args != 1 and (i_arg != n_args - 1 or sub_i_arg != sub_n_arg - 1):
                            raise ValueError(f"invalid arguments for {self.__class__.__name__}()")
                        
                        return
            
            else:
                raise TypeError(f"invalid argument type(s) for {self.__class__.__name__}()")
            
        raise ValueError(f"invalid arguments for {self.__class__.__name__}()")
    
    @property
    def math_form(self)->MathForm:
        return MathForm.Vec

    @abstractmethod
    def __len__(self)->int:
        pass

    @property
    def shape(self)->Tuple[int]:
        return (len(self),)
    
    @staticmethod
    def vec_type(dtype:type, size:int)->type:
        return genType.gen_type(MathForm.Vec, dtype, (size,))

    def _update_data(self, indices:Optional[List[int]] = None):
        genType._update_data(self, indices)

        if self._related_mat is not None:
            if indices is None:
                indices = range(len(self))

            for index in indices:
                self._related_mat._data[self._mat_start_index + index] = self._data[index]

            self._related_mat._call_on_changed()

    def __getattr__(self, name:str)->Union[float,bool,int,genVec]:
        if name not in self.__getter_swizzles():
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
        
        vec_type = self.vec_type(self.dtype, len(name))
        return vec_type(*(self._data[self._attr_index_map[ch]] for ch in name))

    def __setattr__(self, name:str, value:Union[float,bool,int,genVec]):
        if name in self._all_attrs:
            super().__setattr__(name, value)
            return
        
        if name not in self.__setter_swizzles():
            if name in self.__getter_swizzles():
                raise AttributeError(f"property '{name}' of '{self.__class__.__name__}' object has no setter")
            
            if name in self.__total_swizzles():
                raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
            
            super().__setattr__(name, value)
            return

        update_indices:List[int] = []
        value_is_vec:bool = (isinstance(value, genVec) and len(value) == len(name))
        if not value_is_vec and not is_number(value):
            raise TypeError(f"can not set '{value.__class__.__name__}' object to property '{name}' of '{self.__class__.__name__}' object")
        
        for i, ch in enumerate(name):
            index:int = self._attr_index_map[ch]
            self._data[index] = value[i] if value_is_vec else value
            update_indices.append(index)
        self._update_data(update_indices)
    
    def __getitem__(self, index:Union[int,slice])->Union[float,int,bool,genVec]:
        result = self._data[index]
        if isinstance(result, list):
            if len(result) == 1:
                return result[0]
            else:
                result_type = self.vec_type(self.dtype, len(result))
                return result_type(*result)
        else:
            return result
    
    def __setitem__(self, index:Union[int,slice], value:Union[float,int,bool,genVec])->None:
        if isinstance(index, int):
            self._data[index] = value
            self._update_data([index])
            return

        start, stop, step = index.indices(len(self))
        value_is_vec:bool = (not is_number(value))
        update_indices:List[int] = []
        for i in range(start, stop, step):
            self._data[i] = value[i] if value_is_vec else value
            update_indices.append(i)

        self._update_data(update_indices)
        
    def value_ptr(self):
        return self._data
        
    def __getter_swizzles(self):
        if not self.__class__._all_getter_swizzles:
            n:int = len(self)
            self.__class__._all_getter_swizzles = set(
                generate_getter_swizzles(
                    namespace[:n] for namespace in genVec.__namespaces
                )
            )

        return self.__class__._all_getter_swizzles
    
    def __setter_swizzles(self):
        if not self.__class__._all_setter_swizzles:
            n:int = len(self)
            self.__class__._all_setter_swizzles = set(
                generate_setter_swizzles(
                    namespace[:n] for namespace in genVec.__namespaces
                )
            )

        return self.__class__._all_setter_swizzles
    
    @staticmethod
    def __total_swizzles():
        if not genVec.__all_total_swizzles:
            genVec.__all_total_swizzles = set(generate_getter_swizzles(genVec.__namespaces))

        return genVec.__all_total_swizzles

    def __iter__(self):
        return iter(self._data)
    
    def __contains__(self, value:Any)->bool:
        return (value in self._data)
