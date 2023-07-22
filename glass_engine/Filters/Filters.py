from abc import ABC, abstractmethod

from glass import sampler2D
from glass.DictList import DictList
from glass.utils import checktype

from ..Frame import Frame

class Filter(ABC):

    def __init__(self):
        self._should_update = False
        self._enabled = True

    @abstractmethod
    def __call__(self, screen_image:sampler2D)->sampler2D:
        pass

    @abstractmethod
    def draw_to_active(self, screen_image:sampler2D)->None:
        pass

    @property
    def enabled(self)->bool:
        return self._enabled
    
    @enabled.setter
    @checktype
    def enabled(self, flag:bool):
        self._enabled = flag

    @property
    def should_update(self)->bool:
        return (self._should_update and self._enabled)
    
    @should_update.setter
    @checktype
    def should_update(self, flag:bool):
        self._should_update = flag

class Filters(DictList):

    @property
    def has_valid(self):
        for f in self:
            if f.enabled:
                return True
            
        return False

    def draw(self, screen_image:sampler2D)->bool:
        should_update = False
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
            should_update = f.should_update or should_update
            f.should_update = False

        last_filter.draw_to_active(screen_image)
        should_update = last_filter.should_update or should_update
        last_filter.should_update = False
        return should_update
    