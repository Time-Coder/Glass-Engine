from enum import Enum
import time

class Chronoscope:

    class Status(Enum):
        Stop = 0
        Running = 1
        Paused = 2

    def __init__(self):
        self._segment_start_time = 0
        self._segment_speed = 1
        self._end_time = 0

        self._status:Chronoscope.Status = Chronoscope.Status.Stop
        self._speed:float = 1

    def start(self):
        if self._status == Chronoscope.Status.Running:
            return

        self._segment_start_time = time.perf_counter()
        self._segment_speed = self._speed
        self._status = Chronoscope.Status.Running

    def stop(self):
        if self._status == Chronoscope.Status.Stop:
            return
        
        self._end_time = 0
        self._status = Chronoscope.Status.Stop

    def pause(self):
        if self._status != Chronoscope.Status.Running:
            return
        
        duration = self._segment_speed * (time.perf_counter() - self._segment_start_time)
        self._end_time += duration
        self._status = Chronoscope.Status.Paused

    def goto(self, t:float):
        self._segment_start_time = time.perf_counter()
        self._segment_speed = self._speed
        self._end_time = t

        if self._status == Chronoscope.Status.Stop:
            self._status = Chronoscope.Status.Paused

    @property
    def status(self):
        return self._status
    
    @status.setter
    def status(self, status):
        if self._status == status:
            return
        
        if self._status == Chronoscope.Status.Stop:
            if status == Chronoscope.Status.Paused:
                self._status = Chronoscope.Status.Paused
            else:
                self.start()
        elif self._status == Chronoscope.Status.Paused:
            if status == Chronoscope.Status.Stop:
                self.stop()
            else:
                self.start()
        elif self._status == Chronoscope.Status.Running:
            if status == Chronoscope.Status.Paused:
                self.pause()
            else:
                self.stop()

    @property
    def speed(self)->float:
        return self._speed

    @speed.setter
    def speed(self, speed:float):
        if self._speed == speed:
            return
        
        self._speed = speed

        if self._status != Chronoscope.Status.Running:
            return

        duration = self._segment_speed * (time.perf_counter() - self._segment_start_time)
        self._end_time += duration

        self._segment_start_time = time.perf_counter()
        self._segment_speed = self._speed

    def time(self)->float:
        if self._status != Chronoscope.Status.Running:
            return self._end_time
        
        duration = self._segment_speed * (time.perf_counter() - self._segment_start_time)
        return self._end_time + duration
    