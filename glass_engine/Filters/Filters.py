from abc import ABC, abstractmethod

from glass import sampler2D
from glass.DictList import DictList
from glass.utils import checktype

class Filter(ABC):

    @abstractmethod
    def __call__(self, screen_image:sampler2D)->sampler2D:
        pass

    @property
    def enabled(self)->bool:
        if not hasattr(self, "_enabled"):
            return True
        else:
            return self._enabled
    
    @enabled.setter
    @checktype
    def enabled(self, flag:bool):
        self._enabled = flag

class Filters(DictList):
    def __call__(self, screen_image:sampler2D)->sampler2D:
        for f in self:
            if not f.enabled:
                continue
            
            screen_image = f(screen_image)

        return screen_image
    