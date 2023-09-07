from .Light import Light, FlatLight
from glass.DictList import DictList
from glass.ShaderStorageBlock import ShaderStorageBlock

import glm

class DirLight(Light):
    pass

class FlatDirLight(FlatLight):

    def __init__(self, dir_light:DirLight):
        self.direction = glm.vec3(0, 1, 0)
        self.abs_orientation = glm.quat(1, 0, 0, 0)
        self.max_back_offset = 0
        FlatLight.__init__(self, dir_light)

class DirLights(ShaderStorageBlock.HostClass):

    def __init__(self):
        ShaderStorageBlock.HostClass.__init__(self)
        self.dir_lights = DictList()

    def __getitem__(self, key:(str,int)):
        return self.dir_lights[key]
    
    @ShaderStorageBlock.HostClass.not_const
    def __setitem__(self, key:(str,int), dir_light:FlatDirLight):
        self.dir_lights[key] = dir_light

    @ShaderStorageBlock.HostClass.not_const
    def __delitem__(self, key:(str,int)):
        del self.dir_lights[key]

    def __contains__(self, path_str:str):
        return (path_str in self.dir_lights)
    
    def __len__(self):
        return len(self.dir_lights)
    
    def __iter__(self):
        return iter(self.dir_lights)
    
    def keys(self):
        return self.dir_lights.keys()

    @property
    def n_dir_lights(self):
        return len(self.dir_lights)