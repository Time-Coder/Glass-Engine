from glass_engine import *
from glass_engine.Geometries import *
from glass_engine.Manipulators import Manipulator

scene, camera, dir_light, floor = SceneRoam()
scene.skydome = "workspace/assets/skydomes/sunflowers_puresky_4k.exr"
dir_light.generate_shadows = False

model = Model("workspace/assets/models/big_things/ship_pinnace_4k.gltf/ship_pinnace_4k.gltf")
model["root"].scale = 0.1
model["root"].pitch = 90
scene.add(model)

floor.material.shading_model = Material.ShadingModel.NoShading
floor.material.emission_map = "workspace/glsl/Shadertoys/ForkForkedWatpancake89641.glsl"

def toggle_DOF(key):
    if key == Manipulator.Key.Key_X:
        camera.screen.DOF = not camera.screen.DOF

camera.screen.key_pressed.connect(toggle_DOF)
camera.screen.show()