from glass.download import pip_install
from .QtScreen import init_QtScreen
from ..Manipulators.Manipulator import Manipulator

try:
    import PyQt6
    from PyQt6.QtOpenGLWidgets import QOpenGLWidget
except ModuleNotFoundError:
    pip_install("PyQt6")
    import PyQt6
    from PyQt6.QtOpenGLWidgets import QOpenGLWidget

import glm

@init_QtScreen
class PyQt6Screen(QOpenGLWidget):
    mouse_pressed = PyQt6.QtCore.pyqtSignal(Manipulator.MouseButton, glm.vec2, glm.vec2)
    mouse_released = PyQt6.QtCore.pyqtSignal(Manipulator.MouseButton, glm.vec2, glm.vec2)
    mouse_double_clicked = PyQt6.QtCore.pyqtSignal(Manipulator.MouseButton, glm.vec2, glm.vec2)
    mouse_moved = PyQt6.QtCore.pyqtSignal(glm.vec2, glm.vec2)
    wheel_scrolled = PyQt6.QtCore.pyqtSignal(glm.vec2, glm.vec2, glm.vec2)
    key_pressed = PyQt6.QtCore.pyqtSignal(Manipulator.Key)
    key_released = PyQt6.QtCore.pyqtSignal(Manipulator.Key)
    key_repeated = PyQt6.QtCore.pyqtSignal(set)
    frame_started = PyQt6.QtCore.pyqtSignal()
    frame_ended = PyQt6.QtCore.pyqtSignal()
