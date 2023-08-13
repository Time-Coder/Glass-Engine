from .Scene import Scene
from .Camera import Camera
from .Geometries.Floor import Floor
from .Lights.DirLight import DirLight

def BasicScene(add_floor=True):
    scene = Scene()

    camera = Camera()
    camera.position.y = -5
    camera.position.z = 1.7
    camera.pitch = -10
    scene.add(camera)

    floor = None
    if add_floor:
        floor = Floor()
        scene.add(floor)

    dir_light = DirLight()
    dir_light.pitch = -45
    dir_light.yaw = 45
    scene.add(dir_light)

    return scene, camera, dir_light, floor