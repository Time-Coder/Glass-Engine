from PyQt6.QtWidgets import QWidget, QColorDialog, QHBoxLayout, QLabel
from PyQt6.QtGui import QColor, QMouseEvent, QPaintEvent, QPainter
from PyQt6.QtCore import pyqtSignal, Qt

import glm

class ColorChooser(QWidget):

    color_changed = pyqtSignal(QColor)
    glm_color_changed = pyqtSignal(object)

    def __init__(self, color:QColor=QColor(0,0,0), width:int=50, height:int=50, alpha:bool=False, parent:QWidget=None):
        QWidget.__init__(self, parent)
        self.__color = color
        self.__alpha = alpha
        self.setFixedSize(width, height)
    
    def mouseReleaseEvent(self, release_event: QMouseEvent | None) -> None:
        color = None
        if self.__alpha:
            color = QColorDialog.getColor(self.__color, self, "选择颜色", QColorDialog.ColorDialogOption.ShowAlphaChannel)
        else:
            color = QColorDialog.getColor(self.__color, self, "选择颜色")

        if color.isValid():
            self.color = color

        return super().mouseReleaseEvent(release_event)

    @property
    def color(self):
        return self.__color
    
    @color.setter
    def color(self, color:QColor):
        if self.__color != color:
            self.__color = color
            self.update()
            self.color_changed.emit(self.__color)
            self.glm_color_changed.emit(self.glm_color)
        
    @property
    def glm_color(self):
        if self.__alpha:
            return glm.vec4(self.__color.redF(), self.__color.greenF(), self.__color.blueF(), self.__color.alphaF())
        else:
            return glm.vec3(self.__color.redF(), self.__color.greenF(), self.__color.blueF())
        
    @glm_color.setter
    def glm_color(self, glm_color):
        if isinstance(glm_color, glm.vec3):
            self.color = QColor(int(glm_color.r*255), int(glm_color.g*255), int(glm_color.b*255))
        else:
            self.color = QColor(int(glm_color.r*255), int(glm_color.g*255), int(glm_color.b*255), int(glm_color.a*255))

    def paintEvent(self, paint_event: QPaintEvent | None) -> None:
        painter = QPainter(self)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(self.__color)
        painter.drawRect(self.rect())
        return super().paintEvent(paint_event)

class ColorInput(QWidget):

    color_changed = pyqtSignal(QColor)
    glm_color_changed = pyqtSignal(object)

    def __init__(self, prompt:str, color:QColor=QColor(0,0,0), width:int=50, height:int=50, alpha:bool=False, parent:QWidget=None):
        QWidget.__init__(self, parent=parent)

        hlayout = QHBoxLayout()
        hlayout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        label = QLabel(prompt, self)
        hlayout.addWidget(label)

        self.__color_chooser = ColorChooser(color, width, height, alpha, parent)
        hlayout.addWidget(self.__color_chooser)
        self.setLayout(hlayout)

        self.__color_chooser.color_changed.connect(self.color_changed)
        self.__color_chooser.glm_color_changed.connect(self.glm_color_changed)

    @property
    def color(self)->QColor:
        return self.__color_chooser.color
    
    @color.setter
    def color(self, color:QColor)->None:
        self.__color_chooser.color = color

    @property
    def glm_color(self)->glm.vec3:
        return self.__color_chooser.glm_color
    
    @glm_color.setter
    def glm_color(self, glm_color:glm.vec3)->None:
        self.__color_chooser.glm_color = glm_color