import sys
import os

from glass.download import pip_install, is_China_user

try:
    import PyQt6
except:
    pip_install("PyQt6")

from PyQt6.QtWidgets import QApplication, QDialog, QHBoxLayout, QVBoxLayout, QWidget, QLabel, QDoubleSpinBox, QSlider
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon
from qt_material import apply_stylesheet

from ..Camera import Camera
from ..Model import Model
from ..BasicScene import ModelView
from ..Geometries.CoordSys import CoordSys
from glass.download import download