from abc import ABC, abstractmethod

from glass import sampler2D
from glass.DictList import DictList
from glass.utils import checktype

from ..Frame import Frame

class Filter(ABC):

    @abstractmethod
    def __call__(self, screen_image:sampler2D)->sampler2D:
        pass

    @abstractmethod
    def draw_to_active(self, screen_image:sampler2D)->None:
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

    @property
    def has_valid(self):
        for f in self:
            if f.enabled:
                return True
            
        return False

    def draw(self, screen_image:sampler2D):
        last_filter = None
        last_filter_index = -1
        for i in range(len(self)-1, -1, -1):
            f = self[i]
            if f.enabled:
                last_filter = f
                last_filter_index = i
                break

        if last_filter is None:
            Frame.draw(screen_image)
            return

        for i in range(last_filter_index):
            f = self[i]
            if not f.enabled:
                continue
            
            screen_image = f(screen_image)

        last_filter.draw_to_active(screen_image)
    