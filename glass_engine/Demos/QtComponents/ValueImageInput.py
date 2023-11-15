from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QComboBox
from PyQt6.QtCore import pyqtSignal, Qt

from .SliderInput import SliderInput
from .ImageChooser import ImageChooser

from enum import Enum

class ValueImageInput(QWidget):

    class Type(Enum):
        Value = 0
        Image = 1

    type_changed = pyqtSignal(Type)
    value_changed = pyqtSignal(float)
    file_path_changed = pyqtSignal(str)

    def __init__(self, prompt:str="", parent:QWidget=None):
        QWidget.__init__(self, parent=parent)

        hlayout = QHBoxLayout()
        hlayout.setContentsMargins(0, 0, 0, 0)
        hlayout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        label = QLabel(prompt, self)
        hlayout.addWidget(label)

        self.__type_combobox = QComboBox()
        self.__type_combobox.addItem("值", ValueImageInput.Type.Value)
        self.__type_combobox.addItem("贴图", ValueImageInput.Type.Image)
        hlayout.addWidget(self.__type_combobox)

        self.__slider_input = SliderInput(prompt="", range=(0, 1), value=0.5, parent=self)
        hlayout.addWidget(self.__slider_input)
        
        self.__image_chooser = ImageChooser(width=35, height=35, parent=self)
        hlayout.addWidget(self.__image_chooser)
        self.__image_chooser.hide()

        self.setLayout(hlayout)

        self.__type_combobox.currentIndexChanged.connect(self.__slot_type_changed)
        self.__slider_input.value_changed.connect(self.value_changed)
        self.__image_chooser.file_path_changed.connect(self.file_path_changed)

    def __slot_type_changed(self, index:int):
        if index == 0:
            self.__image_chooser.hide()
            self.__slider_input.show()
        else:
            self.__slider_input.hide()
            self.__image_chooser.show()
        self.type_changed.emit(self.__type_combobox.itemData(self.__type_combobox.currentIndex()))

    @property
    def type(self):
        return self.__type_combobox.itemData(self.__type_combobox.currentIndex())
    
    @type.setter
    def type(self, type:Type):
        if type == ValueImageInput.Type.Value:
            self.__type_combobox.setCurrentIndex(0)
        else:
            self.__type_combobox.setCurrentIndex(1)

    @property
    def value(self):
        return self.__slider_input.value
    
    @value.setter
    def value(self, value:float):
        self.__slider_input.value = value

    @property
    def file_path(self):
        return self.__image_chooser.file_path

    @file_path.setter
    def file_path(self, file_path:str):
        self.__image_chooser.file_path = file_path