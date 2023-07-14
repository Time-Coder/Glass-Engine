from glass import FBO, sampler2D, sampler2DMS, samplerCube, ShaderProgram
from glass.DictList import DictList
from glass.utils import checktype
from .Renderers.FlatCamera import FlatCamera
from .CutomSamplerCube import CustomSamplerCube

class SphericalToCube:

    __fbos = {}
    __ms_infos = {}
    __program = None
    __ms_program = None
    __flat_cameras = DictList()
    __skydom = None

    @staticmethod
    @checktype
    def spherical_to_cube(spherical_map:sampler2D, update:bool=None)->samplerCube:
        if update is None:
            update = spherical_map.is_dynamic_shadertoy

        if spherical_map is None or spherical_map.id == 0:
            return None
        
        fbo = None
        if spherical_map.id in SphericalToCube.__fbos:
            fbo = SphericalToCube.__fbos[spherical_map.id]
        else:
            fbo = FBO(1024, 1024)
            fbo.attach(0, samplerCube)
            SphericalToCube.__fbos[spherical_map.id] = fbo
            update = True

        if not update:
            return fbo.color_attachment(0)
        
        if not SphericalToCube.__flat_cameras:
            SphericalToCube.__flat_cameras["right"] = FlatCamera("right")
            SphericalToCube.__flat_cameras["left"] = FlatCamera("left")
            SphericalToCube.__flat_cameras["bottom"] = FlatCamera("bottom")
            SphericalToCube.__flat_cameras["top"] = FlatCamera("top")
            SphericalToCube.__flat_cameras["front"] = FlatCamera("front")
            SphericalToCube.__flat_cameras["back"] = FlatCamera("back")

        if SphericalToCube.__program is None:
            SphericalToCube.__program = ShaderProgram()
            SphericalToCube.__program.compile("glsl/spherical_to_cube/spherical_to_cube.vs")
            SphericalToCube.__program.compile("glsl/spherical_to_cube/spherical_to_cube.gs")
            SphericalToCube.__program.compile("glsl/spherical_to_cube/spherical_to_cube.fs")
            SphericalToCube.__program["cameras"] = SphericalToCube.__flat_cameras

        if SphericalToCube.__skydom is None:
            from .SkyDome import SkyDome
            SphericalToCube.__skydom = SkyDome()

        SphericalToCube.__program["spherical_map"] = spherical_map
        with fbo:
            SphericalToCube.__program.draw_triangles(
                SphericalToCube.__skydom.vertices,
                SphericalToCube.__skydom.indices
            )

        return fbo.color_attachment(0)
    
    @staticmethod
    @checktype
    def spherical_to_cube_ms(spherical_map:sampler2D, update:bool=None, samples:int=4)->CustomSamplerCube:
        if update is None:
            update = spherical_map.is_dynamic_shadertoy

        if spherical_map is None or spherical_map.id == 0:
            return CustomSamplerCube()
        
        cube_map = None
        fbos = None
        if spherical_map.id in SphericalToCube.__ms_infos:
            cube_map = SphericalToCube.__ms_infos[spherical_map.id]["cube_map"]
            fbos = SphericalToCube.__ms_infos[spherical_map.id]["fbos"]
        else:
            cube_map = CustomSamplerCube()
            fbos = []
            for i in range(6):
                fbo = FBO(1024, 1024, samples)
                fbo.attach(0, sampler2DMS)
                fbos.append(fbo)

            SphericalToCube.__ms_infos[spherical_map.id] = \
            {
                "cube_map": cube_map,
                "fbos": fbos
            }
            update = True

        if not update:
            return cube_map

        if not SphericalToCube.__flat_cameras:
            SphericalToCube.__flat_cameras["right"] = FlatCamera("right")
            SphericalToCube.__flat_cameras["left"] = FlatCamera("left")
            SphericalToCube.__flat_cameras["bottom"] = FlatCamera("bottom")
            SphericalToCube.__flat_cameras["top"] = FlatCamera("top")
            SphericalToCube.__flat_cameras["front"] = FlatCamera("front")
            SphericalToCube.__flat_cameras["back"] = FlatCamera("back")

        if SphericalToCube.__ms_program is None:
            SphericalToCube.__ms_program = ShaderProgram()
            SphericalToCube.__ms_program.compile("glsl/spherical_to_cube/spherical_to_cube_ms.vs")
            SphericalToCube.__ms_program.compile("glsl/spherical_to_cube/spherical_to_cube_ms.fs")
            SphericalToCube.__ms_program["cameras"] = SphericalToCube.__flat_cameras

        if SphericalToCube.__skydom is None:
            from .SkyDome import SkyDome
            SphericalToCube.__skydom = SkyDome()
        
        for i in range(6):
            with fbos[i]:
                SphericalToCube.__ms_program["spherical_map"] = spherical_map
                SphericalToCube.__ms_program["camera_index"] = i
                SphericalToCube.__ms_program.draw_triangles(SphericalToCube.__skydom.vertices, SphericalToCube.__skydom.indices)
            cube_map[i] = fbos[i].resolved.color_attachment(0)

        return cube_map
    
spherical_to_cube = SphericalToCube.spherical_to_cube
spherical_to_cube_ms = SphericalToCube.spherical_to_cube_ms