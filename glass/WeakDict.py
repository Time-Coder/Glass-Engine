from .WeakRef import WeakRef


class WeakDict:

    class iterator:
        def __init__(self, weak_ref, _iterator):
            self._iterator = _iterator
            self._weak_ref = weak_ref

        def __next__(self):
            value = self._iterator.__next__()
            if self._weak_ref:
                value = value.value

            return value

        def __iter__(self):
            return self

    class items_iterator:
        def __init__(self, weak_ref_keys, weak_ref_values, _iterator):
            self._iterator = _iterator
            self._weak_ref_keys = weak_ref_keys
            self._weak_ref_values = weak_ref_values

        def __next__(self):
            key, value = self._ref_iterator.__next__()
            if self._weak_ref_keys:
                key = key.value
            if self._weak_ref_values:
                value = value.value
            return key, value

        def __iter__(self):
            return self

    def __init__(self, weak_ref_keys=True, weak_ref_values=True):
        self._dict = {}
        self._weak_ref_keys = weak_ref_keys
        self._weak_ref_values = weak_ref_values

    def __iter__(self):
        result = WeakDict.iterator(self._weak_ref_keys, self._dict.__iter__())
        return result

    def __len__(self):
        return len(self._dict)

    def __bool__(self):
        return bool(self._dict)

    def __contains__(self, key):
        if self._weak_ref_keys:
            key = WeakRef(key)

        return key in self._dict

    def __getitem__(self, key):
        if self._weak_ref_keys:
            key = WeakRef(key)

        value = self._dict[key]
        if self._weak_ref_values:
            value = value.value

        return value

    def __setitem__(self, key, value):
        if self._weak_ref_keys:
            key = WeakRef(key)

        if self._weak_ref_values:
            value = WeakRef(value)

        self._dict[key] = value

    def __delitem__(self, key):
        if self._weak_ref_keys:
            key = WeakRef(key)

        del self._dict[key]

    def __repr__(self):
        return self._dict.__repr__()

    def pop(self, key):
        if self._weak_ref_keys:
            key = WeakRef(key)

        value = self._dict.pop(key)
        if self._weak_ref_values:
            value = value.value

        return value

    def clear(self):
        self._dict.clear()

    def update(self, _dict):
        for key, value in _dict.items():
            self[key] = value

    def keys(self):
        result = WeakDict.iterator(self._weak_ref_keys, self._dict.keys())
        return result

    def values(self):
        result = WeakDict.iterator(self._weak_ref_values, self._dict.values())
        return result

    def items(self):
        result = WeakDict.items_iterator(
            self._weak_ref_keys, self._weak_ref_values, self._dict.items()
        )
        return result
