from abc import ABC, abstractmethod
from glass import sampler2D
from glass.utils import checktype

class PostProcessEffect(ABC):

    def __init__(self):
        self._should_update = False
        self._enabled = True
        self._screen_update_time = 0
        
        self.depth_map = None
        self.view_pos_map = None
        self.view_normal_map = None
        self.camera = None

    def __bool__(self)->bool:
        return self._enabled

    @abstractmethod
    def apply(self, screen_image:sampler2D)->sampler2D:
        pass

    @abstractmethod
    def draw_to_active(self, screen_image:sampler2D)->None:
        pass

    @abstractmethod
    def need_pos_info(self)->bool:
        return False

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

    @property
    def screen_update_time(self):
        return self._screen_update_time
    
    @screen_update_time.setter
    @checktype
    def screen_update_time(self, screen_update_time:float):
        self._screen_update_time = screen_update_time