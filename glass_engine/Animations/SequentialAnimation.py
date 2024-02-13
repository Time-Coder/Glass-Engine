from .GroupAnimation import GroupAnimation


class SequentialAnimation(GroupAnimation):

    def __init__(self, *animations, **kwargs):
        GroupAnimation.__init__(self, *animations, **kwargs)

    @property
    def duration(self):
        duration = 0
        for animation in self.animations:
            duration += animation.total_duration

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

        accum_time = 0
        next_accum_time = 0
        active_animation = None
        for animation in self.animations:
            next_accum_time += animation.total_duration
            if  accum_time <= reduce_t < next_accum_time:
                active_animation = animation
                break
            accum_time = next_accum_time

        if active_animation is None:
            self._running = False
            return
        
        active_animation._goto(reduce_t - accum_time)

        if self.running_callback is not None:
            self.running_callback(t)
