from .WeakSet import WeakSet
import functools

class MetaInstancesRecorder(type):

    _all_instances = {}
    
    @property
    def all_instances(cls):
        if cls not in MetaInstancesRecorder._all_instances:
            MetaInstancesRecorder._all_instances[cls] = WeakSet()

        return MetaInstancesRecorder._all_instances[cls]
    
    @staticmethod
    def init(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            self = args[0]
            if self.__class__ not in MetaInstancesRecorder._all_instances:
                MetaInstancesRecorder._all_instances[self.__class__] = WeakSet()

            MetaInstancesRecorder._all_instances[self.__class__].add(self)
            return func(*args, **kwargs)

        return wrapper
    
    @staticmethod
    def delete(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            self = args[0]
            if self.__class__ in MetaInstancesRecorder._all_instances:
                MetaInstancesRecorder._all_instances[self.__class__].remove(self)
            
            return func(*args, **kwargs)

        return wrapper