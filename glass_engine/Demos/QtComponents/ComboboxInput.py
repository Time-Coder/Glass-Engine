from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QComboBox
from PyQt6.QtCore import pyqtSignal, Qt

class ComboboxInput(QWidget):

    value_changed = pyqtSignal(object)

    def __init__(self, prompt:str, values:dict, value=None, parent:QWidget=None):
        QWidget.__init__(self, parent=parent)

        hlayout = QHBoxLayout()
        hlayout.setContentsMargins(0,0,0,0)
        hlayout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        label = QLabel(prompt, self)
        hlayout.addWidget(label)

        self.__combobox = QComboBox(self)
        active_index = -1
        index = 0
        for key, _value in values.items():
            self.__combobox.addItem(key, _value)
            if value is not None and _value == value:
                active_index = index

            index += 1

        if active_index != -1:
            self.__combobox.setCurrentIndex(active_index)

        hlayout.addWidget(self.__combobox)
        self.setLayout(hlayout)

        self.__combobox.currentIndexChanged.connect(self.__index_changed)

    @property
    def value(self):
        return self.__combobox.currentData()
    
    @value.setter
    def value(self, value):
        for i in range(self.__combobox.count()):
            if value == self.__combobox.itemData(i):
                self.__combobox.setCurrentIndex(i)
                return

    def __index_changed(self, index:int):
        self.value_changed.emit(self.__combobox.itemData(index))