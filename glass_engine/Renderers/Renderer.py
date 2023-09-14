from abc import ABC, abstractmethod

from glass.utils import di

class Renderer(ABC):

    def __init__(self):
        self._camera_id = id(None)

    @property
    def camera(self): 
        return di(self._camera_id)

    @property
    def scene(self):        
        return self.camera.scene
        
    def startup(self):
        pass

    @abstractmethod
    def render(self)->bool:
        pass
