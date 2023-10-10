import cv2
import numpy as np
import glm
from OpenGL import GL
import OpenGL.GL.ARB.bindless_texture as bt

from .FBOAttachment import FBOAttachment
from .GLInfo import GLInfo
from .utils import checktype
from .ImageLoader import ImageLoader
from .helper import get_external_format, width_adapt, get_dtype, get_channels

class sampler2DArray(FBOAttachment):

    _default_internal_format = GL.GL_RGBA32F
    _default_filter_min = GL.GL_LINEAR
    _default_filter_mag = GL.GL_LINEAR
    _default_filter_mipmap = GL.GL_LINEAR

    _basic_info = \
    {
        "gen_func": GL.glGenTextures,
        "bind_func": GL.glBindTexture,
        "del_func": GL.glDeleteTextures,
        "target_type": GL.GL_TEXTURE_2D_ARRAY,
        "binding_type": GL.GL_TEXTURE_BINDING_2D_ARRAY,
        "need_number": True,
    }

    class Images:
        def __init__(self, parent):
            self._images = []
            self._parent = parent

        @checktype
        def __getitem__(self, index:int):
            return self._images[index]
        
        @checktype
        def __setitem__(self, index:int, image:(str,np.ndarray)):
            if isinstance(image, str):
                image = ImageLoader.load(image)

            self._images[index] = image

            if image is None:
                return
            
            if image.shape[1] > self._parent.width:
                self._parent.width = image.shape[1]

            if image.shape[0] > self._parent.height:
                self._parent.height = image.shape[0]

            channels = image.shape[2] if len(image.shape) > 2 else 1
            internal_format = GLInfo.internal_formats_map[image.dtype][channels]
            if internal_format != self._parent._internal_format:
                self._parent._internal_format = internal_format
                self._parent._image_size_changed = True

            self._parent._image_layer_changed[index] = True

        def __delitem__(self, index):
            del self._images[index]
            del self._parent._image_layer_changed[index]

        def __contains__(self, image):
            return image in self._images

        def __len__(self):
            return len(self._images)

        def append(self, image:(str,np.ndarray)):
            self._images.append(None)
            index = len(self._images) - 1
            self._parent._image_layer_changed.append(False)
            self._parent._image_size_changed = True

            self[index] = image

        def insert(self, index, image:(str,np.ndarray)):
            self._images.insert(index, image)
            self._parent._image_layer_changed.insert(index, False)
            self._parent._image_size_changed = True

            self[index] = image

        def index(self, image):
            return self._images.index(image)
        
        def clear(self):
            if not self._images:
                return
            
            self._images.clear()
            self._parent._image_layer_changed.clear()
            self._parent._image_size_changed = True

        def pop(self, index:int=None):
            self._images.pop(index)
            self._parent._image_layer_changed.pop(index)
            self._parent._image_size_changed = True
            
    @checktype
    def __init__(self, images:list=None, width:int=None, height:int=None, layers:int=None, internal_format:GLInfo.internal_formats=None):
        FBOAttachment.__init__(self)
        
        self._handle = 0
        self._images = sampler2DArray.Images(self)
        self._width = 0
        self._height = 0
        self._internal_format = self.__class__._default_internal_format

        self._wrap_r = GL.GL_CLAMP_TO_EDGE
        self._wrap_s = GL.GL_REPEAT
        self._wrap_t = GL.GL_REPEAT
        self._filter_min = self.__class__._default_filter_min
        self._filter_mag = self.__class__._default_filter_mag
        self._filter_mipmap = self.__class__._default_filter_mipmap
        self._border_color = glm.vec4(0, 0, 0, 1)

        self._image_size_changed = True
        self._image_layer_changed = []
        self._wrap_r_changed = True
        self._wrap_s_changed = True
        self._wrap_t_changed = True
        self._filter_min_changed = True
        self._filter_mag_changed = True
        self._border_color_changed = False

        if images is not None:
            for image in images:
                self._images.append(image)
        elif layers is not None:
            self.layers = layers

        if width is not None:
            self.width = width

        if height is not None:
            self.height = height

        if internal_format is not None:
            self.internal_format = internal_format

    def __del__(self):
        if self._handle != 0:
            # bt.glMakeTextureHandleNonResidentARB(self._handle)
            self._handle = 0

        FBOAttachment.__del__(self)

    def __hash__(self):
        return id(self)

    def __deepcopy__(self, memo):
        result = self.__class__()
        result._images = self._images
        result._width = self._width
        result._height = self._height
        result._internal_format = self._internal_format

        result._wrap_s = self._wrap_s
        result._wrap_t = self._wrap_t
        result._filter_min = self._filter_min
        result._filter_mag = self._filter_mag
        result._filter_mipmap = self._filter_mipmap
        result._border_color = self._border_color

        return result

    @property
    def handle(self):
        if not bt.glGetTextureHandleARB:
            return 0
        
        self.bind()
        if self._handle == 0:
            self._handle = bt.glGetTextureHandleARB(self._id)
            if self._handle == 0:
                raise RuntimeError(f"failed to create sampler2DArray {self._id}'s handle")
            bt.glMakeTextureHandleResidentARB(self._handle)            

        return self._handle

    def bind(self, update_fbo:bool=False, force_update_image:bool=False):
        FBOAttachment.bind(self, update_fbo)

        if self._wrap_r_changed:
            GL.glTexParameteri(GL.GL_TEXTURE_2D_ARRAY, GL.GL_TEXTURE_WRAP_R, self._wrap_r)
            self._wrap_r_changed = False
        if self._wrap_s_changed:
            GL.glTexParameteri(GL.GL_TEXTURE_2D_ARRAY, GL.GL_TEXTURE_WRAP_S, self._wrap_s)
            self._wrap_s_changed = False
        if self._wrap_t_changed:
            GL.glTexParameteri(GL.GL_TEXTURE_2D_ARRAY, GL.GL_TEXTURE_WRAP_T, self._wrap_t)
            self._wrap_t_changed = False
        if self._border_color_changed:
            GL.glTexParameterfv(GL.GL_TEXTURE_2D_ARRAY, GL.GL_TEXTURE_BORDER_COLOR, glm.value_ptr(self._border_color))
            self._border_color_changed = False

        if self._filter_min_changed:
            GL.glTexParameteri(GL.GL_TEXTURE_2D_ARRAY, GL.GL_TEXTURE_MIN_FILTER, self._get_filter_min())
            self._filter_min_changed = False
        if self._filter_mag_changed:
            GL.glTexParameteri(GL.GL_TEXTURE_2D_ARRAY, GL.GL_TEXTURE_MAG_FILTER, self._filter_mag)
            self._filter_mag_changed = False

        generated_mipmap = False
        external_format = get_external_format(self._internal_format)
        if force_update_image or self._image_size_changed:
            width_adapt(self._width)
            GL.glTexImage3D(GL.GL_TEXTURE_2D_ARRAY, 0, self._internal_format,
                            self._width, self._height, self.layers, 0, external_format, self.dtype, None)
            
            if not update_fbo and self._filter_mipmap is not None and self._image is not None:
                self.generate_mipmap()
                generated_mipmap = True

            self._image_size_changed = False

        for layer in range(self.layers):
            if self._image_layer_changed[layer]:
                GL.glTexSubImage3D(GL.GL_TEXTURE_2D_ARRAY, 0, 0, 0, layer, self.width, self.height, 1, external_format, self.dtype, self.images[layer])

        if not update_fbo and not generated_mipmap and not self._fbo_image_generated_mipmap:
            if self._filter_mipmap is not None:
                self.generate_mipmap()

            self._fbo_image_generated_mipmap = True

    def generate_mipmap(self):
        FBOAttachment.bind(self)
        GL.glGenerateMipmap(GL.GL_TEXTURE_2D_ARRAY)

    def clear(self):
        if self._id == 0:
            return

        self.bind()
        external_format = get_external_format(self._internal_format)
        dtype = get_dtype(self._internal_format)
        GL.glClearTexImage(self._id, 0, external_format, dtype, None)

    @property
    def width(self):
        return self._width

    @width.setter
    @FBOAttachment.param_setter
    def width(self, width:int):
        self._width = width
        self._image_size_changed = True

    @property
    def height(self):
        return self._height

    @height.setter
    @FBOAttachment.param_setter
    def height(self, height:int):
        self._height = height
        self._image_size_changed = True

    @property
    def layers(self):
        return len(self._images)

    @layers.setter
    @FBOAttachment.param_setter
    def layers(self, layers:int):
        len_images = len(self._images)
        if layers < len_images:
            del self._images[layers:]

        for i in range(layers - len_images):
            self._images.append(None)

    @property
    def dtype(self):
        return get_dtype(self._internal_format)

    @property
    def internal_format(self):
        return self._internal_format

    def _set_internal_format(self, internal_format):
        self._internal_format = internal_format

        convert_map = \
        {
            (1,3): cv2.COLOR_GRAY2RGB,
            (1,4): cv2.COLOR_GRAY2RGBA,
            (3,1): cv2.COLOR_RGB2GRAY,
            (3,4): cv2.COLOR_RGB2RGBA,
            (4,1): cv2.COLOR_RGBA2GRAY,
            (4,3): cv2.COLOR_RGBA2RGB
        }

        for layer in range(self.layers):
            if self._images[layer] is None:
                continue

            old_channels = self._images[layer].shape[2] if len(self._images[layer].shape) > 2 else 1
            new_channels = get_channels(internal_format)
            if (old_channels, new_channels) in convert_map:
                conversion = convert_map[old_channels, new_channels]
                self._images[layer] = cv2.cvtColor(self._images[layer], conversion)
            elif old_channels == 1:
                if len(self._images[layer].shape) == 2:
                    self._images[layer] = np.expand_dims(self._images[layer], axis=2)
                self._images[layer] = self._images[layer].repeat(new_channels, axis=2)
            elif new_channels > old_channels:
                self._images[layer] = np.append(self._images[layer], np.zeros((self._images[layer].shape[0], self._images[layer].shape[1], new_channels-old_channels), dtype=self._images[layer].dtype), axis=2)
            elif new_channels < old_channels:
                self._images[layer] = self._images[layer][:, :, :new_channels]

            old_np_dtype = self._images[layer].dtype
            new_np_dtype = GLInfo.dtype_map[get_dtype(self._internal_format)]
            if old_np_dtype != new_np_dtype:
                if "int" in str(old_np_dtype) and "float" in str(new_np_dtype):
                    self._images[layer] = (self._images[layer] / 255).astype(new_np_dtype)
                elif "float" in str(old_np_dtype) and "int" in str(new_np_dtype):
                    self._images[layer] = (self._images[layer] * 255).astype(new_np_dtype)
                else:
                    self._images[layer] = self._images[layer].astype(new_np_dtype)

            self._image_layer_changed[layer] = True

    @internal_format.setter
    @FBOAttachment.param_setter
    def internal_format(self, internal_format:GLInfo.internal_formats):
        self._set_internal_format(internal_format)

    @property
    def wrap_r(self):
        return self._wrap_r
    
    @wrap_r.setter
    @FBOAttachment.param_setter
    def wrap_r(self, wrap_type:GLInfo.wrap_types):
        self._wrap_r = wrap_type
        self._wrap_r_changed = True

    @property
    def wrap_s(self):
        return self._wrap_s

    @wrap_s.setter
    @FBOAttachment.param_setter
    def wrap_s(self, wrap_type:GLInfo.wrap_types):
        self._wrap_s = wrap_type
        self._wrap_s_changed = True

    @property
    def wrap_t(self):
        return self._wrap_t

    @wrap_t.setter
    @FBOAttachment.param_setter
    def wrap_t(self, wrap_type:GLInfo.wrap_types):
        self._wrap_t = wrap_type
        self._wrap_t_changed = True

    @property
    def wrap(self):
        return self._wrap_r, self._wrap_s, self._wrap_t

    @wrap.setter
    @FBOAttachment.param_setter
    def wrap(self, wrap_type):
        if wrap_type in GLInfo.wrap_types:
            self.wrap_r = wrap_type
            self.wrap_s = wrap_type
            self.wrap_t = wrap_type
        else:
            self.wrap_r = wrap_type[0]
            self.wrap_s = wrap_type[1]
            self.wrap_t = wrap_type[2]

    @property
    def filter_min(self):
        return self._filter_min

    @filter_min.setter
    @FBOAttachment.param_setter
    def filter_min(self, filter_type:GLInfo.filter_types):
        self._filter_min = filter_type
        self._filter_min_changed = True

    @property
    def filter_mag(self):
        return self._filter_mag

    @filter_mag.setter
    @FBOAttachment.param_setter
    def filter_mag(self, filter_type:GLInfo.filter_types):
        self._filter_mag = filter_type
        self._filter_mag_changed = True

    @property
    def filter_mipmap(self):
        return self._filter_mipmap

    @filter_mipmap.setter
    @FBOAttachment.param_setter
    def filter_mipmap(self, filter_type:GLInfo.filter_types):
        self._filter_mipmap = filter_type
        self._filter_min_changed = True
        self._filter_mag_changed = True

    def _get_filter_min(self):
        if self._filter_mipmap is None:
            return self._filter_min
        else:
            return GLInfo.mipmap_filter_map[(self._filter_min, self._filter_mipmap)]
        
    @property
    def filter(self):
        return self._filter_min, self._filter_mag, self._filter_mipmap

    @filter.setter
    @FBOAttachment.param_setter
    def filter(self, filter_type):
        if filter_type in GLInfo.filter_types:
            self.filter_min = filter_type
            self.filter_mag = filter_type
            self.filter_mipmap = filter_type
        else:
            self.filter_min = filter_type[0]
            self.filter_mag = filter_type[1]
            if len(filter_type) > 2:
                self.filter_mipmap = filter_type[2]

    @property
    def border_color(self):
        return self._border_color

    @border_color.setter
    @FBOAttachment.param_setter
    def border_color(self, color:(glm.vec3, glm.vec4)):
        if isinstance(color, glm.vec3):
            color = glm.vec4(color, 1)

        self._border_color = color
        self._border_color_changed = True

    @property
    def images(self):
        return self._images

    @checktype
    def malloc(self, width:int, height:int, samples:int=None, layers:int=None, internal_format:GLInfo.internal_formats=None):        
        self.width = width
        self.height = height
        
        if layers is not None:
            self.layers = layers

        if internal_format is None:
            internal_format = self.internal_format

        if internal_format is None:
            internal_format = self.__class__._default_internal_format

        self.internal_format = internal_format

    @property
    def is_completed(self):
        return (self._width > 0 and self._height > 0 and self.layers > 0)

    @property
    def samples(self):
        return None
    
    @samples.setter
    def samples(self, samples:int):
        pass
