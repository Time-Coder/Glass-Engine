from glass_engine import *
from glass_engine.Geometries import *
from glass_engine.Lights import PointLight
from glass_engine.Animations import Animation, EasingCurve, SequentialAnimation, ParallelAnimation

import math

GlassConfig.recompile = True
GlassConfig.debug = True

scene, camera, light, floor = SceneRoam()
camera.pitch = 0

sphere = Sphere()
sphere.position.z = 0.5

scene.add(sphere)

def running_callback(t):
    if sphere.position.z < sphere.radius:
        sphere.scale.z = sphere.position.z / sphere.radius

def done_callback(t):
    sphere.scale.z = 1

animation = SequentialAnimation(
    Animation(
        target=sphere.position,
        property="z",
        to=5,
        duration=math.sqrt(2*5/9.8),
        easing_curve=EasingCurve.OutQuad,
        go_back=True,
        # running_callback=running_callback
    ),

    Animation(
        target=sphere.position,
        property="x",
        to=5,
        duration=2*math.sqrt(2*5/9.8),
        easing_curve=EasingCurve.Linear,
        # go_back=True,
        # running_callback=running_callback
    ),

    loops=1,
    go_back=True,
    running_callback=running_callback,
    done_callback=done_callback
)

animation.start()

# camera.aspect_ratio = 2.0
# camera.screen.manipulator.scroll_sensitivity = 5.0
camera.screen.show()