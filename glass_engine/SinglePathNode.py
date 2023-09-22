from .SceneNode import SceneNode
import glm

class SinglePathNode(SceneNode):

    def __init__(self, name:str=""):
        SceneNode.__init__(self, name)

    @property
    def parent(self)->SceneNode:
        for parent in self._parents:
            return parent
    
    @property
    def scene(self):        
        for scene in self._scenes:
            return scene
        
    @property
    def abs_scale(self)->glm.vec3:
        return SinglePathNode.__abs_scale(self)
    
    @property
    def abs_orientation(self)->glm.quat:
        return SinglePathNode.__abs_orientation(self)
    
    @property
    def abs_position(self)->glm.vec3:
        return SinglePathNode.__abs_position(self)

    @property
    def path(self)->list:
        if self.parent is None:
            return [self]
        
        path = self.parent.paths[0]
        path.append(self)
        return path
    
    @property
    def path_str(self)->str:
        if self.parent is None:
            return "/" + self.name
        
        path_str = self.parent.paths_str[0]
        return path_str + "/" + self.name

    @staticmethod
    def __abs_orientation(node:SceneNode)->glm.quat:
        try:
            parent = node.parents[0]
        except IndexError:
            return node._orientation.flat

        parent_abs_orientation = SinglePathNode.__abs_orientation(parent)
        return parent_abs_orientation * node._orientation.flat

    @staticmethod
    def __abs_position(node:SceneNode)->glm.vec3:
        try:
            parent = node.parents[0]
        except:
            return node._position.flat

        parent_abs_orientation = SinglePathNode.__abs_orientation(parent)
        parent_abs_scale = SinglePathNode.__abs_scale(parent)
        parent_abs_position = SinglePathNode.__abs_position(parent)
        
        return parent_abs_orientation * (parent_abs_scale * node._position.flat) + parent_abs_position

    @staticmethod
    def __abs_scale(node:SceneNode)->glm.vec3:
        try:
            parent = node.parents[0]
        except:
            return node._scale.flat
        
        parent_abs_scale = SinglePathNode.__abs_scale(parent)
        return parent_abs_scale * node._scale.flat

    def _add_as_child_callback(self)->None:
        len_parents = len(self._parents)
        i = 0
        for parent in self._parents:
            if i >= len_parents-1:
                break

            parent.remove_child(self)
            i += 1

        node = self
        while True:
            if len(node._parents) > 1:
                raise RuntimeError('SinglePathNode can only have one path to root')
            
            try:
                node = node._parents[0]
            except IndexError:
                break

        SceneNode._add_as_child_callback(self)