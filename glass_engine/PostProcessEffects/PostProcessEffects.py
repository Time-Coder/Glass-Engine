from glass import sampler2D
from glass.DictList import DictList
from .PostProcessEffect import PostProcessEffect

from ..Frame import Frame


class PostProcessEffects(DictList):

    def __init__(self, screen):
        DictList.__init__(self)
        self._screen = screen

        self.view_pos_map = None
        self.view_normal_map = None
        self.depth_map = None

    @property
    def has_valid(self) -> bool:
        for effect in self:
            if effect is not None and effect.enabled:
                return True

        return False

    @property
    def need_pos_info(self) -> bool:
        for effect in self:
            if effect is not None and effect.enabled and effect.need_pos_info():
                return True

        return False

    @property
    def last_valid(self) -> PostProcessEffect:
        for i in range(len(self) - 1, -1, -1):
            effect = self[i]
            if effect is not None and effect.enabled:
                return effect

        return None

    def apply(self, screen_image: sampler2D) -> sampler2D:
        for effect in self:
            if effect is None or not effect.enabled:
                continue

            effect.depth_map = self.depth_map
            effect.camera = self._screen._camera
            effect.view_pos_map = self.view_pos_map
            effect.view_normal_map = self.view_normal_map
            screen_image = effect.apply(screen_image)

        return screen_image

    def draw_to_active(self, screen_image: sampler2D) -> None:
        last_effect = None
        last_effect_index = -1
        for i in range(len(self) - 1, -1, -1):
            effect = self[i]
            if effect is not None and effect.enabled:
                last_effect = effect
                last_effect_index = i
                break

        if last_effect is None:
            Frame.draw(screen_image)
            return

        for i in range(last_effect_index):
            effect = self[i]
            if effect is None or not effect.enabled:
                continue

            effect.depth_map = self.depth_map
            effect.camera = self._screen._camera
            effect.view_pos_map = self.view_pos_map
            effect.view_normal_map = self.view_normal_map
            screen_image = effect.apply(screen_image)

        last_effect.depth_map = self.depth_map
        last_effect.camera = self._screen._camera
        last_effect.view_pos_map = self.view_pos_map
        last_effect.view_normal_map = self.view_normal_map
        last_effect.draw_to_active(screen_image)

    @property
    def should_update_until(self) -> float:
        until_time = 0.0
        for effect in self:
            effect_until = effect.should_update_until
            if effect_until > until_time:
                until_time = effect_until
        return until_time