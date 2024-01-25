class SequentialAnimation:

    class DoneCallback:

        def __init__(self, sequential_animation, animation, should_start:bool=True):
            self.sequential_animation = sequential_animation
            self.animation = animation
            self.should_start = should_start

        def __call__(self):
            self.sequential_animation._active_animation = self.animation
            if self.should_start:
                self.animation.start()

    def __init__(self, *animations):
        self.animations = animations
        for i in range(len(animations)):
            if i == len(animations) - 1:
                animations[i].done_callback = SequentialAnimation.DoneCallback(self, animations[0], should_start=False)
            else:
                animations[i].done_callback = SequentialAnimation.DoneCallback(self, animations[i+1])

        self._active_animation = None
        if len(self.animations) > 0:
            self._active_animation = self.animations[0]

    def start(self):
        if self._active_animation is not None:
            self._active_animation.start()
        
    def pause(self):
        if self._active_animation is not None:
            self._active_animation.pause()

    def stop(self):
        for animation in self.animations:
            animation.stop()

    def goto(self, t:float):
        start_time = 0
        active_status = self._active_animation.status
        to_end = True
        for animation in self.animations:
            if start_time <= t <= start_time + animation.duration * animation.loops:
                self._active_animation = animation
                self._active_animation.status = active_status
                self._active_animation.goto(t - start_time)
            else:
                if to_end:
                    animation.stop(animation.end_value)
                else:
                    animation.stop(animation.start_value)