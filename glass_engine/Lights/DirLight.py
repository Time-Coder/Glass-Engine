from .Light import Light
from glass.utils import checktype
from glass.DictList import DictList
from glass.ShaderStorageBlock import ShaderStorageBlock

import glm

class DirLight(Light):
    pass

class FlatDirLight:

    @checktype
    def __init__(self, dir_light:DirLight):
        self.color = dir_light._color.flat
        self.brightness = dir_light._brightness
        self.ambient = dir_light._ambient.flat
        self.diffuse = dir_light._diffuse.flat
        self.specular = dir_light._specular.flat
        self.direction = glm.vec3(0, 1, 0)
        self.abs_orientation = glm.quat(1, 0, 0, 0)
        self.generate_shadows = dir_light.generate_shadows
        self.max_back_offset = 0

        self.depth_fbo = None
        self.depth_map_handle = 0
        self.depth_filter_fbo = None
        self.depth_filter = None
        self.need_update_depth_map = True
        
        self._source = dir_light
        dir_light._flats.add(self)

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
        return self.dir_lights.__iter__()

    @property
    def n_dir_lights(self):
        return len(self.dir_lights)