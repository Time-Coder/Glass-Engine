from .Animation import Animation


class GroupAnimation(Animation):

    def __init__(self, *animations, **kwargs):
        Animation.__init__(self, **kwargs)
        self.animations = animations

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
