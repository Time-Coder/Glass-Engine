from abc import ABC, abstractmethod

from glass import RenderHint
from glass.utils import checktype

from ..Filters import Filters

class Renderer(ABC):

    def __init__(self):
        self._render_hint = RenderHint()
        self._render_hint.depth_test = True
        self._filters = Filters()

    @property
    def render_hint(self):            
        return self._render_hint
    
    @render_hint.setter
    @checktype
    def render_hint(self, render_hint:RenderHint):
        self._render_hint = render_hint
    
    @property
    def filters(self):
        return self._filters
    
    @filters.setter
    @checktype
    def filters(self, filters:Filters):
        self._filters = filters
        
    @abstractmethod
    def startup(self, camera, scene)->bool:
        pass

    @abstractmethod
    def render(self, camera, scene)->bool:
        pass
