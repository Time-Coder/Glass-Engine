import copy
import numpy as np
import glm

from .utils import capacity_of
from .helper import nitems
from .GlassConfig import GlassConfig
from .GLInfo import GLInfo


class SameTypeList:

    class iterator:
        def __init__(self, _list):
            self.__list = _list
            self.__len_list = len(_list)
            self.__current_index = 0

        def __next__(self):
            if self.__current_index >= self.__len_list:
                raise StopIteration()

            value = self.__list[self.__current_index]
            self.__current_index += 1

            return value

        def __iter__(self):
            self.__current_index = 0
            return self

    class const_iterator:
        def __init__(self, _list):
            self.__list = _list
            self.__len_list = len(_list)
            self.__current_index = 0

        def __next__(self):
            if self.__current_index >= self.__len_list:
                raise StopIteration()

            value = self.__list.const_get(self.__current_index)
            self.__current_index += 1

            return value

        def __iter__(self):
            self.__current_index = 0
            return self

    def __init__(self, _list: (list, np.ndarray) = None, dtype: type = None):
        self.reset(_list, dtype)

    def reset(self, _list: (list, np.ndarray) = None, dtype: type = None):
        if _list is None:
            _list = []

        self._list = _list
        self._list_ndarray = None
        self._list_dirty = True
        self._should_retest = True
        self._data_list = []

        str_dtype = str(dtype)
        if str_dtype == "callback_vec3":
            dtype = glm.vec3
        elif str_dtype == "callback_vec4":
            dtype = glm.vec4
        elif str_dtype == "callback_quat":
            dtype = glm.quat

        self._dtype = dtype
        if dtype is None and _list:
            self._dtype = type(_list[0])

        self._increment = None
        self._checked_out_items = {}

    @property
    def ndarray(self) -> np.ndarray:
        if self._list_dirty:
            if isinstance(self._list, np.ndarray):
                self._list_ndarray = self._list
            else:
                if self and "sampler" in type(self._list[0]).__name__:
                    len_list = len(self._list)
                    self._data_list.extend([0] * (len_list - len(self._data_list)))
                    del self._data_list[len_list:]
                    for i in range(len_list):
                        self._data_list[i] = self._list[i].handle

                    self._list_ndarray = np.array(self._data_list, dtype=np.uint64)
                else:
                    if self._dtype is None:
                        self._list_ndarray = np.array(self._list)
                    else:
                        np_dtype = self._dtype
                        if np_dtype in GLInfo.np_dtype_map:
                            np_dtype = GLInfo.np_dtype_map[np_dtype]
                        self._list_ndarray = np.array(self._list, dtype=np_dtype)

            self._list_dirty = False

        return self._list_ndarray

    @ndarray.setter
    def ndarray(self, array: np.ndarray):
        self._list_dirty = False
        self._should_retest = True
        self._list_ndarray = array
        self._list = array

        if self._increment is not None:
            _list = list(map(lambda x: self._dtype(*x), self._list))
            self._increment.reset(_list)

    @classmethod
    def frombuffer(cls, buffer: (bytes, bytearray), dtype):
        np_dtype = GLInfo.np_dtype_map[dtype]
        np_array = np.frombuffer(buffer, dtype=np_dtype).reshape((-1, nitems(dtype)))
        result = cls(np_array, dtype=dtype)
        return result

    @classmethod
    def fromarray(cls, np_array: np.ndarray, dtype):
        np_array = np_array.reshape((-1, nitems(dtype)))
        result = cls(np_array, dtype=dtype)
        return result

    def _check_type(self, value):
        if not self:
            return

        if type(value) != self._dtype and type(value) != type(self._list[0]):
            raise TypeError(
                f"{self._dtype} value expected, {type(value)} value was given"
            )

    def _change_to_list(self):
        if not isinstance(self._list, list):
            self._list = list(map(lambda x: self._dtype(*x), self._list))

    def append(self, value):
        self._change_to_list()
        self._check_in_items()

        if GlassConfig.debug:
            self._check_type(value)

        self._list.append(value)

        if self._increment is not None:
            self._increment.append(value)

        self._list_dirty = True
        self._should_retest = True

    def extend(self, _list):
        self._change_to_list()
        self._check_in_items()

        if GlassConfig.debug:
            for value in _list:
                self._check_type(value)

        self._list.extend(_list)

        if self._increment is not None:
            self._increment.append(_list)

        self._list_dirty = True
        self._should_retest = True

    def insert(self, index, value):
        self._change_to_list()
        self._check_in_items()

        if GlassConfig.debug:
            self._check_type(value)

        self._list.insert(index, value)

        if self._increment is not None:
            self._increment.insert(index, value)

        self._list_dirty = True
        self._should_retest = True

    def remove(self, value):
        self._change_to_list()
        self._check_in_items()

        index = self.index(value)

        self._list.remove(value)

        if self._increment is not None:
            self._increment.delete(index)

        self._list_dirty = True
        self._should_retest = True

    def pop(self, index: int):
        self._change_to_list()
        self._check_in_items()

        value = self._list.pop(index)

        if self._increment is not None:
            self._increment.delete(index)

        self._list_dirty = True
        self._should_retest = True

        return value

    def clear(self):
        self._check_in_items()
        self._list = []

        if self._increment is not None:
            self._increment.clear()

        self._list_dirty = True
        self._should_retest = True

    def update(self, _list):
        len_list = len(_list)
        len_self = len(self._list)
        if len_list < len_self:
            del self[len_list:]

        for i in range(len_self):
            self[i] = _list[i]

        if len_list > len_self:
            self.extend(_list[len_self:])

        self._list_dirty = True
        self._should_retest = True

    def __len__(self):
        if isinstance(self._list, np.ndarray):
            return self._list.shape[0]
        else:
            return len(self._list)

    def __bool__(self):
        return len(self._list) > 0

    def __setitem__(self, index, value):
        self._check_in_items()

        if isinstance(index, int):
            len_list = len(self._list)
            if index >= len_list:
                self.extend([value] * (index + 1 - len_list))
                self._list_dirty = True
                self._should_retest = True
                return True

            if self.const_get(index) == value:
                return False

        if GlassConfig.debug:
            if (
                isinstance(index, slice)
                and type(value) != type(self._list[0])
                and type(value) != self._dtype
            ):
                for subvalue in value:
                    self._check_type(subvalue)
            else:
                self._check_type(value)

        self._list[index] = value
        if self._increment is not None:
            self._increment.update(index, value)

        self._list_dirty = True
        self._should_retest = True
        return True

    def __getitem__(self, index: (int, slice)):
        if self._increment is not None:
            if isinstance(index, slice):
                start, stop, step = self.__process_slice(index)
                for sub_index in range(start, stop, step):
                    if sub_index not in self._checked_out_items:
                        self._checked_out_items[sub_index] = copy.deepcopy(
                            self.const_get(sub_index)
                        )
            else:
                if index not in self._checked_out_items:
                    self._checked_out_items[index] = copy.deepcopy(
                        self.const_get(index)
                    )

        self._list_dirty = True
        self._should_retest = True
        return self.const_get(index)

    def const_get(self, index):
        result = self._list[index]
        if not isinstance(self._list, list):
            result = self._dtype(*result)
        return result

    def const_items(self):
        return SameTypeList.const_iterator(self)

    def __iter__(self):
        return SameTypeList.iterator(self)

    def _check_in_items(self):
        if self._increment is None or not self._checked_out_items:
            return

        for index, value in self._checked_out_items.items():
            new_value = self.const_get(index)
            if new_value != value:
                self._increment.update(index, new_value)

        self._checked_out_items.clear()

    def __delitem__(self, index: (int, slice)):
        self._change_to_list()
        self._check_in_items()
        del self._list[index]

        if self._increment is not None:
            if isinstance(index, slice):
                start, stop, step = self.__process_slice(index)
                if (
                    start >= len(self._list)
                    or step == 0
                    or start == stop
                    or (step > 0 and stop < step)
                    or (step < 0 and stop > step)
                ):
                    return

                if step == 1:
                    self._increment.delete(start, stop)
                else:
                    for i in range(start, stop, step):
                        self._increment.delete(i)
            else:
                self._increment.delete(index)

        self._list_dirty = True
        self._should_retest = True

    def __process_slice(self, index):
        len_self = len(self._list)
        start = index.start if index.start is not None else 0
        stop = index.stop if index.stop is not None else len_self
        step = index.step if index.step is not None else 1

        if len_self > 0:
            while start < 0:
                start += len_self

            while stop < 0:
                stop += len_self

        if start < 0:
            start = 0
        if stop > len_self:
            stop = len_self

        return start, stop, step

    @property
    def increment(self):
        return self._increment

    @property
    def capacity(self):
        return capacity_of(len(self._list))

    @property
    def dtype(self):
        if self._dtype is not None:
            return self._dtype

        if self:
            return type(self._list[0])

        return None

    @dtype.setter
    def dtype(self, dtype):
        str_dtype = str(dtype)
        if str_dtype == "callback_vec3":
            dtype = glm.vec3
        elif str_dtype == "callback_vec4":
            dtype = glm.vec4
        elif str_dtype == "callback_quat":
            dtype = glm.quat

        if self._dtype == dtype:
            return

        self._dtype = dtype
        self._list_dirty = True
        self._should_retest = True
