from glass.MetaInstancesRecorder import MetaInstancesRecorder

from .Chronoscope import Chronoscope
from .EasingCurve import EasingCurve

import threading
import time

class Animation(metaclass=MetaInstancesRecorder):

    @MetaInstancesRecorder.init
    def __init__(self, target=None, attr:str="", start_value=None, end_value=None, duration:float=1, easing_curve:EasingCurve=EasingCurve.Linear, step:float=0.01, loops:int=1, running_callback=None, done_callback=None):
        self.target:object = target
        self.attr:str = attr
        self.start_value:object = start_value
        self.end_value:object = end_value
        self.duration:float = duration
        self.step:float = step
        self.loops:int = loops
        self.easing_curve:EasingCurve = easing_curve
        self.running_callback = running_callback
        self.done_callback = done_callback

        self._timer = Chronoscope()
        self._running_thread = None

        if start_value is None:
            self.start_value = getattr(target, attr)

    @MetaInstancesRecorder.delete
    def __del__(self):
        pass

    def start(self):
        if self._timer.status == Chronoscope.Status.Stop:
            self._running_thread = threading.Thread(target=self._run, args=(), daemon=True)
            self._running_thread.start()
        self._timer.start()

    def pause(self):
        self._timer.pause()

    def stop(self, stop_value=None):
        self._running = False
        if self._running_thread is not None:
            if self._running_thread.is_alive():
                old_done_callback = self.done_callback
                self.done_callback = None
                self._running_thread.join()
                self.done_callback = old_done_callback

            self._running_thread = None

        self._timer.stop()
        if stop_value is None:
            stop_value = self.start_value

        setattr(self.target, self.attr, stop_value)

    def goto(self, t:float):
        self._timer.goto(t)

    @property
    def speed(self):
        return self._timer.speed
    
    @speed.setter
    def speed(self, speed:float):
        self._timer.speed = speed

    @property
    def status(self):
        return self._timer.status
    
    @status.setter
    def status(self, status):
        if self._timer.status == status:
            return
        
        if self._timer.status == Chronoscope.Status.Stop:
            if status == Chronoscope.Status.Paused:
                self._timer.status = Chronoscope.Status.Paused
            else:
                self.start()
        elif self._timer.status == Chronoscope.Status.Paused:
            if status == Chronoscope.Status.Stop:
                self.stop()
            else:
                self.start()
        elif self._timer.status == Chronoscope.Status.Running:
            if status == Chronoscope.Status.Paused:
                self.pause()
            else:
                self.stop()

    def _run(self):
        self._running = True
        while self._running:
            current_time = time.perf_counter()
            next_time = current_time + self.step

            t = self._timer.time()
            end_time = self.duration * self.loops
            if t > end_time:
                t = end_time
                self._running = False
            
            progress = t / self.duration
            int_progress = int(progress)
            if progress != int_progress:
                progress -= int_progress
            elif progress != 0:
                progress = 1
            else:
                progress = 0

            mapped_progress = self.easing_curve(progress)

            if self.target is not None:
                setattr(self.target, self.attr, self.start_value + mapped_progress * (self.end_value - self.start_value))

            if self.running_callback is not None:
                self.running_callback(progress * self.duration)

            if self._running:
                dt = next_time - time.perf_counter()
                if dt > 0:
                    time.sleep(dt)

        self._timer.stop()
        if self.done_callback is not None:
            self.done_callback()
    
    @staticmethod
    def has_valid():
        for animation in Animation.all_instances:
            if animation.status != Chronoscope.Status.Stop:
                return True
            
        return False