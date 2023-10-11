from glass.download import pip_install
from .QtScreen import init_QtScreen
from ..Manipulators.Manipulator import Manipulator

try:
    import PySide2
    from PySide2.QtOpenGLWidgets import QOpenGLWidget
except ModuleNotFoundError:
    pip_install("PySide2")
    import PySide2
    from PySide2.QtOpenGLWidgets import QOpenGLWidget

import glm

@init_QtScreen
class PySide2Screen(QOpenGLWidget):
    mouse_pressed = PySide2.QtCore.Signal(Manipulator.MouseButton, glm.vec2, glm.vec2)
    mouse_released = PySide2.QtCore.Signal(Manipulator.MouseButton, glm.vec2, glm.vec2)
    mouse_double_clicked = PySide2.QtCore.Signal(Manipulator.MouseButton, glm.vec2, glm.vec2)
    mouse_moved = PySide2.QtCore.Signal(glm.vec2, glm.vec2)
    wheel_scrolled = PySide2.QtCore.Signal(glm.vec2, glm.vec2, glm.vec2)
    key_pressed = PySide2.QtCore.Signal(Manipulator.Key)
    key_released = PySide2.QtCore.Signal(Manipulator.Key)
    key_repeated = PySide2.QtCore.Signal(set)
    frame_started = PySide2.QtCore.Signal()
    frame_ended = PySide2.QtCore.Signal()
