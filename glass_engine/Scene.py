from .SceneNode import SceneNode
from .Mesh import Mesh
from .Lights.PointLight import PointLights, PointLight, FlatPointLight
from .Lights.DirLight import DirLights, DirLight, FlatDirLight
from .Lights.SpotLight import SpotLights, SpotLight, FlatSpotLight
from .Transform import Transform
from .SkyBox import SkyBox
from .SkyDome import SkyDome

from glass.utils import checktype, vec4_to_quat, quat_to_vec4
from glass import Instances, samplerCube

import glm
import numpy as np
import time

class Scene:
    def __init__(self):
        self._root = SceneNode("root")
        self._root._scenes.add(self)

        self._all_meshes = {}
        self._backup_meshes = {}
        self._last_generated_meshes = set()

        self._skybox = SkyBox()
        self._skydome = SkyDome()
        self._point_lights = PointLights()
        self._dir_lights = DirLights()
        self._spot_lights = SpotLights()

        self.__anything_changed = False

    @checktype
    def add(self, object:SceneNode):
        self._root.add_child(object)

    @property
    def root(self):
        return self._root

    @property
    def skybox(self):
        return self._skybox
    
    @skybox.setter
    def skybox(self, skybox_map:samplerCube):
        self._skybox.skybox_map = skybox_map
    
    @property
    def skydome(self):
        return self._skydome
    
    @skydome.setter
    @checktype
    def skydome(self, image:(str,np.ndarray)):
        self._skydome.skydome_map = image

    def __update_env_maps(self, scene_node:SceneNode=None):
        if scene_node is None:
            scene_node = self._root

        if isinstance(scene_node, Mesh) and scene_node.material.auto_update_env_map:
            scene_node.material.update_env_map()

        for child in scene_node.children:
            self.__update_env_maps(child)

    def __update_depth_maps(self):
        success = False
        for point_light in self._point_lights:
            if not point_light.need_update_depth_map:
                point_light.need_update_depth_map = True
                success = True

        if success:
            self._point_lights.dirty = True

        for spot_light in self._spot_lights:
            if not spot_light.need_update_depth_map:
                spot_light.need_update_depth_map = True
                success = True

        if success:
            self._spot_lights.dirty = True

    def __clear_dirty(self, scene_node:SceneNode=None):
        if scene_node is None:
            scene_node = self._root

        if self not in scene_node._transform_dirty and self not in scene_node._children_transform_dirty:
            return
        
        if self in scene_node._transform_dirty:
            scene_node._transform_dirty.remove(self)

        if self in scene_node._children_transform_dirty:
            for child in scene_node._children_transform_dirty[self]:
                self.__clear_dirty(child)
            del scene_node._children_transform_dirty[self]
    
    def __trav(self, scene_node:SceneNode, current_instance:Transform, current_path:str):
        if self not in self._root._transform_dirty and self not in self._root._children_transform_dirty:
            return

        new_instance = Transform()

        quat = vec4_to_quat(current_instance.abs_orientation)
        new_instance.abs_position = quat * scene_node.position + current_instance.abs_position
        quat = quat * scene_node.orientation
        new_instance.abs_orientation = quat_to_vec4(quat)
        new_instance.abs_scale = current_instance.abs_scale * scene_node.scale

        new_path = current_path + "/" + scene_node.name

        if self in scene_node._transform_dirty:
            if isinstance(scene_node, Mesh):
                mesh = scene_node
                if mesh not in self._all_meshes:
                    self._all_meshes[mesh] = {}

                if new_path in self._all_meshes[mesh]:
                    self._all_meshes[mesh][new_path].update(new_instance)
                else:
                    self._all_meshes[mesh][new_path] = new_instance
                self.__anything_changed = True
            elif isinstance(scene_node, SpotLight):
                spot_light = FlatSpotLight(scene_node)
                spot_light.abs_position = new_instance.abs_position
                spot_light.direction = quat * glm.vec3(0, 1, 0)
                if new_path in self._spot_lights:
                    scene_node._flats.remove(self._spot_lights[new_path])
                self._spot_lights[new_path] = spot_light
                self.__anything_changed = True
                self._spot_lights_changed = True
            elif isinstance(scene_node, PointLight):
                point_light = FlatPointLight(scene_node)
                point_light.abs_position = new_instance.abs_position
                if new_path in self._point_lights:
                    scene_node._flats.remove(self._point_lights[new_path])
                self._point_lights[new_path] = point_light
                self.__anything_changed = True
                self._point_lights_changed = True
            elif isinstance(scene_node, DirLight):
                dir_light = FlatDirLight(scene_node)
                dir_light.direction = quat * dir_light.direction
                dir_light.abs_orientation = quat
                if new_path in self._dir_lights:
                    scene_node._flats.remove(self._dir_lights[new_path])
                self._dir_lights[new_path] = dir_light
                self.__anything_changed = True
                self._dir_lights_changed = True

        if self in scene_node._children_transform_dirty:
            for child in scene_node._children_transform_dirty[self]:
                self.__trav(child, new_instance, new_path)

    def __collect_render_infos(self):
        if self not in self._root._transform_dirty and self not in self._root._children_transform_dirty:
            return
        
        self.__trav(self._root, Transform(), "")
        if self.__anything_changed:
            self.__update_env_maps()
            self.__update_depth_maps()
            self.__anything_changed = False

        self.__clear_dirty()
        for mesh in self._all_meshes:
            if mesh not in self._backup_meshes:
                assert isinstance(self._all_meshes[mesh], dict)
                self._backup_meshes[mesh] = Instances(self._all_meshes[mesh])
                self._all_meshes[mesh] = self._backup_meshes[mesh]
            elif isinstance(self._all_meshes[mesh], dict):
                self._backup_meshes[mesh].update(self._all_meshes[mesh])
                self._all_meshes[mesh] = self._backup_meshes[mesh]

    @property
    def dir_lights(self):
        self.__collect_render_infos()
        return self._dir_lights
    
    @property
    def point_lights(self):
        self.__collect_render_infos()
        return self._point_lights
    
    @property
    def spot_lights(self):
        self.__collect_render_infos()
        return self._spot_lights
    
    @property
    def all_meshes(self):
        self.__collect_render_infos()
        return self._all_meshes
    
    def generate_meshes(self, seconds:float=0.01):
        generating_meshes = set()
        for mesh in self.all_meshes.keys():
            if mesh.is_generating:
                generating_meshes.add(mesh)
        
        if not generating_meshes:
            return False

        if self._last_generated_meshes >= generating_meshes:
            self._last_generated_meshes.clear()

        start_time = time.time()
        overtime = False
        while True:
            for mesh in (generating_meshes - self._last_generated_meshes):
                mesh.generate()
                current_time = time.time()
                self._last_generated_meshes.add(mesh)

                if current_time - start_time > seconds:
                    overtime = True
                    break

            if overtime:
                break
            
            self._last_generated_meshes.clear()
        
        self.__anything_changed = True
        return True
    
    @staticmethod
    def __remove_path_prefix(instance_map, path_str):
        if isinstance(instance_map, dict):
            should_remove_meshes = []
            for mesh, instances in instance_map.items():
                should_remove_keys = []
                for key in instances.keys():
                    if key.starts_with(path_str):
                        should_remove_keys.append(key)
                
                if len(should_remove_keys) == len(instances):
                    should_remove_meshes.append(mesh)
                else:
                    for key in should_remove_keys:
                        del instances[key]

            for mesh in should_remove_meshes:
                del instance_map[mesh]
        else:
            lights = instance_map
            should_remove_keys = []
            for key in lights.keys():
                if key.starts_with(path_str):
                    should_remove_keys.append(key)

            for key in should_remove_keys:
                lights[key]._source._flats.remove(lights[key])
                del lights[key]

    def _remove_paths_prefix(self, paths_str:set):
        for path_str in paths_str:
            Scene.__remove_path_prefix(self._all_meshes, path_str)
            Scene.__remove_path_prefix(self._dir_lights, path_str)
            Scene.__remove_path_prefix(self._point_lights, path_str)
            Scene.__remove_path_prefix(self._spot_lights, path_str)
