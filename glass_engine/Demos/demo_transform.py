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

class ParamControlLine(QWidget):

    value_changed = pyqtSignal(float)

    def __init__(self, prompt:str, range:tuple, default_value:float, unit:str=None, parent:QWidget=None):
        QWidget.__init__(self, parent=parent)
        self.should_call_slot = True

        hlayout = QHBoxLayout()

        self.label = QLabel(prompt, parent=self)
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

        self.spinbox.setValue(default_value)
        default_tick = self.value_to_tick(default_value)
        self.slider.setValue(default_tick)

        self.spinbox.valueChanged.connect(self.spinbox_value_changed)
        self.slider.valueChanged.connect(self.slider_tick_changed)

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

class TransformControlPanel(QWidget):

    def __init__(self, parent:QWidget=None):
        QWidget.__init__(self, parent=parent)
        hlayout = QHBoxLayout()

        vlayout = QVBoxLayout()
        self.position_x_line = ParamControlLine("position.x", (-5, 5), 0, "m", self)
        vlayout.addWidget(self.position_x_line)

        self.position_y_line = ParamControlLine("position.y", (-5, 5), 0, "m", self)
        vlayout.addWidget(self.position_y_line)

        self.position_z_line = ParamControlLine("position.z", (-5, 5), 0, "m", self)
        vlayout.addWidget(self.position_z_line)
        vlayout.addStretch()

        hlayout.addLayout(vlayout)

        vlayout = QVBoxLayout()
        self.yaw_line = ParamControlLine("偏航角 (yaw)", (-180, 180), 0, "°", self)
        vlayout.addWidget(self.yaw_line)

        self.pitch_line = ParamControlLine("俯仰角 (pitch)", (-90, 90), 0, "°", self)
        vlayout.addWidget(self.pitch_line)

        self.roll_line = ParamControlLine("翻滚角 (roll)", (-180, 180), 0, "°", self)
        vlayout.addWidget(self.roll_line)
        vlayout.addStretch()

        hlayout.addLayout(vlayout)

        vlayout = QVBoxLayout()
        self.scale_x_line = ParamControlLine("scale.x", (-2, 2), 1, "", self)
        vlayout.addWidget(self.scale_x_line)

        self.scale_y_line = ParamControlLine("scale.y", (-2, 2), 1, "", self)
        vlayout.addWidget(self.scale_y_line)

        self.scale_z_line = ParamControlLine("scale.z", (-2, 2), 1, "", self)
        vlayout.addWidget(self.scale_z_line)
        vlayout.addStretch()

        hlayout.addLayout(vlayout)

        self.setLayout(hlayout)

class MainWindow(QDialog):

    def __init__(self, parent:QWidget=None):
        QDialog.__init__(self, parent=parent)
        self.setWindowFlags(Qt.WindowType.WindowMinMaxButtonsHint | Qt.WindowType.WindowCloseButtonHint)
        self.setWindowTitle('glass_engine 空间变换概念演示')

        self_folder = os.path.dirname(os.path.abspath(__file__))
        self.setWindowIcon(QIcon(self_folder + "/../images/glass_engine_logo64.png"))

        vlayout = QVBoxLayout()

        self.scene, self.camera, dir_light = ModelView()
        self.camera.screen.manipulator.elevation = 30
        self.camera.screen.manipulator.distance = 5
        self.camera.projection_mode = Camera.ProjectionMode.Orthographic

        dir_light.generate_shadows = False

        self_path = os.path.dirname(os.path.abspath(__file__))
        self.model = Model(self_path + "/assets/models/jet/11805_airplane_v2_L2.obj")
        self.model["root"].scale = 1/500
        self.model["root"].position.z -= 0.3
        model_coord_sys = CoordSys(1.6)
        self.model.add_child(model_coord_sys)

        coord_sys = CoordSys(1.6, alpha=0.3)

        self.scene.add(self.model)
        self.scene.add(coord_sys)

        self.scene.skydome = "https://dl.polyhaven.org/file/ph-assets/HDRIs/extra/Tonemapped%20JPG/industrial_sunset_puresky.jpg"
        
        vlayout.addWidget(self.camera.screen)

        self.control_panel = TransformControlPanel(self)
        vlayout.addWidget(self.control_panel)

        self.setLayout(vlayout)
        self.resize(1000, 600)

        self.control_panel.position_x_line.value_changed.connect(self.position_x_changed)
        self.control_panel.position_y_line.value_changed.connect(self.position_y_changed)
        self.control_panel.position_z_line.value_changed.connect(self.position_z_changed)
        self.control_panel.yaw_line.value_changed.connect(self.yaw_changed)
        self.control_panel.pitch_line.value_changed.connect(self.pitch_changed)
        self.control_panel.roll_line.value_changed.connect(self.roll_changed)
        self.control_panel.scale_x_line.value_changed.connect(self.scale_x_changed)
        self.control_panel.scale_y_line.value_changed.connect(self.scale_y_changed)
        self.control_panel.scale_z_line.value_changed.connect(self.scale_z_changed)
        self.camera.screen.setFocus()
        
    def position_x_changed(self, value):
        self.model.position.x = value
        self.camera.screen.update()

    def position_y_changed(self, value):
        self.model.position.y = value
        self.camera.screen.update()

    def position_z_changed(self, value):
        self.model.position.z = value
        self.camera.screen.update()

    def yaw_changed(self, value):
        self.model.yaw = value
        self.camera.screen.update()

    def pitch_changed(self, value):
        self.model.pitch = value
        self.camera.screen.update()

    def roll_changed(self, value):
        self.model.roll = value
        self.camera.screen.update()

    def scale_x_changed(self, value):
        self.model.scale.x = value
        self.camera.screen.update()

    def scale_y_changed(self, value):
        self.model.scale.y = value
        self.camera.screen.update()

    def scale_z_changed(self, value):
        self.model.scale.z = value
        self.camera.screen.update()

def download_files():
    self_folder = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")
    model_folder = self_folder + "/assets/models/jet"

    md5_map = \
    {
        "11805_airplane_v2_L2.mtl": "36059ea10e4a35955dc2ee6b1203f9c8",
        "11805_airplane_v2_L2.obj": "85bd6ac8fcc6c717ba5a96a7a065c0ec",
        "airplane_body_diffuse_v1.jpg": "e7b1c3492a69e81959ffc14af0ad8ed7",
        "airplane_wings_diffuse_v1.jpg": "c4ef09fd0825d5d97a1ba105775e253a",
    }

    target_file = model_folder + "/11805_airplane_v2_L2.mtl"
    gitee_url = "https://gitee.com/time-coder/Glass-Engine/raw/main/glass_engine/Demos/assets/models/jet/11805_airplane_v2_L2.mtl"
    github_url = "https://raw.githubusercontent.com/Time-Coder/Glass-Engine/main/glass_engine/Demos/assets/models/jet/11805_airplane_v2_L2.mtl"

    if is_China_user():
        download(gitee_url, target_file, md5_map["11805_airplane_v2_L2.mtl"])
    else:
        download(github_url, target_file, md5_map["11805_airplane_v2_L2.mtl"])

    target_file = model_folder + "/11805_airplane_v2_L2.obj"
    gitee_url = "https://gitee.com/time-coder/Glass-Engine/raw/main/glass_engine/Demos/assets/models/jet/11805_airplane_v2_L2.obj"
    github_url = "https://raw.githubusercontent.com/Time-Coder/Glass-Engine/main/glass_engine/Demos/assets/models/jet/11805_airplane_v2_L2.obj"

    if is_China_user():
        download(gitee_url, target_file, md5_map["11805_airplane_v2_L2.obj"])
    else:
        download(github_url, target_file, md5_map["11805_airplane_v2_L2.obj"])

    target_file = model_folder + "/airplane_body_diffuse_v1.jpg"
    gitee_url = "https://gitee.com/time-coder/Glass-Engine/raw/main/glass_engine/Demos/assets/models/jet/airplane_body_diffuse_v1.jpg"
    github_url = "https://raw.githubusercontent.com/Time-Coder/Glass-Engine/main/glass_engine/Demos/assets/models/jet/airplane_body_diffuse_v1.jpg"

    if is_China_user():
        download(gitee_url, target_file, md5_map["airplane_body_diffuse_v1.jpg"])
    else:
        download(github_url, target_file, md5_map["airplane_body_diffuse_v1.jpg"])

    target_file = model_folder + "/airplane_wings_diffuse_v1.jpg"
    gitee_url = "https://gitee.com/time-coder/Glass-Engine/raw/main/glass_engine/Demos/assets/models/jet/airplane_wings_diffuse_v1.jpg"
    github_url = "https://raw.githubusercontent.com/Time-Coder/Glass-Engine/main/glass_engine/Demos/assets/models/jet/airplane_wings_diffuse_v1.jpg"

    if is_China_user():
        download(gitee_url, target_file, md5_map["airplane_wings_diffuse_v1.jpg"])
    else:
        download(github_url, target_file, md5_map["airplane_wings_diffuse_v1.jpg"])

def demo_transform():
    download_files()
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme='dark_amber.xml')

    main_window = MainWindow()
    main_window.show()

    app.exec()