from .WeakRef import WeakRef

class WeakList:

    class iterator:
        def __init__(self, _iterator):
            self._iterator = _iterator

        def __next__(self):
            return self._iterator.__next__().value
        
        def __iter__(self):
            return self

    def __init__(self):
        self._list = []

    def __setitem__(self, index, value):
        self._list[index] = WeakRef(value)

    def __getitem__(self, index):
        value = self._list[index]
        if isinstance(index, slice):
            return list(map(lambda x:x.value, value))
        else:
            return value.value
            
    def __delitem__(self, index):
        del self._list[index]
        
    def __contains__(self, value):
        return WeakRef(value) in self._list
        
    def __len__(self):
        return self._list.__len__()
    
    def __bool__(self):
        return bool(self._list)
    
    def __iter__(self):
        return WeakList.iterator(self._list.__iter__())
    
    def append(self, value):
        self._list.append(WeakRef(value))

    def insert(self, index, value):
        self._list.insert(index, WeakRef(value))

    def extend(self, value_list):
        if isinstance(value_list, WeakList):
            self._list.extend(value_list._list)
        else:
            self._list.extend(map(lambda x:WeakRef(x), value_list))

    def remove(self, value):
        self._list.remove(WeakRef(value))

    def pop(self, index):
        return self._list.pop(index).value
        
    def clear(self):
        self._list.clear()
        