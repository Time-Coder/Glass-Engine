from .SingleShaderFilter import SingleShaderFilter
from ..Frame import Frame

from glass import sampler2D, FBO, ShaderProgram

class PyramidSamplingFilter(SingleShaderFilter):

    def __init__(self, dest_shape:tuple, shader_path:str=None):
        SingleShaderFilter.__init__(self, shader_path)
        
        self.dest_width = dest_shape[0]
        self.dest_height = dest_shape[1]
        self.last_dest_width = 0
        self.last_dest_height = 0
        self.last_src_width = 0
        self.last_src_height = 0

        self.fbo_list = []
        self.used_length = 0

    def __call__(self, screen_image:sampler2D)->sampler2D:
        self.__update_fbo_list(screen_image.width, screen_image.height)
        for i in range(self.used_length):
            fbo = self.fbo_list[i]
            if self.shader_path is None:
                with fbo:
                    Frame.draw(screen_image)
                screen_image = fbo.color_attachment(0)
            else:
                screen_image = self._call(fbo, screen_image)
        return screen_image
    
    @property
    def dest_shape(self):
        return (self.dest_width, self.dest_height)
    
    @dest_shape.setter
    def dest_shape(self, shape:tuple):
        self.dest_width = shape[0]
        self.dest_height = shape[1]

    def __update_fbo_list(self, src_width:int, src_height:int):
        if self.dest_width == self.last_dest_width and \
           self.dest_height == self.last_dest_height and \
           src_width == self.last_src_width and \
           src_height == self.last_src_height:
            return
        
        dest_width, dest_height = self.dest_width, self.dest_height
        if dest_width < 0:
            dest_width = int(dest_height / src_height * src_width)
        if dest_height < 0:
            dest_height = int(dest_width / src_width * src_height)

        width_list, height_list = [], []
        width, height = src_width, src_height

        is_width_down = (src_width > dest_width)
        scale = 0.5 if is_width_down else 2
        while (width > dest_width) == is_width_down:
            width = int(width * scale)
            width_list.append(width)
        width_list[-1] = dest_width

        is_height_down = (height > dest_height)
        scale = 0.5 if is_height_down else 2
        while (height > dest_height) == is_height_down:
            height = int(height * scale)
            height_list.append(height)
        height_list[-1] = dest_height

        len_width_list = len(width_list)
        len_height_list = len(height_list)
        delta_len = len_height_list - len_width_list
        if delta_len > 0:
            width_list.extend([width_list[-1]] * delta_len)
            len_width_list += delta_len
        elif delta_len < 0:
            height_list.extend([height_list[-1]]*(-delta_len))
            len_height_list -= delta_len

        len_fbo_list = len(self.fbo_list)
        while len_fbo_list < len_width_list:
            fbo = FBO()
            fbo.attach(0, sampler2D)
            self.fbo_list.append(fbo)
            len_fbo_list += 1

        self.used_length = len_width_list

        for i in range(len_width_list):
            fbo = self.fbo_list[i]
            width = width_list[i]
            height = height_list[i]
            fbo.resize(width, height)

        self.last_dest_width = self.dest_width
        self.last_dest_height = self.dest_height
        self.last_src_width = src_width
        self.last_src_height = src_height