from .GroupAnimation import GroupAnimation


class ParallelAnimation(GroupAnimation):

    def __init__(self, *animations, **kwargs):
        GroupAnimation.__init__(self, *animations, **kwargs)

    @property
    def duration(self):
        duration = 0
        for animation in self.animations:
            current_total_duration = animation.total_duration
            if current_total_duration >= duration:
                duration = current_total_duration

        return duration

    def _goto(self, t: float):
        end_time = self.total_duration
        if t > end_time:
            t = end_time
            self._running = False

        self_duration = self.duration
        progress = t / self_duration
        int_progress = int(progress)
        if progress != int_progress:
            progress -= int_progress
        elif progress != 0:
            progress = 1
        else:
            progress = 0

        if self.go_back and int_progress % 2 == 1:
            progress = 1 - progress

        reduce_t = progress * self_duration

        has_active_animation = False
        for animation in self.animations:
            if  reduce_t < animation.total_duration:
                animation._goto(reduce_t)
                has_active_animation = True

        if not has_active_animation:
            self._running = False
            return

        if self.running_callback is not None:
            self.running_callback(t)