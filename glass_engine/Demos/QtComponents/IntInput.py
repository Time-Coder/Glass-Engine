from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QSpinBox
from PyQt6.QtCore import Qt, pyqtSignal

class IntInput(QWidget):

    value_changed = pyqtSignal(int)

    def __init__(self, prompt:str, range, value:int=None, parent:QWidget=None):
        QWidget.__init__(self, parent)

        hlayout = QHBoxLayout()
        hlayout.setContentsMargins(0, 0, 0, 0)
        hlayout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        label = QLabel(prompt, self)
        hlayout.addWidget(label)

        self.__spinbox = QSpinBox()
        self.__spinbox.setMinimum(range[0])
        self.__spinbox.setMaximum(range[1])
        if value is not None:
            self.__spinbox.setValue(value)
        hlayout.addWidget(self.__spinbox)

        self.__spinbox.valueChanged.connect(self.value_changed)

    @property
    def value(self):
        return self.__spinbox.value()
    
    @value.setter
    def value(self, value:float):
        self.__spinbox.setValue(value)

