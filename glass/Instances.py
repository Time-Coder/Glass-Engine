from .Vertices import Vertex, Vertices
from .GLInfo import GLInfo
from .utils import checktype

from OpenGL import GL


class Instance(Vertex):
    def __init__(self, **kwargs):
        Vertex.__init__(self, **kwargs)


class Instances(Vertices):

    element_type = Instance

    @checktype
    def __init__(self, values=None, draw_type: GLInfo.draw_types = GL.GL_STATIC_DRAW):
        self._path_index_map = {}

        if isinstance(values, (list, type(None))):
            Vertices.__init__(self, values=values, draw_type=draw_type)
        else:
            Vertices.__init__(self, draw_type=draw_type)
            self.update(values)

    def __hash__(self):
        return id(self)

    def __eq__(self, other):
        return id(self) == id(other)

    def __setitem__(self, index: (int, slice, str), instance):
        if isinstance(index, str):
            path = index
            if path in self._path_index_map:
                index = self._path_index_map[path]
                Vertices.__setitem__(self, index, instance)
            else:
                self._path_index_map[path] = len(self)
                self.append(instance)
        else:
            Vertices.__setitem__(self, index, instance)

    def __getitem__(self, index: (int, slice, str)):
        if isinstance(index, str):
            path = index
            if path in self._path_index_map:
                index = self._path_index_map[path]
                return Vertices.__getitem__(self, index)
            else:
                raise KeyError(path)
        else:
            return Vertices.__getitem__(self, index)

    def __delitem__(self, index: (int, str, slice)):
        if isinstance(index, str):
            path = index
            if path in self._path_index_map:
                index = self._path_index_map[path]
                Vertices.__delitem__(self, index)
                for p in self._path_index_map:
                    i = self._path_index_map[p]
                    if i > index:
                        self._path_index_map[p] = i - 1
            else:
                raise KeyError(path)
        elif isinstance(index, int):
            Vertices.__delitem__(self, index)
            for p in self._path_index_map:
                i = self._path_index_map[p]
                if i > index:
                    self._path_index_map[p] = i - 1
        elif isinstance(index, slice):
            start, stop, step = self._process_slice(index)
            for i in range(start, stop, step):
                del self[i]

    def pop(self, index: (int, str, slice)):
        if isinstance(index, str):
            path = index
            if path in self._path_index_map:
                index = self._path_index_map[path]
                value = Vertices.pop(self, index)
                for p in self._path_index_map:
                    i = self._path_index_map[p]
                    if i > index:
                        self._path_index_map[p] = i - 1
                return value
            else:
                raise KeyError(path)
        else:
            return Vertices.pop(self, index)

    def insert(self, index: int, value):
        Vertices.insert(self, index, value)
        for p in self._path_index_map:
            i = self._path_index_map[p]
            if i >= index:
                self._path_index_map[p] = i + 1

    def clear(self):
        Vertices.clear(self)
        self._path_index_map.clear()

    def update(self, values):
        if isinstance(values, list):
            Vertices.update(self, values)
        else:
            for key in values.keys():
                value = values[key]
                if key in self:
                    self[key].update(value)
                else:
                    self[key] = value

    def __contains__(self, key) -> bool:
        if isinstance(key, str):
            return key in self._path_index_map
        else:
            return Vertices.__contains__(self, key)

    def keys(self):
        return self._path_index_map.keys()

    @property
    def divisor(self):
        if not hasattr(self, "_divisor"):
            return 1
        else:
            return self._divisor

    @divisor.setter
    @checktype
    def divisor(self, divisor: int):
        if divisor <= 0:
            raise ValueError(f"divisor must be greater than 0, {divisor} were given")
        self._divisor = divisor
