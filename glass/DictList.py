from typing import (
    Union,
    Any,
    Callable,
    Iterable,
    Iterator,
    Dict,
    List,
    KeysView,
    Tuple,
)
from .WeakList import WeakList


class ExtendableList:

    def __init__(
        self,
        weak_ref: bool = True,
        before_item_add_callback=None,
        before_item_remove_callback=None,
        after_item_add_callback=None,
        after_item_remove_callback=None,
    ) -> None:
        if weak_ref:
            self._list: Union[List[Any], WeakList] = WeakList()
        else:
            self._list: Union[List[Any], WeakList] = []

        self.before_item_add_callback: Union[
            None, Callable[[ExtendableList, Any], None]
        ] = before_item_add_callback
        self.before_item_remove_callback: Union[
            None, Callable[[ExtendableList, Any], None]
        ] = before_item_remove_callback
        self.after_item_add_callback: Union[
            None, Callable[[ExtendableList, Any], None]
        ] = after_item_add_callback
        self.after_item_remove_callback: Union[
            None, Callable[[ExtendableList, Any], None]
        ] = after_item_remove_callback

    def __setitem__(self, index: Union[int, slice], value: Any) -> None:
        len_self: int = len(self)
        item_to_be_removed: Any = None
        if isinstance(index, int) and index >= len_self:
            self._list.extend([None] * (index - len_self + 1))
        elif self.after_item_remove_callback is not None:
            item_to_be_removed: Any = self._list[index]

        # before callback
        if (
            self.before_item_remove_callback is not None
            and item_to_be_removed is not None
        ):
            if isinstance(index, int):
                self.before_item_remove_callback(self, item_to_be_removed)
            elif isinstance(index, slice):
                for item in item_to_be_removed:
                    self.before_item_remove_callback(self, item)

        if self.before_item_add_callback is not None:
            if isinstance(index, int):
                self.before_item_add_callback(self, value)
            elif isinstance(index, slice):
                for item in value:
                    self.before_item_add_callback(self, item)

        self._list[index] = value

        # after callback
        if (
            self.after_item_remove_callback is not None
            and item_to_be_removed is not None
        ):
            if isinstance(index, int):
                self.after_item_remove_callback(self, item_to_be_removed)
            elif isinstance(index, slice):
                for item in item_to_be_removed:
                    self.after_item_remove_callback(self, item)

        if self.after_item_add_callback is not None:
            if isinstance(index, int):
                self.after_item_add_callback(self, value)
            elif isinstance(index, slice):
                for item in value:
                    self.after_item_add_callback(self, item)

    def __getitem__(self, index: Union[int, slice]) -> Any:
        return self._list[index]

    def __delitem__(self, index: Union[int, slice]) -> None:
        item_to_be_removed: Any = self._list[index]

        # before callback
        if self.before_item_remove_callback is not None:
            if isinstance(index, int):
                self.before_item_remove_callback(self, item_to_be_removed)
            elif isinstance(index, slice):
                for item in item_to_be_removed:
                    self.before_item_remove_callback(self, item)

        del self._list[index]

        # after callback
        if self.after_item_remove_callback is not None:
            if isinstance(index, int):
                self.after_item_remove_callback(self, item_to_be_removed)
            elif isinstance(index, slice):
                for item in item_to_be_removed:
                    self.after_item_remove_callback(self, item)

    def __contains__(self, value: Any) -> bool:
        return value in self._list

    def __len__(self) -> int:
        return self._list.__len__()

    def __bool__(self) -> bool:
        return bool(self._list)

    def __iter__(self) -> Iterator:
        return self._list.__iter__()

    def append(self, value: Any) -> None:
        # before callback
        if self.before_item_add_callback is not None:
            self.before_item_add_callback(self, value)

        self._list.append(value)

        # after callback
        if self.after_item_add_callback is not None:
            self.after_item_add_callback(self, value)

    def insert(self, index: int, value: Any) -> None:
        # before callback
        if self.before_item_add_callback is not None:
            self.before_item_add_callback(self, value)

        self._list.insert(index, value)

        # after callback
        if self.after_item_add_callback is not None:
            self.after_item_add_callback(self, value)

    def extend(self, values: Iterable) -> None:
        # before callback
        if self.before_item_add_callback is not None:
            for item in values:
                self.before_item_add_callback(self, item)

        self._list.extend(values)

        # after callback
        if self.after_item_add_callback is not None:
            for item in values:
                self.after_item_add_callback(self, item)

    def remove(self, value: Any) -> None:
        index: int = self._list.index(value)
        item_to_be_removed: Any = self._list[index]

        # before callback
        if self.before_item_remove_callback is not None:
            self.before_item_remove_callback(self, item_to_be_removed)

        self._list.remove(value)

        # after callback
        if self.after_item_remove_callback is not None:
            self.after_item_remove_callback(self, item_to_be_removed)

    def pop(self, index: int) -> Any:
        item_to_be_removed: Any = self._list[index]

        # before callback
        if self.before_item_remove_callback is not None:
            self.before_item_remove_callback(self, item_to_be_removed)

        self._list.pop(index)

        # after callback
        if self.after_item_remove_callback is not None:
            self.after_item_remove_callback(self, item_to_be_removed)

        return item_to_be_removed

    def clear(self) -> None:
        # before callback
        items_to_be_removed: List[Any] = []
        for item in self._list:
            items_to_be_removed.append(item)
            if self.before_item_remove_callback is not None:
                self.before_item_remove_callback(self, item)

        self._list.clear()

        # after callback
        if self.after_item_remove_callback is not None:
            for item in items_to_be_removed:
                self.after_item_remove_callback(self, item)


class DictList(ExtendableList):
    def __init__(
        self,
        values: Union[Dict[str, Any], Iterable, None] = None,
        weak_ref: bool = False,
        before_item_add_callback: Union[
            None, Callable[[ExtendableList, Any], None]
        ] = None,
        before_item_remove_callback: Union[
            None, Callable[[ExtendableList, Any], None]
        ] = None,
        after_item_add_callback: Union[
            None, Callable[[ExtendableList, Any], None]
        ] = None,
        after_item_remove_callback: Union[
            None, Callable[[ExtendableList, Any], None]
        ] = None,
        **kwargs
    ) -> None:
        ExtendableList.__init__(
            self,
            weak_ref,
            before_item_add_callback,
            before_item_remove_callback,
            after_item_add_callback,
            after_item_remove_callback,
        )

        self._key_index_map: Dict[str, int] = {}
        self._key_list: ExtendableList = ExtendableList()

        if isinstance(values, dict):
            self.update(values)
        elif values is not None:
            self.extend(values)

        self.update(kwargs)

    def __setitem__(self, index: Union[int, slice, str], value: Any) -> None:
        if isinstance(index, str):
            key: str = index
            if key in self._key_index_map:
                index: int = self._key_index_map[key]
                ExtendableList.__setitem__(self, index, value)
            else:
                len_self: int = len(self)
                self._key_index_map[key] = len_self
                self._key_list[len_self] = key
                ExtendableList.append(self, value)
        else:
            ExtendableList.__setitem__(self, index, value)

    def __getitem__(self, index: Union[int, slice, str]) -> Any:
        if isinstance(index, str):
            key: str = index
            index: int = self._key_index_map[key]

        return ExtendableList.__getitem__(self, index)

    def __update_after(self, index: int) -> None:
        for i in range(index, len(self._key_list)):
            key: str = self._key_list[i]
            if key is not None:
                self._key_index_map[key] = i

    def _process_slice(self, index: slice) -> Tuple[int]:
        len_self: int = len(self)
        start: int = index.start if index.start is not None else 0
        stop: int = index.stop if index.stop is not None else len_self
        step: int = index.step if index.step is not None else 1

        if len_self > 0:
            while start < 0:
                start += len_self

            while stop < 0:
                stop += len_self

        if start < 0:
            start: int = 0
        if stop > len_self:
            stop: int = len_self

        return start, stop, step

    def __delitem__(self, index: Union[int, str, slice]) -> None:
        if isinstance(index, slice):
            start, stop, step = self._process_slice(index)
            for i in range(start, stop, step):
                del self[i]
            return

        key = None
        if isinstance(index, str):
            key = index
            index = self._key_index_map[key]
        elif isinstance(index, int):
            key = self._key_list[index]

        if key is not None:
            del self._key_index_map[key]

        del self._key_list[index]
        ExtendableList.__delitem__(self, index)

        self.__update_after(index)

    def pop(self, index: Union[int, str]) -> Any:
        key: Union[str, None] = None
        if isinstance(index, str):
            key: Union[str, None] = index
            index: int = self._key_index_map[key]
        elif isinstance(index, int):
            key: Union[str, None] = self._key_list[index]

        if key is not None:
            del self._key_index_map[key]

        del self._key_list[index]
        value: Any = ExtendableList.pop(self, index)

        self.__update_after(index)

        return value

    def insert(
        self, index: Union[int, str], value: Any, key: Union[str, None] = None
    ) -> None:
        if isinstance(index, str):
            index: int = self._key_index_map[index]

        ExtendableList.insert(self, index, value)
        self._key_list.insert(index, key)
        if key is not None:
            self._key_index_map[key] = index

        self.__update_after(index + 1)

    def append(self, value: Any, key: Union[str, None] = None) -> None:
        ExtendableList.append(self, value)
        self._key_list.append(key)
        if key is not None:
            self._key_index_map[key] = len(self) - 1

    def extend(self, new_list: Iterable) -> None:
        ExtendableList.extend(self, new_list)
        self._key_list.extend([None] * len(new_list))

    def update(self, new_dict: Dict[str, Any]) -> None:
        for key, value in new_dict.items():
            self[key] = value

    def index(self, key: str) -> int:
        return self._key_index_map[key]

    def key(self, index: int) -> str:
        return self._key_list[index]

    def clear(self) -> None:
        ExtendableList.clear(self)
        self._key_index_map.clear()
        self._key_list.clear()

    def __contains__(self, key: Any) -> bool:
        if isinstance(key, str):
            return key in self._key_index_map
        else:
            return ExtendableList.__contains__(self, key)

    def keys(self) -> KeysView:
        return self._key_index_map.keys()
