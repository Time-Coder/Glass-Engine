from glass.download import pip_install

try:
    import PyQt6
except:
    pip_install("PyQt6")

from PyQt6.QtWidgets import QSplitter, QDialog, QCheckBox, QWidget, QVBoxLayout, QApplication, QHBoxLayout, QScrollArea
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import pyqtSignal, Qt
from qt_material import apply_stylesheet

from .QtComponents import IntInput, ComboboxInput, MapInput, SliderInput, ColorImageInput, ValueImageInput, ColorImageChooser

from ..Model import Model
from ..BasicScene import ModelView
from ..Geometries.Floor import Floor
from ..Geometries.Sphere import Sphere
from ..Material import Material

import sys
import os
import functools
import glm

def slot(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        self = args[0]
        if not self.should_call_slot:
            return
        return func(*args, **kwargs)
    return wrapper

class MaterialEditor(QWidget):

    material_changed = pyqtSignal()
    internal_changed = pyqtSignal()

    def __init__(self, material:Material, parent:QWidget=None):
        QWidget.__init__(self, parent=parent)

        self.__material = None
        self.inputs = {}
        self.should_call_slot = True
        self.parameters_map = \
        {
            "ambient": {Material.ShadingModel.Flat, Material.ShadingModel.Gouraud, Material.ShadingModel.Phong, Material.ShadingModel.PhongBlinn, Material.ShadingModel.Toon, Material.ShadingModel.OrenNayar, Material.ShadingModel.Minnaert, Material.ShadingModel.CookTorrance, Material.ShadingModel.Fresnel, Material.ShadingModel.PBR},
            "diffuse": {Material.ShadingModel.Flat, Material.ShadingModel.Gouraud, Material.ShadingModel.Phong, Material.ShadingModel.PhongBlinn, Material.ShadingModel.Toon, Material.ShadingModel.OrenNayar, Material.ShadingModel.Minnaert, Material.ShadingModel.Fresnel, Material.ShadingModel.Unlit},
            "specular": {Material.ShadingModel.Gouraud, Material.ShadingModel.Phong, Material.ShadingModel.PhongBlinn, Material.ShadingModel.Toon},
            "shininess_strength": {Material.ShadingModel.Gouraud, Material.ShadingModel.Phong, Material.ShadingModel.PhongBlinn, Material.ShadingModel.Toon},
            "shininess": {Material.ShadingModel.Gouraud, Material.ShadingModel.Phong, Material.ShadingModel.PhongBlinn, Material.ShadingModel.Toon},
            "emission": {Material.ShadingModel.Flat, Material.ShadingModel.Gouraud, Material.ShadingModel.Phong, Material.ShadingModel.PhongBlinn, Material.ShadingModel.Toon, Material.ShadingModel.OrenNayar, Material.ShadingModel.Minnaert, Material.ShadingModel.CookTorrance, Material.ShadingModel.Fresnel, Material.ShadingModel.PBR, Material.ShadingModel.Unlit},
            "emission_strength": {Material.ShadingModel.Flat, Material.ShadingModel.Gouraud, Material.ShadingModel.Phong, Material.ShadingModel.PhongBlinn, Material.ShadingModel.Toon, Material.ShadingModel.OrenNayar, Material.ShadingModel.Minnaert, Material.ShadingModel.CookTorrance, Material.ShadingModel.Fresnel, Material.ShadingModel.PBR, Material.ShadingModel.Unlit},
            "rim_power": {Material.ShadingModel.Flat, Material.ShadingModel.Gouraud, Material.ShadingModel.Phong, Material.ShadingModel.PhongBlinn, Material.ShadingModel.Toon, Material.ShadingModel.OrenNayar, Material.ShadingModel.Minnaert, Material.ShadingModel.CookTorrance, Material.ShadingModel.Fresnel, Material.ShadingModel.PBR},
            "base_color": {Material.ShadingModel.CookTorrance, Material.ShadingModel.PBR},
            "metallic": {Material.ShadingModel.CookTorrance, Material.ShadingModel.PBR},
            "roughness": {Material.ShadingModel.CookTorrance, Material.ShadingModel.PBR, Material.ShadingModel.OrenNayar, Material.ShadingModel.Minnaert},
            "diffuse_bands": {Material.ShadingModel.Toon},
            "specular_bands": {Material.ShadingModel.Toon},
            "diffuse_softness": {Material.ShadingModel.Toon},
            "specular_softness": {Material.ShadingModel.Toon},
            "reflection": {Material.ShadingModel.Flat, Material.ShadingModel.Gouraud, Material.ShadingModel.Phong, Material.ShadingModel.PhongBlinn, Material.ShadingModel.Toon, Material.ShadingModel.OrenNayar, Material.ShadingModel.Minnaert, Material.ShadingModel.CookTorrance, Material.ShadingModel.Fresnel, Material.ShadingModel.PBR},
            "reflection_opacity": {Material.ShadingModel.Flat, Material.ShadingModel.Gouraud, Material.ShadingModel.Phong, Material.ShadingModel.PhongBlinn, Material.ShadingModel.Toon, Material.ShadingModel.OrenNayar, Material.ShadingModel.Minnaert, Material.ShadingModel.CookTorrance, Material.ShadingModel.Fresnel, Material.ShadingModel.PBR},
            "refractive_index": {Material.ShadingModel.Flat, Material.ShadingModel.Gouraud, Material.ShadingModel.Phong, Material.ShadingModel.PhongBlinn, Material.ShadingModel.Toon, Material.ShadingModel.OrenNayar, Material.ShadingModel.Minnaert, Material.ShadingModel.CookTorrance, Material.ShadingModel.Fresnel, Material.ShadingModel.PBR},
            "dynamic_env_mapping": {Material.ShadingModel.Flat, Material.ShadingModel.Gouraud, Material.ShadingModel.Phong, Material.ShadingModel.PhongBlinn, Material.ShadingModel.Toon, Material.ShadingModel.OrenNayar, Material.ShadingModel.Minnaert, Material.ShadingModel.CookTorrance, Material.ShadingModel.Fresnel, Material.ShadingModel.PBR},
            "env_mix_diffuse": {Material.ShadingModel.Flat, Material.ShadingModel.Gouraud, Material.ShadingModel.Phong, Material.ShadingModel.PhongBlinn, Material.ShadingModel.Toon, Material.ShadingModel.OrenNayar, Material.ShadingModel.Minnaert, Material.ShadingModel.CookTorrance, Material.ShadingModel.Fresnel, Material.ShadingModel.PBR},
            "opacity": {Material.ShadingModel.Flat, Material.ShadingModel.Gouraud, Material.ShadingModel.Phong, Material.ShadingModel.PhongBlinn, Material.ShadingModel.Toon, Material.ShadingModel.OrenNayar, Material.ShadingModel.Minnaert, Material.ShadingModel.CookTorrance, Material.ShadingModel.Fresnel, Material.ShadingModel.PBR},
            "height_scale": {Material.ShadingModel.Flat, Material.ShadingModel.Gouraud, Material.ShadingModel.Phong, Material.ShadingModel.PhongBlinn, Material.ShadingModel.Toon, Material.ShadingModel.OrenNayar, Material.ShadingModel.Minnaert, Material.ShadingModel.CookTorrance, Material.ShadingModel.Fresnel, Material.ShadingModel.PBR},
            "fog": {Material.ShadingModel.Flat, Material.ShadingModel.Gouraud, Material.ShadingModel.Phong, Material.ShadingModel.PhongBlinn, Material.ShadingModel.Toon, Material.ShadingModel.OrenNayar, Material.ShadingModel.Minnaert, Material.ShadingModel.CookTorrance, Material.ShadingModel.Fresnel, Material.ShadingModel.PBR},
            "recv_shadows": {Material.ShadingModel.Flat, Material.ShadingModel.Gouraud, Material.ShadingModel.Phong, Material.ShadingModel.PhongBlinn, Material.ShadingModel.Toon, Material.ShadingModel.OrenNayar, Material.ShadingModel.Minnaert, Material.ShadingModel.CookTorrance, Material.ShadingModel.Fresnel, Material.ShadingModel.PBR},
            "cast_shadows": {Material.ShadingModel.Flat, Material.ShadingModel.Gouraud, Material.ShadingModel.Phong, Material.ShadingModel.PhongBlinn, Material.ShadingModel.Toon, Material.ShadingModel.OrenNayar, Material.ShadingModel.Minnaert, Material.ShadingModel.CookTorrance, Material.ShadingModel.Fresnel, Material.ShadingModel.PBR},
            "ao_map": {Material.ShadingModel.Flat, Material.ShadingModel.Gouraud, Material.ShadingModel.Phong, Material.ShadingModel.PhongBlinn, Material.ShadingModel.Toon, Material.ShadingModel.OrenNayar, Material.ShadingModel.Minnaert, Material.ShadingModel.CookTorrance, Material.ShadingModel.Fresnel, Material.ShadingModel.PBR},
            "normal_map": {Material.ShadingModel.Flat, Material.ShadingModel.Gouraud, Material.ShadingModel.Phong, Material.ShadingModel.PhongBlinn, Material.ShadingModel.Toon, Material.ShadingModel.OrenNayar, Material.ShadingModel.Minnaert, Material.ShadingModel.CookTorrance, Material.ShadingModel.Fresnel, Material.ShadingModel.PBR},
            "height_map": {Material.ShadingModel.Flat, Material.ShadingModel.Gouraud, Material.ShadingModel.Phong, Material.ShadingModel.PhongBlinn, Material.ShadingModel.Toon, Material.ShadingModel.OrenNayar, Material.ShadingModel.Minnaert, Material.ShadingModel.CookTorrance, Material.ShadingModel.Fresnel, Material.ShadingModel.PBR},
            "arm_map": {Material.ShadingModel.Flat, Material.ShadingModel.Gouraud, Material.ShadingModel.Phong, Material.ShadingModel.PhongBlinn, Material.ShadingModel.Toon, Material.ShadingModel.OrenNayar, Material.ShadingModel.Minnaert, Material.ShadingModel.CookTorrance, Material.ShadingModel.Fresnel, Material.ShadingModel.PBR},
        }

        vlayout_container = QVBoxLayout()
        scroll_area = QScrollArea()

        main_widget = QWidget()
        vlayout = QVBoxLayout()
        shading_model_values = \
        {
            "Flat": Material.ShadingModel.Flat,
            "Gouraud": Material.ShadingModel.Gouraud,
            "Phong": Material.ShadingModel.Phong,
            "PhongBlinn": Material.ShadingModel.PhongBlinn,
            "Toon": Material.ShadingModel.Toon,
            "OrenNaya": Material.ShadingModel.OrenNayar,
            "Minnaert": Material.ShadingModel.Minnaert,
            "Unlit": Material.ShadingModel.Unlit,
            "Fresnel": Material.ShadingModel.Fresnel,
            "PBR": Material.ShadingModel.PBR
        }
        self.inputs["shading_model"] = ComboboxInput("着色模型", shading_model_values, parent=self)
        vlayout.addWidget(self.inputs["shading_model"])

        internal_materials_values = \
        {
            "自定义": None,
            "翡翠": Material.Type.Emerald,
            "玉":  Material.Type.Jade,
            "黑曜石": Material.Type.Obsidian,
            "珍珠": Material.Type.Pearl,
            "红宝石": Material.Type.Ruby,
            "绿松石": Material.Type.Turquoise,
            "黄铜": Material.Type.Brass,
            "青铜": Material.Type.Bronze,
            "铬": Material.Type.Chrome,
            "铜": Material.Type.Copper,
            "金": Material.Type.Gold,
            "银": Material.Type.Silver,
            "黑色塑料": Material.Type.BlackPlastic,
            "青色塑料": Material.Type.CyanPlastic,
            "绿色塑料": Material.Type.GreenPlastic,
            "红色塑料": Material.Type.RedPlastic,
            "白色塑料": Material.Type.WhitePlastic,
            "黄色塑料": Material.Type.YellowPlastic,
            "黑色橡胶": Material.Type.BlackRubber,
            "青色橡胶": Material.Type.CyanRubber,
            "绿色橡胶": Material.Type.GreenRubber,
            "红色橡胶": Material.Type.RedRubber,
            "白色橡胶": Material.Type.WhiteRubber,
            "黄色橡胶": Material.Type.YellowRubber
        }
        self.inputs["internal_material"] = ComboboxInput("内置材质", internal_materials_values, parent=self)
        vlayout.addWidget(self.inputs["internal_material"])

        self.inputs["ambient"] = ColorImageInput(prompt="环境光", parent=self)
        vlayout.addWidget(self.inputs["ambient"])

        self.inputs["diffuse"] = ColorImageInput(prompt="漫反射", parent=self)
        vlayout.addWidget(self.inputs["diffuse"])

        self.inputs["specular"] = ColorImageInput(prompt="镜面高光", parent=self)
        vlayout.addWidget(self.inputs["specular"])

        self.inputs["shininess_strength"] = SliderInput(prompt="高光强度", range=(1, 10), parent=self)
        vlayout.addWidget(self.inputs["shininess_strength"])

        self.inputs["shininess"] = SliderInput(prompt="闪耀度", range=(0, 256), parent=self)
        vlayout.addWidget(self.inputs["shininess"])

        self.inputs["emission"] = ColorImageInput(prompt="自发光", parent=self)
        vlayout.addWidget(self.inputs["emission"])

        self.inputs["emission_strength"] = SliderInput(prompt="自发光强度", range=(1, 50), parent=self)
        vlayout.addWidget(self.inputs["emission_strength"])

        self.inputs["rim_power"] = SliderInput(prompt="边缘光强度", range=(0, 1), parent=self)
        vlayout.addWidget(self.inputs["rim_power"])

        self.inputs["base_color"] = ColorImageInput(prompt="基础颜色", parent=self)
        vlayout.addWidget(self.inputs["base_color"])

        self.inputs["metallic"] = ValueImageInput(prompt="金属度", parent=self)
        vlayout.addWidget(self.inputs["metallic"])

        self.inputs["roughness"] = ValueImageInput(prompt="粗糙度", parent=self)
        vlayout.addWidget(self.inputs["roughness"])

        self.inputs["diffuse_bands"] = IntInput(prompt="漫反射条带数", range=(2, 5), parent=self)
        vlayout.addWidget(self.inputs["diffuse_bands"])

        self.inputs["specular_bands"] = IntInput(prompt="镜面高光条带数", range=(2, 5), parent=self)
        vlayout.addWidget(self.inputs["specular_bands"])

        self.inputs["diffuse_softness"] = SliderInput(prompt="漫反射过度软度", range=(0, 1), parent=self)
        vlayout.addWidget(self.inputs["diffuse_softness"])

        self.inputs["specular_softness"] = SliderInput(prompt="镜面高光过度软度", range=(0, 1), parent=self)
        vlayout.addWidget(self.inputs["specular_softness"])

        self.inputs["opacity"] = ValueImageInput(prompt="不透明度", parent=self)
        vlayout.addWidget(self.inputs["opacity"])

        self.inputs["height_scale"] = SliderInput(prompt="凹凸夸张系数", range=(0, 1), parent=self)
        vlayout.addWidget(self.inputs["height_scale"])

        self.inputs["reflection"] = ColorImageInput(prompt="环境映射层", parent=self)
        vlayout.addWidget(self.inputs["reflection"])

        self.inputs["reflection_opacity"] = SliderInput(prompt="环境映射层不透明度", range=(0,1), parent=self)
        vlayout.addWidget(self.inputs["reflection_opacity"])

        self.inputs["refractive_index"] = SliderInput(prompt="折射率", range=(1,2), checkable=True, parent=self)
        vlayout.addWidget(self.inputs["refractive_index"])

        self.inputs["dynamic_env_mapping"] = QCheckBox("动态环境映射", parent=self)
        vlayout.addWidget(self.inputs["dynamic_env_mapping"])

        self.inputs["env_mix_diffuse"] = QCheckBox("环境映射与漫反射混合", parent=self)
        vlayout.addWidget(self.inputs["env_mix_diffuse"])

        self.inputs["fog"] = QCheckBox("受雾影响", parent=self)
        vlayout.addWidget(self.inputs["fog"])

        self.inputs["recv_shadows"] = QCheckBox("接收阴影", parent=self)
        vlayout.addWidget(self.inputs["recv_shadows"])

        self.inputs["cast_shadows"] = QCheckBox("投射阴影", parent=self)
        vlayout.addWidget(self.inputs["cast_shadows"])

        self.inputs["ao_map"] = MapInput(prompt="ao 贴图", width=35, height=35, parent=self)
        vlayout.addWidget(self.inputs["ao_map"])

        self.inputs["normal_map"] = MapInput(prompt="法向量贴图", width=35, height=35, parent=self)
        vlayout.addWidget(self.inputs["normal_map"])

        self.inputs["height_map"] = MapInput(prompt="凹凸贴图", width=35, height=35, parent=self)
        vlayout.addWidget(self.inputs["height_map"])

        self.inputs["arm_map"] = MapInput(prompt="arm 贴图", width=35, height=35, parent=self)
        vlayout.addWidget(self.inputs["arm_map"])
        vlayout.addStretch()

        main_widget.setLayout(vlayout)
        scroll_area.setWidget(main_widget)

        vlayout_container.addWidget(scroll_area)
        self.setLayout(vlayout_container)

        self.material = material

        self.inputs["shading_model"].value_changed.connect(self.slot_shading_model_changed)
        self.inputs["internal_material"].value_changed.connect(self.slot_internal_material_changed)
        self.inputs["ambient"].type_changed.connect(self.slot_ambient_type_changed)
        self.inputs["ambient"].glm_color_changed.connect(self.slot_ambient_color_changed)
        self.inputs["ambient"].file_path_changed.connect(self.slot_ambient_map_changed)
        self.inputs["diffuse"].type_changed.connect(self.slot_diffuse_type_changed)
        self.inputs["diffuse"].glm_color_changed.connect(self.slot_diffuse_color_changed)
        self.inputs["diffuse"].file_path_changed.connect(self.slot_diffuse_map_changed)
        self.inputs["specular"].type_changed.connect(self.slot_specular_type_changed)
        self.inputs["specular"].glm_color_changed.connect(self.slot_specular_color_changed)
        self.inputs["specular"].file_path_changed.connect(self.slot_specular_map_changed)
        self.inputs["shininess_strength"].value_changed.connect(self.slot_shininess_strength_changed)
        self.inputs["shininess"].value_changed.connect(self.slot_shininess_changed)
        self.inputs["emission"].type_changed.connect(self.slot_emission_type_changed)
        self.inputs["emission"].glm_color_changed.connect(self.slot_emission_color_changed)
        self.inputs["emission"].file_path_changed.connect(self.slot_emission_map_changed)
        self.inputs["emission_strength"].value_changed.connect(self.slot_emission_strength_changed)
        self.inputs["rim_power"].value_changed.connect(self.slot_rim_power_changed)
        self.inputs["base_color"].type_changed.connect(self.slot_base_color_type_changed)
        self.inputs["base_color"].glm_color_changed.connect(self.slot_base_color_changed)
        self.inputs["base_color"].file_path_changed.connect(self.slot_base_color_map_changed)
        self.inputs["metallic"].type_changed.connect(self.slot_metallic_type_changed)
        self.inputs["metallic"].value_changed.connect(self.slot_metallic_value_changed)
        self.inputs["metallic"].file_path_changed.connect(self.slot_metallic_map_changed)
        self.inputs["roughness"].type_changed.connect(self.slot_roughness_type_changed)
        self.inputs["roughness"].value_changed.connect(self.slot_roughness_value_changed)
        self.inputs["roughness"].file_path_changed.connect(self.slot_roughness_map_changed)
        self.inputs["diffuse_bands"].value_changed.connect(self.slot_diffuse_bands_changed)
        self.inputs["specular_bands"].value_changed.connect(self.slot_specular_bands_changed)
        self.inputs["diffuse_softness"].value_changed.connect(self.slot_diffuse_softness_changed)
        self.inputs["specular_softness"].value_changed.connect(self.slot_specular_softness_changed)
        self.inputs["reflection"].type_changed.connect(self.slot_reflection_type_changed)
        self.inputs["reflection"].glm_color_changed.connect(self.slot_reflection_color_changed)
        self.inputs["reflection"].file_path_changed.connect(self.slot_reflection_map_changed)
        self.inputs["reflection_opacity"].value_changed.connect(self.slot_reflection_opacity_changed)
        self.inputs["refractive_index"].checked_changed.connect(self.slot_refractive_index_checked_changed)
        self.inputs["refractive_index"].value_changed.connect(self.slot_refractive_index_changed)
        self.inputs["dynamic_env_mapping"].stateChanged.connect(self.slot_dynamic_env_map_changed)
        self.inputs["env_mix_diffuse"].stateChanged.connect(self.slot_env_mix_diffuse_changed)
        self.inputs["opacity"].type_changed.connect(self.slot_opacity_type_changed)
        self.inputs["opacity"].value_changed.connect(self.slot_opacity_value_changed)
        self.inputs["opacity"].file_path_changed.connect(self.slot_opacity_map_changed)
        self.inputs["height_scale"].value_changed.connect(self.slot_height_scale_changed)
        self.inputs["fog"].stateChanged.connect(self.slot_fog_changed)
        self.inputs["recv_shadows"].stateChanged.connect(self.slot_recv_shadows_changed)
        self.inputs["cast_shadows"].stateChanged.connect(self.slot_cast_shadows_changed)
        self.inputs["ao_map"].checked_changed.connect(self.slot_ao_map_checked_changed)
        self.inputs["ao_map"].file_path_changed.connect(self.slot_ao_map_changed)
        self.inputs["normal_map"].checked_changed.connect(self.slot_normal_map_checked_changed)
        self.inputs["normal_map"].file_path_changed.connect(self.slot_normal_map_changed)
        self.inputs["height_map"].checked_changed.connect(self.slot_height_map_checked_changed)
        self.inputs["height_map"].file_path_changed.connect(self.slot_height_map_changed)
        self.inputs["arm_map"].checked_changed.connect(self.slot_arm_map_checked_changed)
        self.inputs["arm_map"].file_path_changed.connect(self.slot_arm_map_changed)
        self.internal_changed.connect(self.slot_internal_changed)
        self.hide_all()

    @property
    def material(self):
        return self.__material
    
    @material.setter
    def material(self, material:Material):
        if self.__material is material:
            return
        
        self.__material = material
        self.should_call_slot = False
        self.inputs["shading_model"].value = material.shading_model
        self.inputs["ambient"].type = (ColorImageChooser.Type.Color if material.ambient_map is None else ColorImageChooser.Type.Image)
        self.inputs["ambient"].glm_color = material.ambient
        self.inputs["ambient"].file_path = ("" if material.ambient_map is None else material.ambient_map.file_name)
        self.inputs["diffuse"].type = (ColorImageChooser.Type.Color if material.diffuse_map is None else ColorImageChooser.Type.Image)
        self.inputs["diffuse"].glm_color = material.diffuse
        self.inputs["diffuse"].file_path = ("" if material.diffuse_map is None else material.diffuse_map.file_name)
        self.inputs["specular"].type = (ColorImageChooser.Type.Color if material.specular_map is None else ColorImageChooser.Type.Image)
        self.inputs["specular"].glm_color = material.specular
        self.inputs["specular"].file_path = ("" if material.specular_map is None else material.specular_map.file_name)
        self.inputs["shininess_strength"].value = material.shininess_strength
        self.inputs["shininess"].value = material.shininess
        self.inputs["emission"].type = (ColorImageChooser.Type.Color if material.emission_map is None else ColorImageChooser.Type.Image)
        self.inputs["emission"].glm_color = material.emission
        self.inputs["emission"].file_path = ("" if material.emission_map is None else material.emission_map.file_name)
        self.inputs["emission_strength"].value = material.emission_strength
        self.inputs["rim_power"].value = material.rim_power
        self.inputs["base_color"].type = (ColorImageChooser.Type.Color if material.base_color_map is None else ColorImageChooser.Type.Image)
        self.inputs["base_color"].glm_color = material.base_color
        self.inputs["base_color"].file_path = ("" if material.base_color_map is None else material.base_color_map.file_name)
        self.inputs["metallic"].type = (ValueImageInput.Type.Value if material.metallic_map is None else ValueImageInput.Type.Image)
        self.inputs["metallic"].value = material.metallic
        self.inputs["metallic"].file_path = ("" if material.metallic_map is None else material.metallic_map.file_name)
        self.inputs["roughness"].type = (ValueImageInput.Type.Value if material.roughness_map is None else ValueImageInput.Type.Image)
        self.inputs["roughness"].value = material.roughness
        self.inputs["roughness"].file_path = ("" if material.roughness_map is None else material.roughness_map.file_name)
        self.inputs["diffuse_bands"].value = material.diffuse_bands
        self.inputs["specular_bands"].value = material.specular_bands
        self.inputs["diffuse_softness"].value = material.diffuse_softness
        self.inputs["specular_softness"].value = material.specular_softness
        self.inputs["reflection"].type = (ColorImageChooser.Type.Color if material.reflection_map is None else ColorImageChooser.Type.Image)
        self.inputs["reflection"].glm_color = material.reflection.rgb
        self.inputs["reflection"].file_path = ("" if material.reflection_map is None else material.reflection_map.file_name)
        self.inputs["reflection_opacity"].value = material.reflection.a
        self.inputs["refractive_index"].value = (material.refractive_index if material.refractive_index > 1E-6 else 1.5)
        self.inputs["refractive_index"].checked = (material.refractive_index > 1E-6)
        self.inputs["dynamic_env_mapping"].setChecked(material.dynamic_env_mapping)
        self.inputs["env_mix_diffuse"].setChecked(material.env_mix_diffuse)
        self.inputs["opacity"].type = (ValueImageInput.Type.Value if material.opacity_map is None else ValueImageInput.Type.Image)
        self.inputs["opacity"].value = material.opacity
        self.inputs["opacity"].file_path = ("" if material.opacity_map is None else material.opacity_map.file_name)
        self.inputs["height_scale"].value = material.height_scale
        self.inputs["fog"].setChecked(material.fog)
        self.inputs["recv_shadows"].setChecked(material.recv_shadows)
        self.inputs["cast_shadows"].setChecked(material.cast_shadows)
        self.inputs["ao_map"].checked = (material.ao_map is not None)
        self.inputs["ao_map"].file_path = ("" if material.ao_map is None else material.ao_map.file_name)
        self.inputs["normal_map"].checked = (material.normal_map is not None)
        self.inputs["normal_map"].file_path = ("" if material.normal_map is None else material.normal_map.file_name)
        self.inputs["height_map"].checked = (material.height_map is not None)
        self.inputs["height_map"].file_path = ("" if material.height_map is None else material.height_map.file_name)
        self.inputs["arm_map"].checked = (material.arm_map is not None)
        self.inputs["arm_map"].file_path = ("" if material.arm_map is None else material.arm_map.file_name)
        self.should_call_slot = True

    def hide_all(self):
        shading_model = self.inputs["shading_model"].value
        for key, component in self.inputs.items():
            if key not in self.parameters_map:
                continue

            if shading_model in self.parameters_map[key]:
                component.show()
            else:
                component.hide()

    @slot
    def slot_internal_changed(self):
        self.should_call_slot = False
        self.inputs["internal_material"].value = None
        self.should_call_slot = True

    @slot
    def slot_shading_model_changed(self, shading_model):
        self.__material.shading_model = shading_model
        self.hide_all()
        self.material_changed.emit()

    @slot
    def slot_internal_material_changed(self, internal_material):
        self.__material.set_as(internal_material)
        self.material_changed.emit()

    @slot
    def slot_ambient_type_changed(self, type):
        if type == ColorImageChooser.Type.Color:
            self.__material.ambient_map = None
            self.__material.ambient = self.inputs["ambient"].glm_color
        elif os.path.isfile(self.inputs["ambient"].file_path):
            self.__material.ambient_map = self.inputs["ambient"].file_path
        self.material_changed.emit()
        self.internal_changed.emit()

    @slot
    def slot_ambient_color_changed(self, color):
        self.__material.ambient = color
        self.material_changed.emit()
        self.internal_changed.emit()

    @slot
    def slot_ambient_map_changed(self, ambient_map):
        self.__material.ambient_map = ambient_map
        self.material_changed.emit()
        self.internal_changed.emit()

    @slot
    def slot_diffuse_type_changed(self, type):
        if type == ColorImageChooser.Type.Color:
            self.__material.diffuse_map = None
            self.__material.diffuse = self.inputs["diffuse"].glm_color
        elif os.path.isfile(self.inputs["diffuse"].file_path):
            self.__material.diffuse_map = self.inputs["diffuse"].file_path
        self.material_changed.emit()
        self.internal_changed.emit()

    @slot
    def slot_diffuse_color_changed(self, color):
        self.__material.diffuse = color
        self.material_changed.emit()
        self.internal_changed.emit()

    @slot
    def slot_diffuse_map_changed(self, diffuse_map):
        self.__material.diffuse_map = diffuse_map
        self.material_changed.emit()
        self.internal_changed.emit()

    @slot
    def slot_specular_type_changed(self, type):
        if type == ColorImageChooser.Type.Color:
            self.__material.specular_map = None
            self.__material.specular = self.inputs["specular"].glm_color
        elif os.path.isfile(self.inputs["specular"].file_path):
            self.__material.specular_map = self.inputs["specular"].file_path
        self.material_changed.emit()
        self.internal_changed.emit()

    @slot
    def slot_specular_color_changed(self, color):
        self.__material.specular = color
        self.material_changed.emit()
        self.internal_changed.emit()

    @slot
    def slot_specular_map_changed(self, specular_map):
        self.__material.specular_map = specular_map
        self.material_changed.emit()
        self.internal_changed.emit()

    @slot
    def slot_shininess_strength_changed(self, shininess_strength):
        self.__material.shininess_strength = shininess_strength
        self.material_changed.emit()

    @slot
    def slot_shininess_changed(self, shininess):
        self.__material.shininess = shininess
        self.material_changed.emit()

    @slot
    def slot_emission_type_changed(self, type):
        if type == ColorImageChooser.Type.Color:
            self.__material.emission_map = None
            self.__material.emission = self.inputs["emission"].glm_color
        elif os.path.isfile(self.inputs["emission"].file_path):
            self.__material.emission_map = self.inputs["emission"].file_path
        self.material_changed.emit()

    @slot
    def slot_emission_color_changed(self, color):
        self.__material.emission = color
        self.material_changed.emit()

    @slot
    def slot_emission_map_changed(self, emission_map):
        self.__material.emission_map = emission_map
        self.material_changed.emit()

    @slot
    def slot_emission_strength_changed(self, emission_strength):
        self.__material.emission_strength = emission_strength
        self.material_changed.emit()

    @slot
    def slot_rim_power_changed(self, rim_power):
        self.__material.rim_power = rim_power
        self.material_changed.emit()

    @slot
    def slot_base_color_type_changed(self, type):
        if type == ColorImageChooser.Type.Color:
            self.__material.base_color_map = None
            self.__material.base_color = self.inputs["base_color"].glm_color
        elif os.path.isfile(self.inputs["base_color"].file_path):
            self.__material.base_color_map = self.inputs["base_color"].file_path
        self.material_changed.emit()

    @slot
    def slot_base_color_changed(self, color):
        self.__material.base_color = color
        self.material_changed.emit()

    @slot
    def slot_base_color_map_changed(self, base_color_map):
        self.__material.base_color_map = base_color_map
        self.material_changed.emit()

    @slot
    def slot_metallic_type_changed(self, type):
        if type == ValueImageInput.Type.Value:
            self.__material.metallic_map = None
            self.__material.metallic = self.inputs["metallic"].value
        elif os.path.isfile(self.inputs["metallic"].file_path):
            self.__material.metallic_map = self.inputs["metallic"].file_path
        self.material_changed.emit()

    @slot
    def slot_metallic_value_changed(self, metallic):
        self.__material.metallic = metallic
        self.material_changed.emit()

    @slot
    def slot_metallic_map_changed(self, metallic_map):
        self.__material.metallic_map = metallic_map
        self.material_changed.emit()

    @slot
    def slot_roughness_type_changed(self, type):
        if type == ValueImageInput.Type.Value:
            self.__material.roughness = self.inputs["roughness"].value
            self.__material.roughness_map = None
        elif os.path.isfile(self.inputs["roughness"].file_path):
            self.__material.roughness_map = self.inputs["roughness"].file_path
        self.material_changed.emit()

    @slot
    def slot_roughness_value_changed(self, value):
        self.__material.roughness = self.inputs["roughness"].value
        self.material_changed.emit()

    @slot
    def slot_roughness_map_changed(self, file_path):
        self.__material.roughness_map = file_path
        self.material_changed.emit()

    @slot
    def slot_diffuse_bands_changed(self, n_bands):
        self.__material.diffuse_bands = n_bands
        self.material_changed.emit()

    @slot
    def slot_specular_bands_changed(self, n_bands):
        self.__material.specular_bands = n_bands
        self.material_changed.emit()

    @slot
    def slot_diffuse_softness_changed(self, softness):
        self.__material.diffuse_softness = softness
        self.material_changed.emit()

    @slot
    def slot_specular_softness_changed(self, softness):
        self.__material.specular_softness = softness
        self.material_changed.emit()

    @slot
    def slot_reflection_type_changed(self, type):
        if type == ColorImageChooser.Type.Color:
            self.__material.reflection_map = None
            self.__material.reflection = glm.vec4(self.inputs["reflection"].glm_color, self.inputs["reflection_opacity"].value)
        elif os.path.isfile(self.inputs["reflection"].file_path):
            self.__material.reflection_map = self.inputs["reflection"].file_path
        
        self.material_changed.emit()

    @slot
    def slot_reflection_color_changed(self, color):
        self.__material.reflection = glm.vec4(color, self.inputs["reflection_opacity"].value)
        self.material_changed.emit()

    @slot
    def slot_reflection_map_changed(self, file_path):
        self.__material.reflection_map = file_path
        self.material_changed.emit()

    @slot
    def slot_reflection_opacity_changed(self, opacity):
        self.__material.reflection.a = opacity
        self.material_changed.emit()

    @slot
    def slot_refractive_index_changed(self, refractive_index):
        self.__material.refractive_index = refractive_index
        self.inputs["reflection"].glm_color = self.__material.reflection.rgb
        self.inputs["reflection_opacity"].value = self.__material.reflection.a
        self.material_changed.emit()

    @slot
    def slot_refractive_index_checked_changed(self, checked):
        self.__material.refractive_index = (self.inputs["refractive_index"].value if checked else 0)
        self.inputs["reflection"].glm_color = self.__material.reflection.rgb
        self.inputs["reflection_opacity"].value = self.__material.reflection.a
        self.material_changed.emit()

    @slot
    def slot_dynamic_env_map_changed(self, state):
        self.__material.dynamic_env_mapping = (state == Qt.CheckState.Checked.value)
        self.material_changed.emit()

    @slot
    def slot_env_mix_diffuse_changed(self, state):
        self.__material.env_mix_diffuse = (state == Qt.CheckState.Checked.value)
        self.material_changed.emit()

    @slot
    def slot_opacity_type_changed(self, type):
        if type == ValueImageInput.Type.Value:
            self.__material.opacity = self.inputs["opacity"].value
            self.__material.opacity_map = None
        elif os.path.isfile(self.inputs["opacity"].file_path):
            self.__material.opacity_map = self.inputs["opacity"].file_path
        self.material_changed.emit()

    @slot
    def slot_opacity_value_changed(self, value):
        self.__material.opacity = value
        self.material_changed.emit()

    @slot
    def slot_opacity_map_changed(self, file_path):
        self.__material.opacity_map = file_path
        self.material_changed.emit()

    @slot
    def slot_height_scale_changed(self, value):
        self.__material.height_scale = value
        self.material_changed.emit()

    @slot
    def slot_fog_changed(self, state):
        self.__material.fog = (state == Qt.CheckState.Checked.value)
        self.material_changed.emit()

    @slot
    def slot_recv_shadows_changed(self, state):
        self.__material.recv_shadows = (state == Qt.CheckState.Checked.value)
        self.material_changed.emit()

    @slot
    def slot_cast_shadows_changed(self, state):
        self.__material.cast_shadows = (state == Qt.CheckState.Checked.value)
        self.material_changed.emit()

    @slot
    def slot_ao_map_checked_changed(self, checked):
        if checked and os.path.isfile(self.inputs["ao_map"].file_path):
            self.__material.ao_map = self.inputs["ao_map"].file_path
        else:
            self.__material.ao_map = None
        self.material_changed.emit()

    @slot
    def slot_ao_map_changed(self, ao_map):
        self.__material.ao_map = ao_map
        self.material_changed.emit()

    @slot
    def slot_normal_map_checked_changed(self, checked):
        if checked and os.path.isfile(self.inputs["normal_map"].file_path):
            self.__material.normal_map = self.inputs["normal_map"].file_path
        else:
            self.__material.normal_map = None
        self.material_changed.emit()

    @slot
    def slot_normal_map_changed(self, normal_map):
        self.__material.normal_map = normal_map
        self.material_changed.emit()

    @slot
    def slot_height_map_checked_changed(self, checked):
        if checked and os.path.isfile(self.inputs["height_map"].file_path):
            self.__material.height_map = self.inputs["height_map"].file_path
        else:
            self.__material.height_map = None
        self.material_changed.emit()

    @slot
    def slot_height_map_changed(self, height_map):
        self.__material.height_map = height_map
        self.material_changed.emit()

    @slot
    def slot_arm_map_checked_changed(self, checked):
        if checked and os.path.isfile(self.inputs["arm_map"].file_path):
            self.__material.arm_map = self.inputs["arm_map"].file_path
        else:
            self.__material.arm_map = None
        self.material_changed.emit()

    @slot
    def slot_arm_map_changed(self, arm_map):
        self.__material.arm_map = arm_map
        self.material_changed.emit()

class MainWindow(QDialog):

    def __init__(self, parent:QWidget=None):
        QDialog.__init__(self, parent=parent)
        self.setWindowFlags(Qt.WindowType.WindowMinMaxButtonsHint | Qt.WindowType.WindowCloseButtonHint)
        self.setWindowTitle('glass_engine 材质编辑概念演示')

        self_folder = os.path.dirname(os.path.abspath(__file__))
        self.setWindowIcon(QIcon(self_folder + "/../images/glass_engine_logo64.png"))

        self.scene, self.camera, dir_light = ModelView()
        self.scene.skydome = "https://dl.polyhaven.org/file/ph-assets/HDRIs/extra/Tonemapped%20JPG/industrial_sunset_puresky.jpg"
        self.camera.screen.bloom = True
        
        sphere = Sphere()
        sphere.material.opacity = 1
        sphere.color = glm.vec4(1,1,1,0)
        self.scene.add(sphere)

        self_path = os.path.dirname(os.path.abspath(__file__))
        model = Model(self_path + "/assets/models/jet/11805_airplane_v2_L2.obj")
        model["root"].scale = 1/300
        model["root"].position.z -= 1
        model.position.y = 5
        model.yaw = 45
        self.scene.add(model)

        floor = Floor()
        floor.position.z = -1
        self.scene.add(floor)

        self.material_editor = MaterialEditor(sphere.material)
        self.splitter = QSplitter()
        self.splitter.addWidget(self.camera.screen)
        self.splitter.addWidget(self.material_editor)
        self.material_editor.material_changed.connect(self.slot_material_changed)

        hlayout = QHBoxLayout()
        hlayout.addWidget(self.splitter)
        self.setLayout(hlayout)

    def slot_material_changed(self):
        self.camera.screen.update()

def demo_material():
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme='dark_amber.xml')

    main_window = MainWindow()
    main_window.show()

    app.exec()