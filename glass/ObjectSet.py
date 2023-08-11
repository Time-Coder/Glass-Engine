from .utils import id_to_var

class ObjectSet:

    class iterator:
        def __init__(self, _set_iterator):
            self._set_iterator = _set_iterator

        def __next__(self):
            id_var = self._set_iterator.__next__()
            return id_to_var(id_var)
        
        def __iter__(self):
            return self

    def __init__(self):
        self._set = set()

    def __iter__(self):
        result = ObjectSet.iterator(self._set.__iter__())
        return result
    
    def __len__(self):
        return self._set.__len__()
    
    def __bool__(self):
        return bool(self._set)
    
    def __contains__(self, var):
        return (id(var) in self._set)

    def add(self, var):
        self._set.add(id(var))

    def remove(self, var):
        id_var = id(var)
        if id_var in self._set:
            self._set.remove(id_var)

    def clear(self):
        self._set.clear()
    
    def update(self, new_set):
        if isinstance(new_set, ObjectSet):
            self._set.update(new_set._set)
        else:
            self._set.update(map(lambda x:id(x), new_set))