from abc import ABC, abstractmethod

from glass import RenderHint
from glass.utils import checktype, di

class Renderer(ABC):

    def __init__(self):
        self._render_hint = RenderHint()
        self._render_hint.depth_test = True
        self._camera_id = id(None)

    @property
    def camera(self): 
        return di(self._camera_id)

    @property
    def scene(self):        
        return self.camera.scene

    @property
    def render_hint(self):
        return self._render_hint
    
    @render_hint.setter
    @checktype
    def render_hint(self, render_hint:RenderHint):
        self._render_hint = render_hint
        
    def startup(self):
        pass

    @abstractmethod
    def render(self)->bool:
        pass
