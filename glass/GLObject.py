import numpy as np
from OpenGL import GL

from .WeakSet import WeakSet
from .GLConfig import GLConfig

class _MetaGLObject(type):

    _all_instances = {}

    @property
    def active_id(cls):
        try:
            return GL.glGetIntegerv(cls._basic_info["binding_type"])
        except:
            return 0
        
    @property
    def all_instances(cls):
        if cls not in _MetaGLObject._all_instances:
            _MetaGLObject._all_instances[cls] = WeakSet()

        return _MetaGLObject._all_instances[cls]

class GLObject(metaclass=_MetaGLObject):

    def __init__(self, context_shared=True):
        self._id = 0
        self._context_shared = context_shared
        self._context = 0
        if self.__class__ not in _MetaGLObject._all_instances:
            _MetaGLObject._all_instances[self.__class__] = WeakSet()

        _MetaGLObject._all_instances[self.__class__].add(self)

    def __hash__(self)->int:
        return id(self)
    
    def __eq__(self, _value)->bool:
        return (id(self) == id(_value))

    @property
    def context_shared(self):
        return self._context_shared
    
    @property
    def context(self):
        return self._context

    @property
    def id(self):
        return self._id
    
    def delete(self):
        if self._id == 0:
            return

        try:
            self.unbind()
        except:
            pass

        try:
            del_func = self.__class__._basic_info["del_func"]
            need_number = self.__class__._basic_info["need_number"]
            if need_number:
                del_func(1, np.array([self._id]))
            else:
                del_func(self._id)
        except:
            pass

        self._id = 0

    def __del__(self):
        if self.__class__ in _MetaGLObject._all_instances:
            _MetaGLObject._all_instances[self.__class__].remove(self)

        if self._id == 0:
            return

        is_bound = False
        try:
            is_bound = self.is_bound
        except:
            pass

        if is_bound:
            try:
                target_type = self.__class__._basic_info["target_type"]
                bind_func = self.__class__._basic_info["bind_func"]
                if target_type is None:
                    bind_func(0)
                else:
                    bind_func(target_type, 0)
            except:
                pass

        try:
            del_func = self.__class__._basic_info["del_func"]
            need_number = self.__class__._basic_info["need_number"]
            if need_number:
                del_func(1, np.array([self._id]))
            else:
                del_func(self._id)
        except:
            pass

        self._id = 0

    def bind(self):
        current_context = GLConfig.buffered_current_context
        if self._context != 0 and current_context != self._context:
            raise RuntimeError(f"try to bind context({self._context})'s {self.__class__.__name__}({self.id}) in context({current_context})")

        if self._id == 0:
            gen_func = self.__class__._basic_info["gen_func"]
            need_number = self.__class__._basic_info["need_number"]
            if need_number:
                self._id = gen_func(1)
            else:
                self._id = gen_func()
            self._id = int(self._id)

            if self._id == 0:
                raise MemoryError("failed to create " + self.__class__.__name__)

        # if self.is_bound:
        #     return

        target_type = self.__class__._basic_info["target_type"]
        bind_func = self.__class__._basic_info["bind_func"]
        if target_type is None:
            bind_func(self._id)
        else:
            bind_func(target_type, self._id)

        if not self._context_shared:
            self._context = current_context

    def unbind(self):
        if not self.is_bound:
            return False

        target_type = self.__class__._basic_info["target_type"]
        bind_func = self.__class__._basic_info["bind_func"]
        try:
            if target_type is None:
                bind_func(0)
            else:
                bind_func(target_type, 0)
            return True
        except:
            return False

    @property
    def is_bound(self):
        return (self._id != 0 and self.__class__.active_id == self._id)
    