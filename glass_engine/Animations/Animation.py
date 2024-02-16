from glass.MetaInstancesRecorder import MetaInstancesRecorder

from .Chronoscope import Chronoscope
from .EasingCurve import EasingCurve
from glass.WeakSet import WeakSet
from ..GlassEngineConfig import GlassEngineConfig

import threading
import time


class Animation(metaclass=MetaInstancesRecorder):

    @MetaInstancesRecorder.init
    def __init__(
        self,
        target=None,
        property: str = "",
        from_=None,
        to=None,
        duration: float = 1,
        easing_curve: EasingCurve = EasingCurve.Linear,
        step: float = 0.01,
        loops: int = 1,
        go_back: bool = False,
        start_after_show: bool = True,
        running_callback=None,
        done_callback=None,
    ):
        self.target: object = target
        self.property: str = property
        self.from_: object = from_
        self.to: object = to
        self._duration: float = duration
        self._total_duration: float = 0
        self.__total_duration_dirty: bool = True
        self.step: float = step
        self._loops: int = loops
        self._go_back: bool = go_back
        self.start_after_show: bool = start_after_show
        self.easing_curve: EasingCurve = easing_curve
        self.running_callback = running_callback
        self.done_callback = done_callback

        self._timer = Chronoscope()
        self._running_thread = None
        self._wait_to_start: bool = False
        self._parents: WeakSet = WeakSet()

    @MetaInstancesRecorder.delete
    def __del__(self):
        pass

    def _start(self):
        if self._timer.status == Chronoscope.Status.Stop:
            self._running_thread = threading.Thread(
                target=self._run, args=(), daemon=True
            )
            self._running_thread.start()
        self._timer.start()
        self._wait_to_start: bool = False

    def start(self):
        if not GlassEngineConfig.is_first_shown and self.start_after_show:
            self._wait_to_start: bool = True
        else:
            self._start()

    def pause(self):
        self._timer.pause()
        self._wait_to_start: bool = False

    def stop(self, stop_value=None):
        self._running = False
        if self._running_thread is not None:
            if self._running_thread.is_alive():
                self._running_thread.join()

            self._running_thread = None

        self._timer.stop()
        if stop_value is None:
            stop_value = self.from_

        if self.target is not None and self.property:
            setattr(self.target, self.property, stop_value)

        self._wait_to_start: bool = False

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

        mapped_progress = self.easing_curve(progress)

        if self.target is not None and self.property:
            if self.from_ is None:
                self.from_ = getattr(self.target, self.property)

            value = self.from_ + mapped_progress * (self.to - self.from_)
            setattr(self.target, self.property, value)

        if self.running_callback is not None:
            self.running_callback(t)

    def go_to(self, t: float):
        self._timer.go_to(t)
        self._go_to(t)

    @property
    def duration(self):
        return self._duration

    @property
    def _total_duration_dirty(self) -> bool:
        return self.__total_duration_dirty

    @_total_duration_dirty.setter
    def _total_duration_dirty(self, dirty: bool):
        if self.__total_duration_dirty == dirty:
            return

        self.__total_duration_dirty = dirty
        if dirty:
            for parent in self._parents:
                parent._total_duration_dirty = True

    @duration.setter
    def duration(self, duration: float):
        self._duration = duration
        self._total_duration_dirty = True

    @property
    def loops(self):
        return self._loops

    @loops.setter
    def loops(self, loops: int):
        self._loops = loops
        self._total_duration_dirty = True

    @property
    def go_back(self) -> bool:
        return self._go_back

    @go_back.setter
    def go_back(self, go_back: bool):
        self._go_back = go_back
        self._total_duration_dirty = True

    @property
    def speed(self):
        return self._timer.speed

    @speed.setter
    def speed(self, speed: float):
        self._timer.speed = speed

    @property
    def status(self):
        return self._timer.status

    @property
    def total_duration(self):
        if self._total_duration_dirty:
            self._total_duration = self.duration * self.loops
            if self.go_back:
                self._total_duration *= 2

            self._total_duration_dirty = False

        return self._total_duration

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
            self._go_to(t)

            if self._running:
                dt = next_time - time.perf_counter()
                if dt > 0:
                    time.sleep(dt)

        t = self._timer.time()
        if self.done_callback is not None:
            self.done_callback(t)
        self._timer.stop()

    @classmethod
    def has_valid(cls):
        for animation in cls.all_instances:
            if animation.status != Chronoscope.Status.Stop:
                return True

        return False
