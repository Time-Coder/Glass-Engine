from .utils import di

from typing import Any, Union


class WeakRef:

    def __init__(self, obj: Any) -> None:
        if isinstance(obj, (int, float, complex, bool, str, bytes, type(None))):
            self._obj_id: Union[int, float, complex, bool, str, bytes, None] = obj
            self._is_real_id: bool = False
        else:
            self._obj_id: Union[int, float, complex, bool, str, bytes, None] = id(obj)
            self._is_real_id: bool = True

    def __hash__(self) -> int:
        return hash(self._obj_id)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, WeakRef):
            return self._obj_id == other._obj_id
        else:
            return self.value == other

    def __repr__(self) -> str:
        return self.value.__repr__()

    @property
    def value(self) -> Any:
        if self._is_real_id:
            return di(self._obj_id)
        else:
            return self._obj_id
