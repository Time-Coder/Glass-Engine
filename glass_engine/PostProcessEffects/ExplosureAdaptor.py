from .ShaderEffect import ShaderEffect
from glass import sampler2D, ShaderStorageBlock

import time
import os

class ExplosureAdaptor(ShaderEffect):

    class CurrentLuma(ShaderStorageBlock.HostClass):
        def __init__(self):
            ShaderStorageBlock.HostClass.__init__(self)
            self._current_luma = 0

        @property
        def current_luma(self):
            return self._current_luma
        
        @current_luma.setter
        @ShaderStorageBlock.HostClass.not_const
        def current_luma(self, luma:float):
            self._current_luma = luma

    def __init__(self):
        self_folder = os.path.dirname(os.path.abspath(__file__))
        ShaderEffect.__init__(self, self_folder + "/../glsl/PostProcessEffects/explosure_adaptor.glsl", generate_mipmap=True)

        self.current_luma = ExplosureAdaptor.CurrentLuma()
        self["CurrentLuma"] = self.current_luma

    def apply(self, screen_image:sampler2D)->sampler2D:
        self.program["fps"] = self.camera.screen.smooth_fps
        return ShaderEffect.apply(self, screen_image)
    
    def draw_to_active(self, screen_image: sampler2D) -> None:
        self.program["fps"] = self.camera.screen.smooth_fps
        ShaderEffect.draw_to_active(self, screen_image)

    @property
    def should_update(self) -> bool:
        if not self._enabled:
            return False
        
        if (not self.camera.lens.auto_explosure) or self.camera.lens.local_explosure:
            return False
        
        return (self.screen_update_time == 0 or time.time()-self.screen_update_time <= self.camera.lens.explosure_adapt_time)
    
    @should_update.setter
    def should_update(self, flag:bool):
        pass
