from .WeakSet import WeakSet
import functools


class MetaInstancesRecorder(type):

    _all_instances = {}

    @property
    def all_instances(cls):
        all_instances = WeakSet()
        for key, _set in MetaInstancesRecorder._all_instances.items():
            if issubclass(key, cls):
                all_instances.update(_set)

        return all_instances

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
