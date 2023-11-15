from .demo_transform import demo_transform
from .demo_material import demo_material

def demo(name:str):
    if name == "transform":
        demo_transform()
    elif name == "material":
        demo_material()