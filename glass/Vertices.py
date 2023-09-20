import copy
from OpenGL import GL
import glm
import numpy as np

from .GLConfig import GLConfig
from .VAO import VAO
from .utils import checktype, di
from .AttrList import AttrList
from .GLInfo import GLInfo
from .SameTypeList import SameTypeList

class Vertex(dict):
    _all_attrs = \
    {
        '__class__', '__contains__', '__delattr__', '__delitem__',
        '__dict__', '__dir__', '__doc__', '__eq__', '__format__',
        '__ge__', '__getattribute__', '__getitem__', '__gt__',
        '__hash__', '__init__', '__init_subclass__', '__iter__',
        '__le__', '__len__', '__lt__', '__module__', '__ne__', '__new__',
        '__reduce__', '__reduce_ex__', '__repr__', '__setattr__',
        '__setitem__', '__sizeof__', '__str__', '__subclasshook__',
        '__weakref__', '__getattr__', '__setattr__', '__deepcopy__', '__setstate__',
        'clear', 'copy', 'fromkeys', 'get', 'items', 'keys',
        'pop', 'popitem', 'setdefault', 'update', 'values',
        '_array_index_map', '_add_array_index', "user_data"
    }

    def __init__(self, **kwargs):
        self._array_index_map = {}
        self.user_data = {}
        dict.__init__(self, **kwargs)

    def _add_array_index(self, array, index):
        id_array = id(array)
        if id_array not in self._array_index_map:
            self._array_index_map[id_array] = set()

        self._array_index_map[id_array].add(index)

    def __hash__(self):
        return id(self)

    def __deepcopy__(self, memo):
        vertex = self.__class__()
        for key in self.keys():
            vertex[key] = copy.deepcopy(self[key], memo)
        return vertex

    def __getattr__(self, name):
        if name in Vertex._all_attrs:
            return dict.__getattribute__(self, name)

        return self[name]

    def __setattr__(self, name, value):
        if name in Vertex._all_attrs:
            return dict.__setattr__(self, name, value)

        self[name] = value

    def __setitem__(self, name:str, value):
        dict.__setitem__(self, name, value)

        for id_parent_array, index_set in self._array_index_map.items():
            parent_array = di(id_parent_array)
            if name not in parent_array._attr_list_map:
                parent_array._attr_list_map[name] = AttrList(dtype=type(value))

            for index in index_set:
                parent_array._attr_list_map[name][index] = value

    def __getitem__(self, name:str):
        for id_parent_array, index_set in self._array_index_map.items():
            parent_array = di(id_parent_array)
            if name not in parent_array._attr_list_map:
                value = dict.__getitem__(self, name)
                parent_array._attr_list_map[name] = AttrList(dtype=type(value))
                for index in index_set:
                    parent_array._attr_list_map[name][index] = value

            for index in index_set:
                value = parent_array._attr_list_map[name][index]
                dict.__setitem__(self, name, value)
                return value
            
        return dict.__getitem__(self, name)

dtype_uint64 = np.array([], dtype=np.uint64).dtype
class Vertices:

    element_type = Vertex

    @checktype
    def __init__(self, _list:list=None, draw_type:GLInfo.draw_types=GL.GL_STATIC_DRAW, **kwargs):
        self._attr_list_map = {}
        self._vao_map = {}
        self._index_vertex_map = {}
        self._draw_type = draw_type
        self._tested_front_transparent = False
        self._tested_back_transparent = False
        self._front_has_transparent = False
        self._front_has_opaque = True
        self._back_has_transparent = False
        self._back_has_opaque = True
        
        if _list is not None:
            for value in _list:
                self.append(value)
        else:
            self._attr_list_map = kwargs

    def hasattr(self, attr_name:str):
        return (attr_name in self._attr_list_map)
    
    def reset(self, **kwargs):
        self._attr_list_map = kwargs
        self._vao_map = {}
        self._index_vertex_map = {}
        self._tested_front_transparent = False
        self._tested_back_transparent = False
        self._front_has_transparent = False
        self._front_has_opaque = True
        self._back_has_transparent = False
        self._back_has_opaque = True

    @property
    def draw_type(self):
        return self._draw_type

    @draw_type.setter
    @checktype
    def draw_type(self, value:GLInfo.draw_types):
        self._draw_type = value

    def _first_apply(self, program, instances)->bool:
        current_context = GLConfig.buffered_current_context
        key = (current_context, program, instances)
        if key in self._vao_map or not self:
            return False

        vao = VAO()
        self._vao_map[key] = vao
        return self._apply_increment(instances)

    def _update_VAOs(self, key, attr_list, divisor=None):
        for (context, program, insts), vao in self._vao_map.items():
            if key not in program._attributes_info:
                continue

            location = program._attributes_info[key]["location"]
            if location in vao and not attr_list.is_new_vbo:
                continue

            feed_type = attr_list.dtype
            need_type = program._attributes_info[key]["python_type"]
            if feed_type != need_type:
                if feed_type in GLInfo.primary_types and need_type in GLInfo.primary_types:
                    attr_list.dtype = need_type
                    feed_type = need_type
                elif feed_type == int and need_type == glm.uvec2:
                    attr_list.dtype = np.uint64
                    feed_type = glm.uvec2
                elif feed_type in (np.uint64, dtype_uint64) and need_type == glm.uvec2:
                    feed_type = glm.uvec2
                else:
                    error_message = f"vertex attribute '{key}' need type {need_type}, {feed_type} value were given"
                    raise TypeError(error_message)
            
            vao[location].interp(attr_list._vbo, feed_type, attr_list.stride, 0)
            if divisor is not None:
                vao[location].divisor = divisor

            attr_list.is_new_vbo = False

    def _apply_increment(self, instances)->bool:
        for key, attr_list in self._attr_list_map.items():
            attr_list._apply()
            self._update_VAOs(key, attr_list)

        if instances is None:
            return True
        
        for key, attr_list in instances._attr_list_map.items():
            attr_list._apply()
            self._update_VAOs(key, attr_list, instances.divisor)

        return True

    def _apply(self, program, instances):
        success = False
        current_context = GLConfig.buffered_current_context
        key = (current_context, program, instances)
        if key not in self._vao_map:
            success = self._first_apply(program, instances)
        else:
            success = self._apply_increment(instances)

        if success:
            self._vao_map[key].bind()

    def _process_slice(self, index):
        len_self = len(self)
        start = index.start if index.start is not None else 0
        stop = index.stop if index.stop is not None else len_self
        step = index.step if index.step is not None else 1

        if len_self > 0:
            while start < 0:
                start += len_self

            while stop < 0:
                stop += len_self

        if start < 0: start = 0
        if stop > len_self: stop = len_self

        return start, stop, step

    def __len__(self):        
        for attr_list in self._attr_list_map.values():
            return len(attr_list)
        
        return 0
    
    def __bool__(self):
        for attr_list in self._attr_list_map.values():
            return bool(attr_list)
        
        return False

    def append(self, vertex):
        len_self = len(self)
        for key in set.union(set(vertex.keys()), set(self._attr_list_map.keys())):
            if key not in self._attr_list_map:
                self._attr_list_map[key] = AttrList(dtype=type(vertex[key]))
            if key not in vertex:
                vertex[key] = self._attr_list_map[key].dtype()

            self._attr_list_map[key][len_self] = vertex[key]

        vertex._add_array_index(self, len_self)
        self._index_vertex_map[len_self] = vertex

    def __contains__(self, value:(Vertex,str)):
        if isinstance(value, str):
            return (value in self._attr_list_map)
        else:
            return (self.index(value) != -1)

    def __iter__(self):
        return SameTypeList.iterator(self)
    
    def const_items(self):
        return SameTypeList.const_iterator(self)

    def const_get(self, index:(int,slice)):
        result = None
        if isinstance(index, slice):
            result = []
            start, stop, step = self._process_slice(index)
            for sub_index in range(start, stop, step):
                result.append(self.const_get(sub_index))
        else:
            result = self.__class__.element_type()
            for key, attr_list in self._attr_list_map.items():
                result[key] = attr_list[index]

        return result

    def __getitem__(self, index:(int,slice,str)):
        if isinstance(index, str):
            return self._attr_list_map[index]

        result = None
        if isinstance(index, slice):
            result = []
            start, stop, step = self._process_slice(index)
            for sub_index in range(start, stop, step):
                result.append(self[sub_index])
        else:
            if index in self._index_vertex_map:
                result = self._index_vertex_map[index]
            else:
                result = self.__class__.element_type()
                result._add_array_index(self, index)
                for key, attr_list in self._attr_list_map.items():
                    if index >= len(attr_list):
                        result[key] = attr_list.dtype()
                    else:
                        result[key] = attr_list[index]
                self._index_vertex_map[index] = result

        return result

    def __setitem__(self, index:(int,slice), value:Vertex):
        for key in set.union(set(value.keys()), set(self._attr_list_map.keys())):
            if key not in self._attr_list_map:
                self._attr_list_map[key] = AttrList(dtype=type(value[key]))
            if key not in value:
                if len(self._attr_list_map[key]) == 0:
                    value[key] = self._attr_list_map[key].dtype()
                else:
                    value[key] = copy.deepcopy(self._attr_list_map[key].const_get(-1))

            self._attr_list_map[key][index] = value[key]

        if isinstance(index, int):
            value._add_array_index(self, index)
            self._index_vertex_map[index] = value
        elif isinstance(index, slice):
            start, stop, step = self._process_slice(index)
            for sub_index in range(start, stop, step):
                value._add_array_index(self, sub_index)
                self._index_vertex_map[sub_index] = value
        else:
            raise TypeError(index)

    def __delitem(self, index:int):
        if index in self._index_vertex_map:
            vertex = self._index_vertex_map[index]
            vertex._array_index_map[self].remove(index)
            if not vertex._array_index_map[self]:
                del vertex._array_index_map[self]

            del self._index_vertex_map[index]

        should_update_index = []
        for sub_index, vertex in self._index_vertex_map:
            if sub_index > index:
                should_update_index.append(sub_index)
                vertex._array_index_map[self].remove(sub_index)
                vertex._array_index_map[self].add(sub_index-1)

        for sub_index in should_update_index:
            vertex = self._index_vertex_map[sub_index]
            del self._index_vertex_map[sub_index]
            self._index_vertex_map[sub_index-1] = vertex

    def __delitem__(self, index:(str,int,slice)):
        if isinstance(index, str):
            del self._attr_list_map[index]
            return

        for key in self._attr_list_map:
            del self._attr_list_map[key][index]

        if isinstance(index, int):
            self.__delitem(index)
        else:
            start, stop, step = self._process_slice(index)
            for sub_index in range(start, stop, step):
                self.__delitem(sub_index)

    def clear(self):
        for key in self._attr_list_map:
            self._attr_list_map[key].clear()

        for vertex in self._index_vertex_map:
            del vertex._array_index_map[self]

        self._index_vertex_map.clear()

    def pop(self, index:int)->Vertex:
        vertex = self[index]
        del self[index]

        return vertex
    
    def index(self, vertex:Vertex)->int:
        for key in vertex:
            if key not in self._attr_list_map:
                return -1

        for i in range(len(self)):
            is_equal = True
            for key in vertex:
                if self._attr_list_map[key].const_get(i) != vertex[key]:
                    is_equal = False
                    break
            if is_equal:
                return i
            
        return -1
    
    def remove(self, vertex:Vertex):
        i = self.index(vertex)
        if i == -1:
            raise ValueError(vertex)
        
        del self[i]
    
    def extend(self, _list):
        for vertex in _list:
            self.append(vertex)

    def insert(self, index:int, vertex:Vertex)->None:
        for key in set.union(set(vertex.keys()), set(self._attr_list_map.keys())):
            if key not in vertex:
                vertex[key] = self._attr_list_map[key].dtype()

            vertex_attr = vertex[key]
            if key not in self._attr_list_map:
                self._attr_list_map[key] = AttrList(dtype=type(vertex_attr))
                delta_len = len(self) - len(self._attr_list_map[key])
                self._attr_list_map[key].extend([vertex_attr] * delta_len)
            else:
                self._attr_list_map[key].insert(index, vertex_attr)

        should_update_index = []
        for sub_index, sub_vertex in self._index_vertex_map.items():
            if sub_index >= index:
                should_update_index.append(sub_index)
                sub_vertex._array_index_map[self].remove(sub_index)
                sub_vertex._array_index_map[self].add(sub_index+1)

        for sub_index in should_update_index:
            sub_vertex = self._index_vertex_map[sub_index]
            del self._index_vertex_map[sub_index]
            self._index_vertex_map[sub_index+1] = sub_vertex

        vertex._add_array_index(self, index)
        self._index_vertex_map[index] = self

    def update(self, _list):
        len_list = len(_list)
        len_self = len(self)
        if len_list < len_self:
            del self[len_list:]
        
        for i in range(len_self):
            self[i] = _list[i]

        if len_list > len_self:
            self.extend(_list[len_self:])

    def _test_front_transparent(self):
        if "color" in self._attr_list_map:
            if not self._tested_front_transparent or self._attr_list_map["color"]._should_retest:
                front_alpha = self._attr_list_map["color"].ndarray[:,3]
                self._front_has_transparent = np.any(front_alpha < 1-1E-6)
                self._front_has_opaque = np.any(front_alpha >= 1-1E-6)
                self._attr_list_map["color"]._should_retest = False
        else:
            self._front_has_transparent = False
            self._front_has_opaque = True

        self._tested_front_transparent = True

    def _test_back_transparent(self):
        if "back_color" in self._attr_list_map:
            if not self._tested_back_transparent or self._attr_list_map["back_color"]._should_retest:
                back_alpha = self._attr_list_map["back_color"].ndarray[:,3]
                self._back_has_transparent = np.any(back_alpha < 1-1E-6)
                self._back_has_opaque = np.any(back_alpha >= 1-1E-6)
                self._attr_list_map["back_color"]._should_retest = False
        else:
            self._back_has_transparent = False
            self._back_has_opaque = True

        self._tested_back_transparent = True

    @property
    def front_has_transparent(self):
        self._test_front_transparent()
        return self._front_has_transparent
    
    @property
    def front_has_opaque(self):
        self._test_front_transparent()
        return self._front_has_opaque

    @property
    def back_has_transparent(self):
        self._test_back_transparent()
        return self._back_has_transparent
    
    @property
    def back_has_opaque(self):
        self._test_back_transparent()
        return self._back_has_opaque