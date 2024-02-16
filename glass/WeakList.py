from .WeakRef import WeakRef

from typing import Self, Any, Iterable, Iterator, Union, List


class WeakList:

    class iterator:
        def __init__(self: Self, iterator: Iterator):
            self._iterator: Iterator = iterator

        def __next__(self: Self) -> Any:
            return self._iterator.__next__().value

        def __iter__(self: Self) -> Iterator:
            return self

    def __init__(self: Self) -> None:
        self._list: List[WeakRef] = []

    def __setitem__(self: Self, index: Union[int, slice], value: Any) -> None:
        self._list[index] = WeakRef(value)

    def __getitem__(self: Self, index: Union[int, slice]) -> Any:
        value: Any = self._list[index]
        if isinstance(index, slice):
            return list(map(lambda x: x.value, value))
        else:
            return value.value

    def __delitem__(self: Self, index: Union[int, slice]) -> None:
        del self._list[index]

    def __contains__(self: Self, value: Any) -> bool:
        return WeakRef(value) in self._list

    def __len__(self: Self) -> int:
        return self._list.__len__()

    def __bool__(self: Self) -> bool:
        return bool(self._list)

    def __iter__(self: Self) -> Iterator:
        return WeakList.iterator(self._list.__iter__())

    def append(self: Self, value: Any) -> None:
        self._list.append(WeakRef(value))

    def insert(self: Self, index: int, value: Any) -> None:
        self._list.insert(index, WeakRef(value))

    def extend(self: Self, value_list: Iterable):
        if isinstance(value_list, WeakList):
            self._list.extend(value_list._list)
        else:
            self._list.extend(map(lambda x: WeakRef(x), value_list))

    def index(self: Self, value: Any) -> int:
        return self._list.index(WeakRef(value))

    def remove(self: Self, value: Any) -> None:
        self._list.remove(WeakRef(value))

    def pop(self: Self, index: int) -> Any:
        return self._list.pop(index).value

    def clear(self: Self) -> None:
        self._list.clear()
