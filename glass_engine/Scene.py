from .SceneNode import SceneNode
from .Mesh import Mesh
from .Lights.PointLight import PointLights, PointLight, FlatPointLight
from .Lights.DirLight import DirLights, DirLight, FlatDirLight
from .Lights.SpotLight import SpotLights, SpotLight, FlatSpotLight
from .AffineTransform import AffineTransform

from .Fog import Fog
from .Background import Background

from glass.utils import quat_to_mat4, scale_to_mat4, translate_to_mat4
from glass import Instances

import glm
import time

class Scene:

    def __init__(self):
        self._root = SceneNode("root")
        self._root._scenes.add(self)

        self._all_meshes = {}
        self._backup_meshes = {}
        self._last_generated_meshes = set()

        self._fog = Fog()
        self._background = Background()
        self._dir_lights = DirLights()
        self._point_lights = PointLights()
        self._spot_lights = SpotLights()

        self.__anything_changed = False
        self._should_update_env_maps = False
        self._should_update_depth_maps = False

    def add(self, scene_node:SceneNode)->None:
        self._root.add_child(scene_node)

    def remove(self, scene_node:SceneNode)->None:
        self._root.remove_child(scene_node)

    @property
    def root(self):
        return self._root

    @property
    def background(self)->Background:
        return self._background

    @property
    def skybox(self):
        return self._background.skybox
    
    @skybox.setter
    def skybox(self, skybox):
        self._background.skybox = skybox

    @property
    def skydome(self):
        return self._background.skydome
    
    @skydome.setter
    def skydome(self, skydome):
        self._background.skydome = skydome

    @property
    def fog(self):
        return self._fog

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

        success = False
        for spot_light in self._spot_lights:
            if not spot_light.need_update_depth_map:
                spot_light.need_update_depth_map = True
                success = True

        if success:
            self._spot_lights.dirty = True

    def __clear_dirty(self, scene_node:SceneNode=None):
        if scene_node is None:
            scene_node = self._root

        if self not in scene_node._transform_dirty and \
           self not in scene_node._children_transform_dirty:
            return
        
        if self in scene_node._transform_dirty:
            scene_node._transform_dirty.remove(self)

        if self in scene_node._children_transform_dirty:
            for child in scene_node._children_transform_dirty[self]:
                self.__clear_dirty(child)
            del scene_node._children_transform_dirty[self]
    
    def __trav(self, scene_node:SceneNode,
               current_quat:glm.quat,
               current_mat:glm.mat4,
               current_path:str):
        
        if self not in self._root._transform_dirty and \
           self not in self._root._children_transform_dirty:
            return

        new_quat = current_quat * scene_node.orientation
        new_mat = current_mat * translate_to_mat4(scene_node.position) * \
                                quat_to_mat4(scene_node.orientation) * \
                                scale_to_mat4(scene_node.scale)
        new_path = current_path + "/" + scene_node.name

        if self in scene_node._transform_dirty:
            if isinstance(scene_node, Mesh):
                mesh = scene_node
                if mesh not in self._all_meshes:
                    self._all_meshes[mesh] = {}

                if new_path not in self._all_meshes[mesh]:
                    self._all_meshes[mesh][new_path] = AffineTransform()

                self._all_meshes[mesh][new_path]["affine_transform_row0"] = glm.vec4(new_mat[0][0], new_mat[1][0], new_mat[2][0], new_mat[3][0])
                self._all_meshes[mesh][new_path]["affine_transform_row1"] = glm.vec4(new_mat[0][1], new_mat[1][1], new_mat[2][1], new_mat[3][1])
                self._all_meshes[mesh][new_path]["affine_transform_row2"] = glm.vec4(new_mat[0][2], new_mat[1][2], new_mat[2][2], new_mat[3][2])
                self.__anything_changed = True
            elif isinstance(scene_node, SpotLight):
                spot_light = None
                if new_path not in self._spot_lights:
                    spot_light = FlatSpotLight(scene_node)
                    self._spot_lights[new_path] = spot_light
                else:
                    spot_light = self._spot_lights[new_path]
                    spot_light.update(scene_node)

                spot_light.abs_position = new_mat[3].xyz
                spot_light.direction = new_quat * glm.vec3(0, 1, 0)
                self._spot_lights.dirty = True

                self.__anything_changed = True
                self._spot_lights_changed = True
            elif isinstance(scene_node, PointLight):
                point_light = None
                if new_path not in self._point_lights:
                    point_light = FlatPointLight(scene_node)
                    self._point_lights[new_path] = point_light
                else:
                    point_light = self._point_lights[new_path]
                    point_light.update(scene_node)

                point_light.abs_position = new_mat[3].xyz
                self._point_lights.dirty = True

                self.__anything_changed = True
                self._point_lights_changed = True
            elif isinstance(scene_node, DirLight):
                dir_light = None
                if new_path not in self._dir_lights:
                    dir_light = FlatDirLight(scene_node)
                    self._dir_lights[new_path] = dir_light
                else:
                    dir_light = self._dir_lights[new_path]
                    dir_light.update(scene_node)

                dir_light.direction = new_quat * glm.vec3(0, 1, 0)
                dir_light.abs_orientation = new_quat
                self._dir_lights.dirty = True

                self.__anything_changed = True
                self._dir_lights_changed = True

        if self in scene_node._children_transform_dirty:
            for child in scene_node._children_transform_dirty[self]:
                self.__trav(child, new_quat, new_mat, new_path)

    def __collect_render_infos(self):
        if self not in self._root._transform_dirty and \
           self not in self._root._children_transform_dirty:
            return
        
        self.__trav(self._root, glm.quat(), glm.mat4(), "")
        if self.__anything_changed:
            self.__update_env_maps()
            self.__update_depth_maps()
            self.__anything_changed = False
            self._should_update_env_maps = False
            self._should_update_depth_maps = False
        else:
            if self._should_update_env_maps:
                self.__update_env_maps()
                self._should_update_env_maps = False

            if self._should_update_depth_maps:
                self.__update_depth_maps()
                self._should_update_depth_maps = False

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
                    if key == path_str or key.starts_with(path_str + "/"):
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
                if key == path_str or key.starts_with(path_str + "/"):
                    should_remove_keys.append(key)

            for key in should_remove_keys:
                lights[key].before_del()
                del lights[key]

    def _remove_paths_prefix(self, paths_str:set):
        for path_str in paths_str:
            Scene.__remove_path_prefix(self._all_meshes, path_str)
            Scene.__remove_path_prefix(self._dir_lights, path_str)
            Scene.__remove_path_prefix(self._point_lights, path_str)
            Scene.__remove_path_prefix(self._spot_lights, path_str)
