from abc import ABC, abstractmethod
from glass import sampler2D
from glass.utils import checktype

from functools import wraps


class PostProcessEffect(ABC):

    def __init__(self):
        self._enabled = True

        self.depth_map = None
        self.world_pos_map = None
        self.world_normal_map = None
        self.camera = None

    def __bool__(self) -> bool:
        return self._enabled
    
    def param_setter(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            self = args[0]
            value = args[1]

            equal = False
            try:
                lvalue = getattr(self, func.__name__)
                if type(lvalue) != type(value):
                    equal = False
                else:
                    equal = bool(lvalue == value)
            except:
                equal = False

            if equal:
                return

            safe_func = checktype(func)
            return_value = safe_func(*args, **kwargs)
            if self.camera is not None:
                self.camera.screen.update_PPEs()

            return return_value

        return wrapper

    @abstractmethod
    def apply(self, screen_image: sampler2D) -> sampler2D:
        pass

    @abstractmethod
    def draw_to_active(self, screen_image: sampler2D) -> None:
        pass

    @abstractmethod
    def need_pos_info(self) -> bool:
        return False

    @property
    def enabled(self) -> bool:
        return self._enabled

    @enabled.setter
    @param_setter
    def enabled(self, flag: bool):
        self._enabled = flag

    @property
    def should_update_until(self)->float:
        return 0.0