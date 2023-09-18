import glm
import math
import uuid

from glass.utils import checktype
from glass.DictList import DictList
from glass.WeakSet import WeakSet
from glass.WeakDict import WeakDict
from .callback_vec import callback_quat, callback_vec3

class SceneNode:

    @checktype
    def __init__(self, name:str=""):
        if name:
            self._name = name
        else:
            self._name = self.__class__.__name__ + "_" + str(uuid.uuid1())

        self._position = callback_vec3(0, 0, 0, callback=self._set_dirty)
        self._orientation = callback_quat(1, 0, 0, 0, callback=self._update_yaw_pitch_roll)
        self._scale = callback_vec3(1, 1, 1, callback=self._set_dirty)
        self._yaw_pitch_roll = glm.vec3(0, 0, 0)

        self._parents = DictList(weak_ref=True)
        self._children = DictList()
        self._scenes = WeakSet()
        self._transform_dirty = WeakSet()
        self._children_transform_dirty = WeakDict(weak_ref_keys=True, weak_ref_values=False)
        self._should_update_yaw_pitch_roll = True

        self._propagation_props = {}
        self._block_propagation = set()
        self._propagation_props["visible"] = True

    @property
    def visible(self):
        return self.propagation_prop("visible")
    
    @visible.setter
    @checktype
    def visible(self, visible:bool):
        self.set_propagation_prop("visible", visible)

    def hide(self):
        self.visible = False

    def show(self):
        self.visible = True

    @property
    def scenes(self):
        return self._scenes

    @property
    def parents(self):
        return self._parents

    @property
    def children(self):
        return self._children
    
    def block_propagation(self, name:str, flag:bool=True):
        if flag:
            self._block_propagation.add(name)
        elif name in self._block_propagation:
            self._block_propagation.remove(name)

    def propagation_prop(self, name:str):
        if name not in self._propagation_props:
            return None
        
        return self._propagation_props[name]

    def set_propagation_prop(self, name:str, value, callback=None, args:tuple=(), kwargs:dict={}):
        parent_queues = [self]
        is_self_set = False
        while parent_queues:
            parent = parent_queues.pop()
            if name in parent._block_propagation:
                child_queues = [parent]
                while child_queues:
                    child = child_queues.pop()
                    child._propagation_props[name] = value
                    if callback is not None:
                        callback(child, *args, **kwargs)
                    child_queues.extend(child._children)
                    if child is self:
                        is_self_set = True
            else:
                parent_queues.extend(parent.parents)

        if not is_self_set:
            child_queues = [self]
            while child_queues:
                child = child_queues.pop()
                child._propagation_props[name] = value
                if callback is not None:
                    callback(child, *args, **kwargs)
                child_queues.extend(child._children)

    def has_parent(self, parent):
        return (parent in self._parents)

    def has_child(self, child):
        return (child in self._children)

    def add_child(self, node):
        if node.has_parent(self):
            return

        if node.name in self._children:
            if self._children[node.name] is not node:
                old_name = node.name
                i = 1
                new_name = f"{old_name}-{i}"
                while new_name in self._children:
                    i += 1
                    new_name = f"{old_name}-{i}"
                node.name = new_name
            else:
                return

        if self.name in node._parents:
            if node._parents[self.name] is not self:
                raise NameError("already has one parent named '" + self.name + "'")
            else:
                return

        node._parents[self.name] = self
        self._children[node.name] = node
        node._add_as_child_callback()

        node._scenes.update(self._scenes)
        self._set_dirty(False, True)

    def remove_child(self, child):
        detached_node = None
        paths_prefix = None
        if isinstance(child, str):
            name = child
            if name in self._children:
                detached_node = self._children[name]
                paths_prefix = detached_node.paths_str
                del self._children[name]
                del detached_node._parents[self.name]
        else:
            try:
                self._children.remove(child)
                paths_prefix = child.paths_str
                child._parents.remove(self)
                detached_node = child
            except ValueError:
                pass

        if detached_node is None:
            return None
        
        detached_node._update_scenes()
        for scene in self.scenes:
            scene._remove_paths_prefix(paths_prefix)

    def clear_children(self):
        children_names = self.children_names
        for child_name in children_names:
            self.remove_child(child_name)

    @property
    def children_names(self):
        return list(self._children.keys())

    def __hash__(self):
        return id(self)

    @checktype
    def __getitem__(self, name:(str,int)):
        if isinstance(name, str):
            if name not in self._children:
                self.add_child(SceneNode(name))
        else:
            while name >= len(self._children):
                self.add_child(SceneNode())

        return self._children[name]

    @checktype
    def __setitem__(self, name:str, node):
        if name in self._children:
            if self._children[name] is node:
                return
            self.remove_child(name)

        node.name = name
        self.add_child(node)

    @checktype
    def __delitem__(self, name:str):
        self.remove_child(name)

    def __to_string(self, indent):
        result = indent * "  " + self.name
        for child in self._children:
            result += ("\n" + child.__to_string(indent+1))
        return result

    def __repr__(self):
        return self.__to_string(0)

    @property
    def name(self):
        return self._name

    @name.setter
    @checktype
    def name(self, name:str):
        if name == self._name:
            return

        if not self._parents:
            self._name = name
            return

        for parent in self._parents:
            if name in parent._children:
                raise NameError("parent node already has one child named '" + name + "'")

            del parent._children[self._name]
            parent._children[name] = self

        self._name = name

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position:glm.vec3):
        self._position.x = position.x
        self._position.y = position.y
        self._position.z = position.z

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, scale:(glm.vec3, float)):
        if isinstance(scale, (int,float)):
            self._scale.x = scale
            self._scale.y = scale
            self._scale.z = scale
        else:
            self._scale.x = scale.x
            self._scale.y = scale.y
            self._scale.z = scale.z

    @property
    def orientation(self):
        return self._orientation

    @orientation.setter
    def orientation(self, orientation:glm.quat):
        self._orientation.w = orientation.w
        self._orientation.x = orientation.x
        self._orientation.y = orientation.y
        self._orientation.z = orientation.z

    def _update_yaw_pitch_roll(self):
        if not self._should_update_yaw_pitch_roll:
            return
        
        q0 = self._orientation.w
        q1 = self._orientation.x
        q2 = self._orientation.y
        q3 = self._orientation.z
        self._yaw_pitch_roll[0] = math.atan2(2 * (q0*q3 - q1*q2), 1 - 2 * (q1*q1 + q3*q3))/math.pi*180
        self._yaw_pitch_roll[1] = math.asin(2 * (q0*q1 + q2*q3))/math.pi*180
        self._yaw_pitch_roll[2] = math.atan2(2 * (q0*q2 - q1*q3), 1 - 2 * (q1*q1 + q2*q2))/math.pi*180

        self._set_dirty()

    def _update_orientation(self):
        yaw = self._yaw_pitch_roll[0]/180*math.pi
        pitch = self._yaw_pitch_roll[1]/180*math.pi
        roll = self._yaw_pitch_roll[2]/180*math.pi

        quat1 = glm.quat(math.cos(yaw / 2), 0, 0, math.sin(yaw / 2))
        quat2 = glm.quat(math.cos(pitch / 2), math.sin(pitch / 2), 0, 0)
        quat3 = glm.quat(math.cos(roll / 2), 0, math.sin(roll / 2), 0)

        self._should_update_yaw_pitch_roll = False
        self.orientation = quat1 * quat2 * quat3
        self._should_update_yaw_pitch_roll = True

        self._set_dirty()

    @property
    def yaw(self):
        return self._yaw_pitch_roll[0]

    @yaw.setter
    @checktype
    def yaw(self, new_yaw:float):
        self._yaw_pitch_roll[0] = new_yaw
        self._update_orientation()

    @property
    def pitch(self):
        return self._yaw_pitch_roll[1]

    @pitch.setter
    @checktype
    def pitch(self, new_pitch:float):
        self._yaw_pitch_roll[1] = new_pitch
        self._update_orientation()

    @property
    def roll(self):
        return self._yaw_pitch_roll[2]

    @roll.setter
    @checktype
    def roll(self, new_roll:float):
        self._yaw_pitch_roll[2] = new_roll
        self._update_orientation()

    @staticmethod
    def path_str(node_path):
        path = ""
        for node in node_path:
            path += ("/" + node.name)

        return path
    
    @property
    def paths(self):
        if not self.parents:
            return [[self]]
        
        all_paths = []
        for parent in self.parents:
            parent_paths = parent.paths
            for path in parent_paths:
                path.append(self)
            all_paths.extend(parent_paths)

        return all_paths
    
    @property
    def paths_str(self):
        if not self.parents:
            return ["/" + self.name]
        
        all_paths_str = []
        for parent in self.parents:
            parent_paths_str = parent.paths_str
            for i, path_str in enumerate(parent_paths_str):
                parent_paths_str[i] = path_str + "/" + self.name
            all_paths_str.extend(parent_paths_str)

        return all_paths_str
    
    def _add_as_child_callback(self):
        for child in self._children:
            child._add_as_child_callback()

    def _clear_dirty_scenes(self, scenes):
        for scene in scenes:
            if scene in self._transform_dirty:
                self._transform_dirty.remove(scene)

            if scene in self._children_transform_dirty:
                del self._children_transform_dirty[scene]

        for child in self._children:
            child._clear_dirty_scenes(scenes)

    def _update_scenes(self):
        old_scenes = self._scenes
        self._scenes = WeakSet()
        for parent in self.parents:
            self._scenes.update(parent._scenes)

        self._clear_dirty_scenes(old_scenes - self._scenes)

    def _set_upstream_dirty(self, scenes):
        for parent in self.parents:
            for scene in scenes:
                if scene not in parent._children_transform_dirty:
                    parent._children_transform_dirty[scene] = set()

                parent._children_transform_dirty[scene].add(self)

            parent._set_upstream_dirty(scenes)

    def _set_transform_dirty(self, scenes):
        return False

    def _set_dirty(self, self_transform_dirty=True, upstream=True, scenes=None):
        if scenes is None:
            scenes = self._scenes

        self_transform_dirty_set = False
        if self_transform_dirty:
            self_transform_dirty_set = self._set_transform_dirty(scenes)

        for scene in scenes:
            if self._children:
                if scene not in self._children_transform_dirty:
                    self._children_transform_dirty[scene] = set()

                for child in self._children:
                    self._children_transform_dirty[scene].add(child)
                    child._set_dirty(True, False, scenes)
            elif scene in self._children_transform_dirty:
                del self._children_transform_dirty[scene]

        if upstream and (self_transform_dirty_set or self._children):
            self._set_upstream_dirty(scenes)
