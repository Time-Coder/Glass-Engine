import glm

class callback_vec3(glm.vec3):

    def __init__(self, x:float=0.0, y:float=0.0, z:float=0.0, callback=None):
        glm.vec3.__init__(self, x, y, z)
        self.__dict__["_callback"] = callback
    
    def __deepcopy__(self, memo):
        return self.flat
    
    def __copy__(self):
        return self.flat

    @property
    def flat(self):
        return glm.vec3(self.x, self.y, self.z)

    def __setattr__(self, name:str, value):
        super().__setattr__(name, value)
        if name in "xyzrgbstp" and self._callback is not None:
            self._callback()

    def __rmul__(self, other):
        return other * self.flat
    
class callback_vec4(glm.vec4):

    def __init__(self, x:float=0.0, y:float=0.0, z:float=0.0, w:float=1.0, callback=None):
        glm.vec4.__init__(self, x, y, z, w)
        self.__dict__["_callback"] = callback
    
    def __deepcopy__(self, memo):
        return self.flat

    def __copy__(self):
        return self.flat

    @property
    def flat(self):
        return glm.vec4(self.x, self.y, self.z, self.w)

    def __setattr__(self, name:str, value):
        super().__setattr__(name, value)
        if name in "xyzwrgbastpq" and self._callback is not None:
            self._callback()

    def __rmul__(self, other):
        return other * self.flat

class callback_quat(glm.quat):
    def __init__(self, w:float=1.0, x:float=0.0, y:float=0.0, z:float=0.0, callback=None):
        glm.quat.__init__(self, w, x, y, z)
        self.__dict__["_callback"] = callback
    
    @property
    def flat(self):
        return glm.quat(self.w, self.x, self.y, self.z)

    def __deepcopy__(self, memo):
        return self.flat
    
    def __copy__(self):
        return self.flat

    def __setattr__(self, name:str, value):
        super().__setattr__(name, value)
        if name in "wxyz" and self._callback is not None:               
            self._callback()

    def __mul__(self, other):
        return self.flat * other
    
    def __rmul__(self, other):
        return other * self.flat
    