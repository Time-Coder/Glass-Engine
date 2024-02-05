from glass.download import pip_install
from .QtScreen import init_QtScreen
from ..Manipulators.Manipulator import Manipulator

try:
    import PyQt5
except ModuleNotFoundError:
    pip_install("PyQt5")
    import PyQt5

from PyQt5.QtWidgets import QOpenGLWidget

import glm


@init_QtScreen
class PyQt5Screen(QOpenGLWidget):
    mouse_pressed = PyQt5.QtCore.pyqtSignal(Manipulator.MouseButton, glm.vec2, glm.vec2)
    mouse_released = PyQt5.QtCore.pyqtSignal(
        Manipulator.MouseButton, glm.vec2, glm.vec2
    )
    mouse_double_clicked = PyQt5.QtCore.pyqtSignal(
        Manipulator.MouseButton, glm.vec2, glm.vec2
    )
    mouse_moved = PyQt5.QtCore.pyqtSignal(glm.vec2, glm.vec2)
    wheel_scrolled = PyQt5.QtCore.pyqtSignal(glm.vec2, glm.vec2, glm.vec2)
    key_pressed = PyQt5.QtCore.pyqtSignal(Manipulator.Key)
    key_released = PyQt5.QtCore.pyqtSignal(Manipulator.Key)
    key_repeated = PyQt5.QtCore.pyqtSignal(set)
    frame_started = PyQt5.QtCore.pyqtSignal()
    frame_ended = PyQt5.QtCore.pyqtSignal()
