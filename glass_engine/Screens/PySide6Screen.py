from glass.download import pip_install
from .QtScreen import init_QtScreen
from ..Manipulators.Manipulator import Manipulator

try:
    import PySide6
except ModuleNotFoundError:
    pip_install("PySide6")
    import PySide6

from PySide6.QtOpenGLWidgets import QOpenGLWidget

import cgmath as cgm


@init_QtScreen
class PySide6Screen(QOpenGLWidget):
    mouse_pressed = PySide6.QtCore.Signal(Manipulator.MouseButton, cgm.vec2, cgm.vec2)
    mouse_released = PySide6.QtCore.Signal(Manipulator.MouseButton, cgm.vec2, cgm.vec2)
    mouse_double_clicked = PySide6.QtCore.Signal(
        Manipulator.MouseButton, cgm.vec2, cgm.vec2
    )
    mouse_moved = PySide6.QtCore.Signal(cgm.vec2, cgm.vec2)
    wheel_scrolled = PySide6.QtCore.Signal(cgm.vec2, cgm.vec2, cgm.vec2)
    key_pressed = PySide6.QtCore.Signal(Manipulator.Key)
    key_released = PySide6.QtCore.Signal(Manipulator.Key)
    key_repeated = PySide6.QtCore.Signal(set)
    frame_started = PySide6.QtCore.Signal()
    frame_ended = PySide6.QtCore.Signal()
