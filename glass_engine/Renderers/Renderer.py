from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from ..Camera import Camera
    from ..Scene import Scene

class Renderer(ABC):

    def __init__(self):
        self._camera:Optional[Camera] = None

    @property
    def camera(self)->Optional[Camera]:
        return self._camera

    @property
    def scene(self)->Scene:
        return self.camera.scene

    @property
    def screen(self):
        return self.camera.screen

    def startup(self):
        pass

    @abstractmethod
    def render(self) -> bool:
        pass
