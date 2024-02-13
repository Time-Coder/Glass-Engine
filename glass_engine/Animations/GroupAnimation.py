from .Animation import Animation


class GroupAnimation(Animation):

    def __init__(self, *animations, **kwargs):
        Animation.__init__(self, **kwargs)
        self.animations = animations

    @property
    def total_duration(self):
        total_duration = self.duration * self.loops
        if self.go_back:
            total_duration *= 2

        return total_duration
