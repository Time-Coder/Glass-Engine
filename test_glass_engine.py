from glass_engine import *
from glass_engine.Geometries import *
from glass_engine.PostProcessEffects import *
from glass_engine.Animations import Animation

scene, camera, light, floor = SceneRoam()

sphere = Sphere()
node = SceneNode()
node.add_child(sphere)
scene.add(node)
node.position.z = 1

# animation = Animation(target=node.position, attr="z", end_value=5, loops=10000)
# animation.start()

camera.screen.show()