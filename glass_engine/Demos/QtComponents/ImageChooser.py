from PyQt6.QtWidgets import QWidget, QFileDialog
from PyQt6.QtGui import QColor, QMouseEvent, QPaintEvent, QPainter, QPixmap, QPen
from PyQt6.QtCore import pyqtSignal, QRect, Qt

import os

class ImageChooser(QWidget):

    file_path_changed = pyqtSignal(str)

    def __init__(self, file_path:str="", width:int=50, height:int=50, parent:QWidget=None):
        QWidget.__init__(self, parent)
        self.__file_path = file_path
        self.setFixedSize(width, height)

    @property
    def file_path(self):
        return self.__file_path
    
    @file_path.setter
    def file_path(self, file_path:str):
        if not os.path.isfile(file_path):
            return
        
        if os.path.abspath(self.__file_path).replace("\\", "/") != os.path.abspath(file_path).replace("\\", "/"):
            self.__file_path = file_path
            self.update()
            self.file_path_changed.emit(self.__file_path)

    def mouseReleaseEvent(self, mouse_event: QMouseEvent | None) -> None:
        directory = None
        if os.path.isfile(self.__file_path):
            directory = os.path.dirname(self.__file_path)

        file_path = QFileDialog.getOpenFileName(self, "选择图片", directory, "Image File(*.jpg *.png *.bmp *.ico *.exr *.hdr *.glsl)")
        if file_path[0]:
            self.file_path = file_path[0]

        return super().mouseReleaseEvent(mouse_event)
    
    def paintEvent(self, paint_event: QPaintEvent | None) -> None:
        painter = QPainter(self)
        painter.setPen(QPen(Qt.PenStyle.NoPen))
        painter.setBrush(QColor(0,0,0))
        rect = self.rect()
        painter.drawRect(rect)
        if self.isEnabled() and os.path.isfile(self.__file_path):
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