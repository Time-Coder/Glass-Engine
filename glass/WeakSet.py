from .WeakRef import WeakRef

class WeakSet:

    class iterator:
        def __init__(self, _iterator):
            self._iterator = _iterator

        def __next__(self):
            value = self._iterator.__next__()
            return value.value
        
        def __iter__(self):
            return self

    def __init__(self):
        self._set = set()

    def __iter__(self):
        result = WeakSet.iterator(self._set.__iter__())
        return result
    
    def __len__(self):
        return len(self._set)
    
    def __bool__(self):
        return bool(self._set)
    
    def __contains__(self, value):
        return (WeakRef(value) in self._set)
    
    def __repr__(self):
        return self._set.__repr__()
    
    def __sub__(self, other):
        result = WeakSet()
        if isinstance(other, WeakSet):
            result._set = self._set - other._set
        else:
            result._set = self._set - map(lambda x:WeakRef(x), other)

        return result
    
    def __add__(self, other):
        result = WeakSet()
        if isinstance(other, WeakSet):
            result._set = self._set + other._set
        else:
            result._set = self._set + map(lambda x:WeakRef(x), other)

        return result
    
    def __isub__(self, other):
        result = WeakSet()
        if isinstance(other, WeakSet):
            self._set -= other._set
        else:
            self._set -= map(lambda x:WeakRef(x), other)

        return result
    
    def __iadd__(self, other):
        result = WeakSet()
        if isinstance(other, WeakSet):
            self._set += other._set
        else:
            self._set += map(lambda x:WeakRef(x), other)

        return result

    def add(self, value):
        self._set.add(WeakRef(value))

    def remove(self, value):
        ref_value = WeakRef(value)
        if ref_value in self._set:
            self._set.remove(ref_value)

    def pop(self):
        return self._set.pop().value

    def clear(self):
        self._set.clear()
    
    def update(self, new_set):
        if isinstance(new_set, WeakSet):
            self._set.update(new_set._set)
        else:
            self._set.update(map(lambda x:WeakRef(x), new_set))
