from .AnimationGroup import AnimationGroup


class ParallelAnimation(AnimationGroup):

    def __init__(self, *animations, **kwargs):
        AnimationGroup.__init__(self, *animations, **kwargs)

    def _update_duration(self):
        if not self._total_duration_dirty:
            return

        self._duration = 0
        for animation in self:
            if animation.total_duration > self._duration:
                self._duration = animation.total_duration

        self._total_duration = self._duration * self.loops
        if self._go_back:
            self._total_duration *= 2

        self._total_duration_dirty = False

    def _go_to(self, t: float):
        if t > self.total_duration:
            t = self.total_duration
            self._running = False

        progress = t / self.duration
        int_progress = int(progress)
        if progress != int_progress:
            progress -= int_progress
        elif progress != 0:
            progress = 1
        else:
            progress = 0

        if self.go_back and int_progress % 2 == 1:
            progress = 1 - progress

        reduce_t = progress * self.duration

        has_active_animation = False
        for animation in self:
            if animation is None:
                continue

            if reduce_t < animation.total_duration:
                animation._go_to(reduce_t)
                has_active_animation = True

        if not has_active_animation:
            self._running = False
            return

        if self.running_callback is not None:
            self.running_callback(t)
