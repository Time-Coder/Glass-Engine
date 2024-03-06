__version__ = "0.1.52"

from .Scene import Scene
from .SceneNode import SceneNode
from .BasicScene import SceneRoam, ModelView

from .Camera import Camera
from .Material import Material
from .Mesh import Mesh
from .Model import Model

from .ColorMap import ColorMap
from .Frame import Frame
from .Fog import Fog

import glm
import platform

if platform.machine() == "aarch64":
    from OpenGL import GLES2 as GL
else:
    from OpenGL import GL
from glass import GlassConfig
