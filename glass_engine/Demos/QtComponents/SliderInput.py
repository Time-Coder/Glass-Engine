from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QDoubleSpinBox, QSlider, QCheckBox
from PyQt6.QtCore import pyqtSignal, Qt

class SliderInput(QWidget):

    checked_changed = pyqtSignal(bool)
    value_changed = pyqtSignal(float)

    def __init__(self, range:tuple, value:float=None, prompt:str=None, checkable:bool=False, unit:str=None, parent:QWidget=None):
        QWidget.__init__(self, parent=parent)
        self.should_call_slot = True

        hlayout = QHBoxLayout()
        hlayout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        if prompt:
            if not checkable:
                self.label = QLabel(prompt, parent=self)
            else:
                self.label = QCheckBox(prompt, parent=self)
                self.label.stateChanged.connect(self.slot_state_changed)
            hlayout.addWidget(self.label)

        self.spinbox = QDoubleSpinBox(parent=self)
        if unit:
            self.spinbox.setSuffix(unit)
        self.spinbox.setRange(range[0], range[1])
        hlayout.addWidget(self.spinbox)

        self.slider = QSlider(Qt.Orientation.Horizontal, parent=self)
        self.slider.setRange(0, 1000)
        hlayout.addWidget(self.slider)

        hlayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(hlayout)

        if value is not None:
            self.spinbox.setValue(value)
            default_tick = self.value_to_tick(value)
            self.slider.setValue(default_tick)

        self.spinbox.valueChanged.connect(self.spinbox_value_changed)
        self.slider.valueChanged.connect(self.slider_tick_changed)
        if checkable:
            self.slot_state_changed(0)

    def value_to_tick(self, value:float):
        return int((value - self.spinbox.minimum()) / (self.spinbox.maximum() - self.spinbox.minimum()) * (self.slider.maximum() - self.slider.minimum())) + self.slider.minimum()

    def tick_to_value(self, tick:int):
        return (tick - self.slider.minimum()) / (self.slider.maximum() - self.slider.minimum()) * (self.spinbox.maximum() - self.spinbox.minimum()) + self.spinbox.minimum()

    def spinbox_value_changed(self, value:float):
        if not self.should_call_slot:
            return
        
        old_should_call_slot = self.should_call_slot
        self.should_call_slot = False

        tick = self.value_to_tick(value)
        self.slider.setValue(tick)

        self.should_call_slot = old_should_call_slot

        self.value_changed.emit(value)

    def slider_tick_changed(self):
        if not self.should_call_slot:
            return
        
        old_should_call_slot = self.should_call_slot
        self.should_call_slot = False

        tick = self.slider.value()
        value = self.tick_to_value(tick)
        self.spinbox.setValue(value)

        self.should_call_slot = old_should_call_slot

        self.value_changed.emit(value)

    def slot_state_changed(self, state):
        self.slider.setEnabled(state == Qt.CheckState.Checked.value)
        self.spinbox.setEnabled(state == Qt.CheckState.Checked.value)
        self.checked_changed.emit(state == Qt.CheckState.Checked.value)

    @property
    def value(self):
        return self.spinbox.value()
    
    @value.setter
    def value(self, value:float):
        self.spinbox.setValue(value)

    @property
    def checked(self):
        if isinstance(self.label, QCheckBox):
            return self.label.isChecked()
        else:
            return True
    
    @checked.setter
    def checked(self, checked:bool):
        if isinstance(self.label, QCheckBox):
            self.label.setChecked(checked)