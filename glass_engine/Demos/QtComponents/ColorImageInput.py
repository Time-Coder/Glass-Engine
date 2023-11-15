from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QComboBox, QColorDialog, QFileDialog
from PyQt6.QtGui import QColor, QMouseEvent, QPaintEvent, QPainter, QPixmap
from PyQt6.QtCore import pyqtSignal, Qt, QRect

from enum import Enum
import glm
import os

class ColorImageChooser(QWidget):

    class Type(Enum):
        Color = 0
        Image = 1

    type_changed = pyqtSignal(Type)
    color_changed = pyqtSignal(QColor)
    glm_color_changed = pyqtSignal(object)
    file_path_changed = pyqtSignal(str)

    def __init__(self, type:Type=Type.Color, width:int=35, height:int=35, alpha:bool=False, parent:QWidget=None):
        QWidget.__init__(self, parent=parent)
        self.__type:ColorImageChooser.Type = type
        self.__alpha = alpha
        self.__color:QColor = QColor(0,0,0)
        self.__file_path:str = ""
        self.setFixedSize(width, height)
    
    @property
    def type(self):
        return self.__type
    
    @type.setter
    def type(self, type:Type):
        if self.__type == type:
            return
        
        self.__type = type
        self.update()
        self.type_changed.emit(self.__type)

    @property
    def color(self):
        return self.__color
    
    @color.setter
    def color(self, color:QColor):
        if self.__color == color:
            return
        
        self.__color = color
        if self.__type == ColorImageChooser.Type.Color:
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

    @property
    def file_path(self):
        return self.__file_path
    
    @file_path.setter
    def file_path(self, file_path:str):
        if self.__file_path == file_path:
            return
        
        self.__file_path = file_path
        if self.__type == ColorImageChooser.Type.Image:
            self.update()
        self.file_path_changed.emit(self.__file_path)

    def mouseReleaseEvent(self, mouse_event: QMouseEvent | None) -> None:
        if self.__type == ColorImageChooser.Type.Color:
            color = None
            if self.__alpha:
                color = QColorDialog.getColor(self.__color, self, "选择颜色", QColorDialog.ColorDialogOption.ShowAlphaChannel)
            else:
                color = QColorDialog.getColor(self.__color, self, "选择颜色")

            if color.isValid():
                self.color = color
        else:
            directory = None
            if os.path.isfile(self.__file_path):
                directory = os.path.dirname(self.__file_path)

            file_path = QFileDialog.getOpenFileName(self, "选择图片", directory, "Image File(*.jpg *.png *.bmp *.ico *.exr *.hdr *.glsl)")
            if file_path[0]:
                self.file_path = file_path[0]

        return super().mouseReleaseEvent(mouse_event)
    
    def paintEvent(self, paint_event: QPaintEvent | None) -> None:
        painter = QPainter(self)
        painter.setPen(Qt.PenStyle.NoPen)
        if self.__type == ColorImageChooser.Type.Color:
            painter.setBrush(self.__color)
        else:
            painter.setBrush(QColor(0,0,0))

        rect = self.rect()
        painter.drawRect(rect)
        if self.__type == ColorImageChooser.Type.Image and \
           os.path.isfile(self.__file_path):
            pixmap = QPixmap(self.__file_path)
            pixmap_ratio = pixmap.width() / pixmap.height()
            rect_ratio = rect.width() / rect.height()
            if pixmap_ratio > rect_ratio:
                pixmap_width = rect.width()
                pixmap_height = int(rect.width() / pixmap_ratio)
                contain_rect = QRect(0, int(rect.height()/2-pixmap_height/2), pixmap_width, pixmap_height)
                painter.drawPixmap(contain_rect, pixmap)
            else:
                pixmap_height = rect.height()
                pixmap_width = int(rect.height() * pixmap_ratio)
                contain_rect = QRect(int(rect.width()/2-pixmap_width/2), 0, pixmap_width, pixmap_height)
                painter.drawPixmap(contain_rect, pixmap)

        return super().paintEvent(paint_event)

class ColorImageInput(QWidget):

    type_changed = pyqtSignal(ColorImageChooser.Type)
    color_changed = pyqtSignal(QColor)
    glm_color_changed = pyqtSignal(glm.vec3)
    file_path_changed = pyqtSignal(str)

    def __init__(self, prompt:str, width:int=35, height:int=35, alpha:bool=False, parent:QWidget=None):
        QWidget.__init__(self, parent)

        hlayout = QHBoxLayout()
        hlayout.setContentsMargins(0, 0, 0, 0)
        hlayout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        label = QLabel(prompt, self)
        hlayout.addWidget(label)

        self.__type_combobox = QComboBox(self)
        self.__type_combobox.addItem("颜色", ColorImageChooser.Type.Color)
        self.__type_combobox.addItem("贴图", ColorImageChooser.Type.Image)
        hlayout.addWidget(self.__type_combobox)

        self.__color_image_chooser = ColorImageChooser(width=width, height=height, alpha=alpha, parent=self)
        hlayout.addWidget(self.__color_image_chooser)
        self.setLayout(hlayout)

        self.__color_image_chooser.type_changed.connect(self.type_changed)
        self.__color_image_chooser.color_changed.connect(self.color_changed)
        self.__color_image_chooser.glm_color_changed.connect(self.glm_color_changed)
        self.__color_image_chooser.file_path_changed.connect(self.file_path_changed)
        self.__type_combobox.currentIndexChanged.connect(self.__slot_type_changed)
        

    def __slot_type_changed(self, index:int):
        self.__color_image_chooser.type = self.__type_combobox.itemData(index)

    @property
    def type(self):
        return  self.__color_image_chooser.type
    
    @type.setter
    def type(self, type:ColorImageChooser.Type):
        if type == ColorImageChooser.Type.Color:
            self.__type_combobox.setCurrentIndex(0)
        else:
            self.__type_combobox.setCurrentIndex(1)

    @property
    def color(self):
        return self.__color_image_chooser.color
    
    @color.setter
    def color(self, color:QColor):
        self.__color_image_chooser.color = color

    @property
    def glm_color(self):
        return self.__color_image_chooser.glm_color
    
    @glm_color.setter
    def glm_color(self, glm_color:glm.vec3):
        self.__color_image_chooser.glm_color = glm_color

    @property
    def file_path(self):
        return self.__color_image_chooser.file_path
    
    @file_path.setter
    def file_path(self, file_path:str):
        self.__color_image_chooser.file_path = file_path