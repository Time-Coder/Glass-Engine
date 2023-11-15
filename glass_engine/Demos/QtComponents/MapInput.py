from PyQt6.QtWidgets import QWidget, QHBoxLayout, QCheckBox
from PyQt6.QtCore import pyqtSignal, Qt
from .ImageChooser import ImageChooser

class MapInput(QWidget):

    checked_changed = pyqtSignal(bool)
    file_path_changed = pyqtSignal(str)

    def __init__(self, prompt:str="贴图", file_path:str="", width:int=50, height:int=50, parent:QWidget=None):
        QWidget.__init__(self, parent=parent)
        hlayout = QHBoxLayout()
        hlayout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.__prompt_checkbox = QCheckBox(prompt, self)
        self.__image_chooser = ImageChooser(file_path, width, height, self)
        self.__image_chooser.setEnabled(False)
        hlayout.addWidget(self.__prompt_checkbox)
        hlayout.addWidget(self.__image_chooser)
        hlayout.setContentsMargins(0, 0, 0, 0)
        hlayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.setLayout(hlayout)

        self.__prompt_checkbox.stateChanged.connect(self.__checkbox_state_changed)
        self.__image_chooser.file_path_changed.connect(self.file_path_changed)

    def __checkbox_state_changed(self, state:Qt.CheckState):
        self.__image_chooser.setEnabled(state == Qt.CheckState.Checked.value)
        self.__image_chooser.update()
        self.checked_changed.emit(state == Qt.CheckState.Checked.value)

    @property
    def checked(self):
        return self.__prompt_checkbox.isChecked()
    
    @checked.setter
    def checked(self, checked:bool):
        self.__prompt_checkbox.setChecked(checked)

    @property
    def file_path(self):
        return self.__image_chooser.file_path
    
    @file_path.setter
    def file_path(self, file_path:str):
        self.__image_chooser.file_path = file_path