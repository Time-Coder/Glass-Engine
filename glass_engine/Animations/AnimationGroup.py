from .Animation import Animation
from glass.DictList import DictList, ExtendableList

from typing import Any


def before_animation_add_callback(self: ExtendableList, animation: Any):
    if not isinstance(animation, Animation):
        raise TypeError("item add to AnimationGroup must be in type 'Animation'")


def after_animation_add_callback(self: ExtendableList, animation: Any):
    animation._parents.add(self)


def after_animation_remove_callback(self: ExtendableList, animation: Any):
    animation._parents.remove(self)


class AnimationGroup(Animation, DictList):

    def __init__(self, *animations, **kwargs):
        Animation.__init__(self, **kwargs)
        DictList.__init__(
            self,
            values=animations,
            before_item_add_callback=before_animation_add_callback,
            after_item_add_callback=after_animation_add_callback,
            after_item_remove_callback=after_animation_remove_callback,
        )

    def _update_duration(self):
        return

    @property
    def duration(self):
        self._update_duration()
        return self._duration

    @property
    def total_duration(self):
        self._update_duration()
        return self._total_duration
