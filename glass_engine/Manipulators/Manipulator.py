from ._Manipulator import _MouseButton, _Key

import glm

class Manipulator:

    MouseButton = _MouseButton
    Key = _Key

    @property
    def camera(self):
        if hasattr(self, "_camera"):
            return self._camera
        else:
            return None

    def startup(self)->bool:
        return False

    def on_mouse_pressed(self, button:MouseButton, screen_pos:glm.vec2, global_pos:glm.vec2)->bool:
        return False

    def on_mouse_released(self, button:MouseButton, screen_pos:glm.vec2, global_pos:glm.vec2)->bool:
        return False
    
    def on_mouse_double_clicked(self, button:MouseButton, screen_pos:glm.vec2, global_pos:glm.vec2)->bool:
        return False

    def on_mouse_moved(self, screen_pos:glm.vec2, global_pos:glm.vec2)->bool:
        return False

    def on_wheel_scrolled(self, angle:glm.vec2, screen_pos:glm.vec2, global_pos:glm.vec2)->bool:
        return False

    def on_key_pressed(self, key:Key)->bool:
        return False

    def on_key_released(self, key:Key)->bool:
        return False

    def on_key_repeated(self, keys:set[Key])->bool:
        return False