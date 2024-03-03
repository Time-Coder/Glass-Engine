from .WeakRef import WeakRef

from typing import Any, Iterable, Iterator, Union, List


class WeakList:

    class iterator:
        def __init__(self, iterator: Iterator):
            self._iterator: Iterator = iterator

        def __next__(self) -> Any:
            return self._iterator.__next__().value

        def __iter__(self) -> Iterator:
            return self

    def __init__(self) -> None:
        self._list: List[WeakRef] = []

    def __setitem__(self, index: Union[int, slice], value: Any) -> None:
        self._list[index] = WeakRef(value)

    def __getitem__(self, index: Union[int, slice]) -> Any:
        value: Any = self._list[index]
        if isinstance(index, slice):
            return list(map(lambda x: x.value, value))
        else:
            return value.value

    def __delitem__(self, index: Union[int, slice]) -> None:
        del self._list[index]

    def __contains__(self, value: Any) -> bool:
        return WeakRef(value) in self._list

    def __len__(self) -> int:
        return self._list.__len__()

    def __bool__(self) -> bool:
        return bool(self._list)

    def __iter__(self) -> Iterator:
        return WeakList.iterator(self._list.__iter__())

    def append(self, value: Any) -> None:
        self._list.append(WeakRef(value))

    def insert(self, index: int, value: Any) -> None:
        self._list.insert(index, WeakRef(value))

    def extend(self, value_list: Iterable):
        if isinstance(value_list, WeakList):
            self._list.extend(value_list._list)
        else:
            self._list.extend(map(lambda x: WeakRef(x), value_list))

    def index(self, value: Any) -> int:
        return self._list.index(WeakRef(value))

    def remove(self, value: Any) -> None:
        self._list.remove(WeakRef(value))

    def pop(self, index: int) -> Any:
        return self._list.pop(index).value

    def clear(self) -> None:
        self._list.clear()
