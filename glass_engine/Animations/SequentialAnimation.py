from .AnimationGroup import AnimationGroup


class SequentialAnimation(AnimationGroup):

    def __init__(self, *animations, **kwargs):
        AnimationGroup.__init__(self, *animations, **kwargs)

    def _update_duration(self):
        if not self._total_duration_dirty:
            return

        self._duration = 0
        for animation in self:
            self._duration += animation.total_duration

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

        accum_time = 0
        next_accum_time = 0
        active_animation = None
        for animation in self:
            if animation is None:
                continue

            next_accum_time += animation.total_duration
            if accum_time <= reduce_t < next_accum_time:
                active_animation = animation
                break
            accum_time = next_accum_time

        if active_animation is None:
            self._running = False
            return

        active_animation._go_to(reduce_t - accum_time)

        if self.running_callback is not None:
            self.running_callback(t)
