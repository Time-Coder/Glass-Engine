from glass_engine import *
from glass_engine.Geometries import * # 导入所有的基本几何体
from glass_engine.Lights import *
from glass_engine.Renderers import *

GlassConfig.debug = True
GlassConfig.recompile = True

scene = Scene()
camera = Camera()
scene.add(camera)
camera.position.y = -5
camera.position.z = 1.7
camera.pitch = -15

# floor = Floor()
# scene.add(floor)

light = DirLight()
light.pitch = -45
# light.position.z = 4
light.yaw = 45
scene.add(light)
scene.skydome = "https://dl.polyhaven.org/file/ph-assets/HDRIs/extra/Tonemapped%20JPG/hochsal_field.jpg"
light.generate_shadows = False

sphere = Sphere() # 创建一个球体模型
sphere.material.shading_model = Material.ShadingModel.Gouraud
sphere.position.z = 1 # 设置球体位置
# sphere.material.reflection.a = 1
# sphere.material.dynamic_env_mapping = True
scene.add(sphere) # 将球体添加到场景中

# camera.screen.renderer = DeferredRenderer()
camera.screen.show() # 相机显示屏显示渲染结果