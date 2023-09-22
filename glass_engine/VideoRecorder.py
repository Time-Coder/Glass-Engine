import numpy as np
import queue
import threading
import math
import cv2
import time

from glass.utils import di

def convert_to_image(data:np.ndarray, viewport:tuple)->np.ndarray:
    if viewport[0] != 0 or \
       viewport[1] != 0 or \
       viewport[2] != data.shape[1] or \
       viewport[3] != data.shape[0]:
        width_pad = max(viewport[0] + viewport[2] - data.shape[1], 0)
        height_pad = max(viewport[1] + viewport[3] - data.shape[0], 0)
        if len(data.shape) == 2:
            if width_pad > 0 or height_pad > 0:
                data = np.pad(data, ((height_pad,0), (0,width_pad)))
            data = data[viewport[1]:viewport[1]+viewport[3], viewport[0]:viewport[0]+viewport[2]]
        else:
            if width_pad > 0 or height_pad > 0:
                data = np.pad(data, ((height_pad,0), (0,width_pad), (0, 0)))
            data = data[viewport[1]:viewport[1]+viewport[3], viewport[0]:viewport[0]+viewport[2], :]

    image = data
    if "float" in str(data.dtype):
        image = np.clip(255*data, 0, 255)

    image = image.astype(np.uint8)
    image = cv2.flip(image, 0)

    channels = (1 if len(image.shape) < 3 else image.shape[2])
    if channels == 3:
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    elif channels == 4:
        image = cv2.cvtColor(image, cv2.COLOR_RGBA2BGR)

    return image

class VideoRecorder:
    def __init__(self, screen, file_name:str, fourcc:list, viewport:tuple, fps:(float,int))->None:
        self._screen_id = id(screen)

        self._file_name = file_name
        self._fourcc = fourcc

        self._last_frame = None
        self._frame_queue = queue.Queue()
        self._stop_time = float("inf")
        self._writing_thread = threading.Thread(target=self._writing_loop)
        self._started = False
        if viewport is not None and fps is not None:
            self._start(viewport, fps)

    def _start(self, viewport, fps):
        if self._started:
            return
        
        if fps == 0:
            fps = 24

        self._viewport = viewport
        self._dt = 1/fps
        self._cv_video_writer = cv2.VideoWriter(self._file_name, self._fourcc, fps, (viewport[2], viewport[3]))
        self._start_time = time.time()
        self._writing_thread.start()
        self._started = True

    def __del__(self)->None:
        self.stop()

    def stop(self)->None:
        if math.isinf(self._stop_time):
            self._stop_time = time.time()
            self._frame_queue.put(None)

    def _writing_loop(self)->None:
        t = self._start_time
        while t < self._stop_time:
            frame = self._frame_queue.get()
            if frame is None:
                if self._last_frame is None:
                    break

                while t < self._stop_time:
                    self._cv_video_writer.write(self._last_frame[1])
                    t += self._dt

                break
            image = convert_to_image(frame[1], self._viewport)

            if self._last_frame is None:
                self._last_frame = (frame[0], image)

            while t <= min(self._stop_time, frame[0]):
                self._cv_video_writer.write(self._last_frame[1])
                t += self._dt

            self._last_frame = (frame[0], image)

        self._cv_video_writer.release()
        try:
            screen = di(self._screen_id)
            screen._screen_video_writers.remove(self)
        except:
            pass