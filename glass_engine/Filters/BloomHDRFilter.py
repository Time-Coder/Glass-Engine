from .Filters import Filter
from .LightExtractFilter import LightExtractFilter
from ..Frame import Frame

from glass import FBO, sampler2D, ShaderProgram, GLConfig
from glass.utils import checktype

from OpenGL import GL

class BloomHDRFilter(Filter):

    @checktype
    def __init__(self, bloom:bool=True, HDR:bool=False):
        self.last_src_width = 0
        self.last_src_height = 0

        self.bloom_down_fbo_list = []
        self.bloom_up_fbo_list = []
        self.hdr_down_fbo_list = []
        self.hdr_up_fbo_list = []
        self.used_length = 0

        self.light_extract_filter = LightExtractFilter()

        self.down_program = ShaderProgram()
        self.down_program.compile("../glsl/Pipelines/draw_frame.vs")
        self.down_program.compile("../glsl/Filters/bloom_downsampling.fs")

        self.up_program = ShaderProgram()
        self.up_program.compile("../glsl/Pipelines/draw_frame.vs")
        self.up_program.compile("../glsl/Filters/bloom_upsampling.fs")

        self.mix_fbo = FBO()
        self.mix_fbo.attach(0, sampler2D)
        self.mix_program = ShaderProgram()
        self.mix_program.compile("../glsl/Pipelines/draw_frame.vs")
        self.mix_program.compile("../glsl/Filters/bloom_mix.fs")

        self.__enable_bloom = bloom
        self.__enable_HDR = HDR
        self.mix_program["enable_bloom"] = self.__enable_bloom
        self.mix_program["enable_HDR"] = self.__enable_HDR

    def __call__(self, screen_image:sampler2D)->sampler2D:
        if not self.__enable_bloom and not self.__enable_HDR:
            return screen_image

        self.__update_fbo_list(screen_image.width, screen_image.height)

        bloom_image = None
        luminance_image = None
        if self.__enable_bloom:
            bloom_image = self.light_extract_filter(screen_image)
            with GLConfig.LocalConfig(cull_face=None, polygon_mode=GL.GL_FILL):
                for i in range(self.used_length):
                    down_fbo = self.bloom_down_fbo_list[i]
                    with down_fbo:
                        self.down_program["mip_level"] = i
                        self.down_program["screen_image"] = bloom_image
                        self.down_program.draw_triangles(Frame.vertices, Frame.indices)
                    bloom_image = down_fbo.color_attachment(0)

                for i in range(self.used_length-1, 0, -1):
                    up_fbo = self.bloom_up_fbo_list[i]
                    down_fbo = self.bloom_down_fbo_list[i]
                    with up_fbo:
                        self.up_program["filter_radius"] = up_fbo.width/10000
                        self.up_program["screen_image"] = bloom_image
                        self.up_program["original_image"] = down_fbo.color_attachment(0)
                        self.up_program.draw_triangles(Frame.vertices, Frame.indices)
                    bloom_image = up_fbo.color_attachment(0)

        if self.__enable_HDR:
            luminance_image = screen_image
            with GLConfig.LocalConfig(cull_face=None, polygon_mode=GL.GL_FILL):
                for i in range(self.used_length):
                    down_fbo = self.hdr_down_fbo_list[i]
                    with down_fbo:
                        self.down_program["mip_level"] = i
                        self.down_program["screen_image"] = luminance_image
                        self.down_program.draw_triangles(Frame.vertices, Frame.indices)
                    luminance_image = down_fbo.color_attachment(0)

                for i in range(self.used_length-1, 0, -1):
                    up_fbo = self.hdr_up_fbo_list[i]
                    down_fbo = self.hdr_down_fbo_list[i]
                    with up_fbo:
                        self.up_program["filter_radius"] = up_fbo.width/10000
                        self.up_program["screen_image"] = luminance_image
                        self.up_program["original_image"] = down_fbo.color_attachment(0)
                        self.up_program.draw_triangles(Frame.vertices, Frame.indices)
                    luminance_image = up_fbo.color_attachment(0)
    
        self.mix_fbo.resize(screen_image.width, screen_image.height)
        with GLConfig.LocalConfig(cull_face=None, polygon_mode=GL.GL_FILL):
            with self.mix_fbo:
                self.mix_program["screen_image"] = screen_image
                self.mix_program["bloom_image"] = bloom_image
                self.mix_program["luminance_image"] = luminance_image
                self.mix_program.draw_triangles(Frame.vertices, Frame.indices)
        return self.mix_fbo.color_attachment(0)

    @property
    def enable_bloom(self):
        return self.__enable_bloom
    
    @enable_bloom.setter
    @checktype
    def enable_bloom(self, flag:bool):
        self.__enable_bloom = flag
        self.mix_program["enable_bloom"] = flag
    
    @property
    def enable_HDR(self):
        return self.__enable_HDR
    
    @enable_HDR.setter
    @checktype
    def enable_HDR(self, flag:bool):
        self.__enable_HDR = flag
        self.mix_program["enable_HDR"] = flag

    def __update_fbo_list(self, src_width:int, src_height:int):
        if src_width == self.last_src_width and \
           src_height == self.last_src_height:
            return
        
        dest_width = 16
        dest_height = int(dest_width / src_width * src_height)

        width_list, height_list = [], []
        width, height = src_width, src_height

        is_width_down = (src_width > dest_width)
        scale = 0.5 if is_width_down else 2
        while (width > dest_width) == is_width_down:
            width = int(width * scale)
            width_list.append(width)

        is_height_down = (height > dest_height)
        scale = 0.5 if is_height_down else 2
        while (height > dest_height) == is_height_down:
            height = int(height * scale)
            height_list.append(height)

        len_width_list = len(width_list)
        len_height_list = len(height_list)
        delta_len = len_height_list - len_width_list

        if delta_len > 0:
            width_list.extend([width_list[-1]]*delta_len)
            len_width_list += delta_len
        elif delta_len < 0:
            height_list.extend([height_list[-1]]*(-delta_len))
            len_height_list -= delta_len

        len_bloom_down_fbo_list = len(self.bloom_down_fbo_list)
        while len_bloom_down_fbo_list < len_width_list:
            fbo = FBO()
            fbo.attach(0, sampler2D)
            self.bloom_down_fbo_list.append(fbo)
            len_bloom_down_fbo_list += 1

            fbo = FBO()
            fbo.attach(0, sampler2D)
            self.hdr_down_fbo_list.append(fbo)

        len_bloom_up_fbo_list = len(self.bloom_up_fbo_list)
        while len_bloom_up_fbo_list < len_width_list:
            fbo = FBO()
            fbo.attach(0, sampler2D)
            self.bloom_up_fbo_list.append(fbo)
            len_bloom_up_fbo_list += 1

            fbo = FBO()
            fbo.attach(0, sampler2D)
            self.hdr_up_fbo_list.append(fbo)

        self.used_length = len_width_list

        for i in range(len_width_list):
            bloom_down_fbo = self.bloom_down_fbo_list[i]
            bloom_up_fbo = self.bloom_up_fbo_list[i]
            hdr_down_fbo = self.hdr_down_fbo_list[i]
            hdr_up_fbo = self.hdr_up_fbo_list[i]

            width = width_list[i]
            height = height_list[i]

            bloom_down_fbo.resize(width, height)
            bloom_up_fbo.resize(width, height)
            hdr_down_fbo.resize(width, height)
            hdr_up_fbo.resize(width, height)

        self.last_src_width = src_width
        self.last_src_height = src_height
