from glass import sampler2D
from glass.DictList import DictList
from .PostProcessEffect import PostProcessEffect

from ..Frame import Frame

class PostProcessEffects(DictList):

    def __init__(self):
        DictList.__init__(self)
        self._screen_update_time = 0
        self._should_update = False

        self.camera = None
        self.view_pos_map = None
        self.view_normal_map = None
        self.depth_map = None

    @property
    def has_valid(self)->bool:
        for effect in self:
            if effect.enabled:
                return True
            
        return False
    
    @property
    def need_pos_info(self)->bool:
        for effect in self:
            if effect.enabled and effect.need_pos_info():
                return True
            
        return False

    @property
    def last_valid(self)->PostProcessEffect:
        for i in range(len(self)-1, -1, -1):
            effect = self[i]
            if effect.enabled:
                return effect
            
        return None

    def apply(self, screen_image:sampler2D)->sampler2D:
        self._should_update = False
        for effect in self:
            if not effect.enabled:
                continue

            effect.depth_map = self.depth_map
            effect.camera = self.camera
            effect.view_pos_map = self.view_pos_map
            effect.view_normal_map = self.view_normal_map
            screen_image = effect.apply(screen_image)

            self._should_update = self._should_update or effect.should_update
            effect.should_update = False

        return screen_image
    
    @property
    def should_update(self)->bool:
        return self._should_update

    def draw_to_active(self, screen_image:sampler2D)->bool:
        should_update = False
        last_effect = None
        last_effect_index = -1
        for i in range(len(self)-1, -1, -1):
            effect = self[i]
            if effect.enabled:
                last_effect = effect
                last_effect_index = i
                break

        if last_effect is None:
            Frame.draw(screen_image)
            return

        for i in range(last_effect_index):
            effect = self[i]
            if not effect.enabled:
                continue
            
            effect.depth_map = self.depth_map
            effect.camera = self.camera
            effect.view_pos_map = self.view_pos_map
            effect.view_normal_map = self.view_normal_map
            screen_image = effect.apply(screen_image)

            should_update = effect.should_update or should_update
            effect.should_update = False

        last_effect.depth_map = self.depth_map
        last_effect.camera = self.camera
        last_effect.view_pos_map = self.view_pos_map
        last_effect.view_normal_map = self.view_normal_map
        last_effect.draw_to_active(screen_image)

        should_update = last_effect.should_update or should_update
        last_effect.should_update = False

        return should_update
    
    @property
    def screen_update_time(self)->float:
        return self._screen_update_time
    
    @screen_update_time.setter
    def screen_update_time(self, screen_update_time:float)->None:
        self._screen_update_time = screen_update_time
        for effect in self:
            effect.screen_update_time = screen_update_time
    