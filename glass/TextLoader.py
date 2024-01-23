import platform
import os
import freetype
import numpy as np
import glm
import cv2

class MetaFont(type):

    _font_map = {}
    _font_files = []
    _font_names = []
    _font_folders = []

    def _init(cls):
        if MetaFont._font_map:
            return

        for folder in cls.font_folders:
            file_names = os.listdir(folder)
            for file_name in file_names:
                file_path = folder + "/" + file_name
                try:
                    face = freetype.Face(file_path)
                except:
                    continue

                font = cls(face)
                MetaFont._font_map[file_name] = font
                MetaFont._font_map[file_path] = font
                MetaFont._font_map[os.path.basename(file_name).lower()] = font
                name = face.family_name.decode("utf-8")
                MetaFont._font_map[name.lower()] = font
                MetaFont._font_files.append(file_path)
                MetaFont._font_names.append(name)

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

    _text_map = {}

    def load(content:str, font_family:str='Microsoft YaHei', point_size:int=48, color:glm.vec4=glm.vec4(1,1,1,1)):
        if isinstance(color, glm.vec3):
            color = glm.vec4(color, 1)

        key = (content, font_family, point_size, color)
        if key in TextLoader._text_map:
            return TextLoader._text_map[key]

        t = Font[font_family].text(content, point_size)
        image = cv2.merge((color.r * t.bitmap, color.g * t.bitmap, color.b * t.bitmap, color.a * t.bitmap))
        image = cv2.flip(image.astype(np.uint8), 0)
        TextLoader._text_map[key] = image
        return image
