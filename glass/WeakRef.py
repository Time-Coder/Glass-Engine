from .utils import di

class WeakRef:

    def __init__(self, obj):
        if isinstance(obj, (int,float,bool,str,bytes,type(None))):
            self._obj_id = obj
            self._is_real_id = False
        else:
            self._obj_id = id(obj)
            self._is_real_id = True

    def __hash__(self):
        return self._obj_id
    
    def __eq__(self, other):
        return (self._obj_id == other._obj_id)
    
    def __repr__(self):
        return self.value.__repr__()

    @property
    def value(self):
        if self._is_real_id:
            return di(self._obj_id)
        else:
            return self._obj_id
        