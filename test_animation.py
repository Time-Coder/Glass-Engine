from glass_engine import *
from glass_engine.Geometries import *
from glass_engine.Animations import Animation, EasingCurve, SequentialAnimation, ParallelAnimation

import math

scene, camera, light, floor = SceneRoam()
camera.pitch = 0

sphere = Sphere()
sphere.position.z = 0.5

scene.add(sphere)

def scale_callback(t):
    if sphere.position.z < sphere.radius:
        sphere.scale.z = sphere.position.z / sphere.radius

animation = ParallelAnimation(
    Animation(
        target=sphere.position,
        attr="z",
        end_value=5,
        duration=math.sqrt(2*5/9.8),
        easing_curve=EasingCurve.OutQuad,
        go_back=True,
        # running_callback=scale_callback
    ),

    Animation(
        target=sphere.position,
        attr="x",
        end_value=5,
        duration=2*math.sqrt(2*5/9.8),
        easing_curve=EasingCurve.Linear,
        # go_back=True,
        # running_callback=scale_callback
    ),

    loops=200,
    go_back=True,
    running_callback=scale_callback
)

animation.start()

camera.screen.show()