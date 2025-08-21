from __future__ import annotations

from typing import Optional, Union, TYPE_CHECKING, TypeAlias

from .swizzle import generate_swizzle


if TYPE_CHECKING:
    from .bvec2 import bvec2
    from .bvec3 import bvec3
    from .bvec4 import bvec4
    from .ivec2 import ivec2
    from .ivec3 import ivec3
    from .ivec4 import ivec4
    from .uvec2 import uvec2
    from .uvec3 import uvec3
    from .uvec4 import uvec4
    from .vec3 import vec3
    from .vec4 import vec4

    vec: TypeAlias = Optional[Union[float, bool, int, bvec2, bvec3, bvec4, ivec2, ivec3, ivec4, uvec2, uvec3, uvec4, 'vec2', vec3, vec4]]


class vec2:

    _all_attrs = {
        '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__',
        '__firstlineno__', '__format__', '__ge__', '__getattribute__',
        '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__',
        '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__',
        '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__static_attributes__',
        '__str__', '__subclasshook__', '__weakref__', '_x', '_y'
    }

    _all_swizzle = generate_swizzle("xyrgst", 1, 2)

    def __init__(self, x:vec=None, y:Optional[float]=None):
        self._x:float = 0.0
        self._y:float = 0.0

        if x is None and y is None:
            return
        
        if y is None:
            if isinstance(x, (bool, int, float)):
                self._x:float = float(x)
                self._y:float = float(x)
            elif isinstance(x, (bvec2, bvec3, bvec4, ivec2, ivec3, ivec4, uvec2, uvec3, uvec4, vec2, vec3, vec4)):
                self._x:float = float(x.x)
                self._y:float = float(x.y)
            else:
                raise TypeError(f"not support type {type(x)}")
            
            return
        
        self._x:float = float(x)
        self._y:float = float(y)

    def __getattr__(self, name:str):
        if name in vec2._all_swizzle:
            if len(name) == 

    def __setattr__(self, name, value):
        if name in vec2._all_attrs:
            super().__setattr__(name, value)
            return
        

        