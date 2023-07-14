from .SceneNode import SceneNode

class Entity(SceneNode):

    def _set_transform_dirty(self, scenes):
        self._transform_dirty.update(scenes)
        return True