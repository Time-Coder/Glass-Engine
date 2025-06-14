from abc import ABC, abstractmethod


class Renderer(ABC):

    def __init__(self):
        self._camera = None

    @property
    def camera(self):
        return self._camera

    @property
    def scene(self):
        return self.camera.scene

    @property
    def screen(self):
        return self.camera.screen

    def startup(self):
        pass

    @abstractmethod
    def render(self) -> bool:
        pass
