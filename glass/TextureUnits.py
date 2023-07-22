from .GLConfig import GLConfig

class TextureUnits:
    def __init__(self):
        self._unit_texture_map = {}
        self._texture_unit_map = {}

    def __getitem__(self, unit:int)->tuple:
        key = (GLConfig.buffered_current_context, unit)
        if key not in self._unit_texture_map:
            return None
        
        return self._unit_texture_map[key]
    
    def __setitem__(self, unit:int, texture:tuple):
        context = GLConfig.buffered_current_context

        unit_key = (context, unit)
        if unit_key in self._unit_texture_map:
            old_texture = self._unit_texture_map[unit_key]
            if old_texture != texture:
                del self._texture_unit_map[context, old_texture]

        texture_key = (context, texture)
        if texture_key in self._texture_unit_map:
            old_unit = self._texture_unit_map[texture_key]
            if old_unit != unit:
                del self._unit_texture_map[context, old_unit]

        self._unit_texture_map[unit_key] = texture
        self._texture_unit_map[texture_key] = unit

    @property
    def current_texture(self):
        return self[GLConfig.active_texture_unit]
    
    @current_texture.setter
    def current_texture(self, texture:tuple):
        self[GLConfig.active_texture_unit] = texture

    def unit_of_texture(self, texture:tuple)->int:
        key = (GLConfig.buffered_current_context, texture)
        if key not in self._texture_unit_map:
            return None
        
        return self._texture_unit_map[key]
    
    @property
    def available_unit(self):
        context = GLConfig.buffered_current_context

        for i in range(GLConfig.max_texture_units):
            key = (context, i)
            if key not in self._unit_texture_map:
                return i
            
            if self._unit_texture_map[key] == 0:
                return i
            
        return None

TextureUnits = TextureUnits()
