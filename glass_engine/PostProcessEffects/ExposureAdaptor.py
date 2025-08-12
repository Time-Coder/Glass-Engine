from .ShaderEffect import ShaderEffect
from glass import sampler2D, BlockHostClass

import time
import os


class ExposureAdaptor(ShaderEffect):

    class CurrentLuma(BlockHostClass):
        def __init__(self):
            BlockHostClass.__init__(self)
            self._current_luma = 0

        @property
        def current_luma(self):
            return self._current_luma

        @current_luma.setter
        @BlockHostClass.not_const
        def current_luma(self, luma: float):
            self._current_luma = luma

    def __init__(self):
        self_folder = os.path.dirname(os.path.abspath(__file__))
        ShaderEffect.__init__(
            self,
            self_folder + "/../glsl/PostProcessEffects/exposure_adaptor.glsl",
            generate_mipmap=True,
        )

        self.current_luma = ExposureAdaptor.CurrentLuma()
        self["CurrentLuma"] = self.current_luma

    def apply(self, screen_image: sampler2D) -> sampler2D:
        self.program["fps"] = self.camera.screen.smooth_fps
        return ShaderEffect.apply(self, screen_image)

    def draw_to_active(self, screen_image: sampler2D) -> None:
        self.program["fps"] = self.camera.screen.smooth_fps
        ShaderEffect.draw_to_active(self, screen_image)

    @property
    def should_update_until(self)->float:
        if not self._enabled:
            return 0

        if self.camera is None:
            return 0

        if (not self.camera.lens.auto_explosure) or self.camera.lens.local_explosure:
            return 0

        return self.camera.screen.scene_update_time + self.camera.lens.explosure_adapt_time
