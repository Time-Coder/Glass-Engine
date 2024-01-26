import platform
import os
import freetype
import numpy as np
import glm
import cv2

from .sampler2D import sampler2D

def edtaa(a:np.ndarray):
    gx = cv2.Sobel(a, cv2.CV_64F, 1, 0, ksize=3)
    gy = cv2.Sobel(a, cv2.CV_64F, 0, 1, ksize=3)
    df = 1000000 * np.ones(a.shape)

    condition1 = ((gx == 0) | (gy == 0))
    condition2 = ((gx != 0) & (gy != 0))
    # df[condition1] = 0.5 - a[condition1]

    glength = np.sqrt(gx**2 + gy**2)
    condition3 = condition2 & (glength > 0)
    divisor = glength[condition3]
    gx[condition3] /= divisor
    gy[condition3] /= divisor

    gx[condition2] = np.abs(gx[condition2])
    gy[condition2] = np.abs(gy[condition2])
    condition4 = (condition2 & (gx < gy))
    gx[condition4], gy[condition4] = gy[condition4], gx[condition4]
    a1 = np.zeros(a.shape)
    a1[condition2] = 0.5*gy[condition2]/gx[condition2]

    condition5 = condition2 & (a < a1)
    condition6 = condition2 & (a1 <= a) & (a < (1.0-a1))
    condition7 = condition2 & (1-a1 < a) & (a <= 1)
    gx5 = gx[condition5]
    gy5 = gy[condition5]
    a5 = a[condition5]

    gx6 = gx[condition6]
    a6 = a[condition6]

    gx7 = gx[condition7]
    gy7 = gy[condition7]
    a7 = a[condition7]

    df[condition5] = 0.5*(gx5 + gy5) - np.sqrt(2*gx5*gy5*a5)
    df[condition6] = (0.5 - a6) * gx6
    df[condition7] = -0.5*(gx7 + gy7) + np.sqrt(2*gx7*gy7*(1-a7))
    return df
    
def octSSEDT(a, df):
    for i in range(a.shape[0]):
        for j in range(a.shape[1]):
            if df[i,j] > 100000:
                df_left = df[i,j-1] if j-1 >= 0 else 1000000
                df_left_top = df[i-1,j-1] if i-1 >= 0 and j-1 >= 0 else 1000000
                df_top = df[i-1,j] if i-1 >= 0 else 1000000
                df_right_top = df[i-1,j+1] if i-1 >= 0 and j+1 < a.shape[1] else 1000000

class MetaFont(type):

    _font_map = {}
    _font_files = []
    _font_names = []
    _font_folders = []

    def _init(cls):
        if MetaFont._font_map:
            return

        for folder in cls.font_folders:
            for root, dirs, files in os.walk(folder):
                for file_name in files:
                    file_path = root + "/" + file_name
                    try:
                        face = freetype.Face(file_path)
                    except:
                        continue

                    font = cls(face)
                    MetaFont._font_map[file_name] = font
                    MetaFont._font_map[file_path] = font
                    MetaFont._font_map[os.path.basename(file_name).lower()] = font
                    MetaFont._font_files.append(file_path)

                    try:
                        name = face.family_name.decode("utf-8")
                        MetaFont._font_map[name.lower()] = font
                        MetaFont._font_names.append(name)
                    except:
                        pass

    def __getitem__(cls, font_name:str):
        cls._init()
            
        if font_name in MetaFont._font_map:
            return MetaFont._font_map[font_name]
        elif font_name.lower() in MetaFont._font_map:
            return MetaFont._font_map[font_name.lower()]
        else:
            raise KeyError(font_name)

    @property
    def font_names(cls):
        cls._init()
        return MetaFont._font_names

    @property
    def font_files(cls):
        cls._init()
        return MetaFont._font_files

    @property
    def font_folders(cls):
        if not MetaFont._font_folders:
            if platform.system() == "Windows":
                MetaFont._font_folders = ["C:/Windows/fonts"]
            elif platform.system() == "Linux":
                MetaFont._font_folders = ["/usr/share/fonts"]
            elif platform.system() == "Darwin":
                MetaFont._font_folders = ["/Library/Fonts", "/System/Library/Fonts"]

        return MetaFont._font_folders


class Font(metaclass=MetaFont):
    
    class Char:

        def __init__(self, content:str):
            self.content = content
            self.bearing = (0,0)
            self.advance = (0,0)
            self.bitmap = None
            self.sdf = None

    class Text:

        def __init__(self, content:str):
            self.content = content
            self.chars = []
            self.bitmap = None

    _char_map = {}
    _text_map = {}

    def __init__(self, face):
        self.face = face
        
    def char(self, content:str, point_size:int=48):
        if len(content) != 1:
            raise ValueError('length of content should be 1')
        
        key = (content, point_size)
        if key in Font._char_map:
            return Font._char_map[key]
        
        self.face.set_pixel_sizes(0, point_size)
        self.face.load_char(content)
        char = Font.Char(content)
        char.bearing = (self.face.glyph.bitmap_left, self.face.glyph.bitmap_top)
        char.advance = (self.face.glyph.advance.x//64, self.face.glyph.advance.y//64)
        char.bitmap = np.array(self.face.glyph.bitmap.buffer, dtype=np.uint8).reshape((self.face.glyph.bitmap.rows, self.face.glyph.bitmap.width))
        char.sdf = edtaa(char.bitmap/255)
        Font._char_map[key] = char

        return char
    
    def text(self, content:str, point_size:int=48):
        key = (content, point_size)
        if key in Font._text_map:
            return Font._text_map[key]
        
        text = Font.Text(content)
        width = 0
        max_up_height = 0
        max_down_height = 0
        for ch in content:
            char = self.char(ch, point_size)
            text.chars.append(char)
            width += char.advance[0]
            height = char.bitmap.shape[0]
            up_height = char.bearing[1]
            down_height = height - up_height

            if up_height > max_up_height:
                max_up_height = up_height

            if down_height > max_down_height:
                max_down_height = down_height

        text.bitmap = np.zeros((max_up_height+max_down_height, width), dtype=np.uint8)
        left = 0
        for char in text.chars:
            start_y = max_up_height - char.bearing[1]
            stop_y = start_y + char.bitmap.shape[0]
            start_x = left+char.bearing[0]
            stop_x = start_x+char.bitmap.shape[1]
            text.bitmap[start_y:stop_y, start_x:stop_x] = char.bitmap
            left += char.advance[0]

        Font._text_map[key] = text

        return text

class TextLoader:

    _image_map = {}
    _sampler_map = {}

    @staticmethod
    def load(content:str, font_family:str=None, point_size:int=48, color:glm.vec4=glm.vec4(1,1,1,1)):
        if font_family is None:
            if platform.system() == "Windows":
                font_family = "Microsoft YaHei"
            else:
                font_family = "DejaVu Sans Mono"

        if isinstance(color, glm.vec3):
            color = glm.vec4(color, 1)

        key = (content, font_family, point_size, color)
        if key in TextLoader._image_map:
            return TextLoader._image_map[key]

        t = Font[font_family].text(content, point_size)
        image = cv2.merge((255 * color.r * np.ones(t.bitmap.shape),
                           255 * color.g * np.ones(t.bitmap.shape),
                           255 * color.b * np.ones(t.bitmap.shape),
                           color.a * t.bitmap))
        image = cv2.flip(image.astype(np.uint8), 0)
        TextLoader._image_map[key] = image
        return image
    
    @staticmethod
    def load_sampler(content:str, font_family:str=None, point_size:int=48, color:glm.vec4=glm.vec4(1,1,1,1)):
        if font_family is None:
            if platform.system() == "Windows":
                font_family = "Microsoft YaHei"
            else:
                font_family = "DejaVu Sans Mono"
                
        if isinstance(color, glm.vec3):
            color = glm.vec4(color, 1)

        key = (content, font_family, point_size, color)
        if key in TextLoader._sampler_map:
            return TextLoader._sampler_map[key]
        
        sampler = sampler2D(TextLoader.load(content, font_family, point_size, color))
        TextLoader._sampler_map[key] = sampler
        return sampler
