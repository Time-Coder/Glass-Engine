import cv2
import os
from PIL import Image
import OpenEXR, Imath
import numpy as np

from .utils import extname, relative_path
from .GlassConfig import GlassConfig

class ImageLoader:

    __image_map = {}

    @staticmethod
    def load(file_name:str):
        if not os.path.isfile(file_name):
            raise FileNotFoundError("not a valid image file: " + file_name)
        
        file_name = os.path.abspath(file_name).replace("\\", "/")
        if file_name in ImageLoader.__image_map:
            return ImageLoader.__image_map[file_name]
        ext_name = extname(file_name)
        if ext_name == "glsl":
            raise ValueError(f"not supported image format: '{file_name}'")
        
        if GlassConfig.print:
            print(f"loading image: {relative_path(file_name)} ", end="", flush=True)
        image = None
        if ext_name == "exr":
            image = ImageLoader.OpenEXR_load(file_name)
        else:
            image = ImageLoader.PIL_load(file_name)
            if image is None:
                image = ImageLoader.cv2_load(file_name)

        if image is None:
            if GlassConfig.print:
                print("")
            raise ValueError(f"not supported image format: '{file_name}'")
        
        image = cv2.flip(image, 0)

        if image.dtype in [np.float32, np.float64] and image.max() > 1:
            image = ImageLoader.tone_mapping(image)

        ImageLoader.__image_map[file_name] = image

        if GlassConfig.print:
            print("done")

        return image
    
    @staticmethod
    def cv2_load(file_name):
        try:
            image = cv2.imread(file_name, cv2.IMREAD_UNCHANGED)
            if image is None:
                return None
            
            channels = image.shape[2] if len(image.shape) > 2 else 1
            if channels == 3:
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            elif channels == 4:
                image = cv2.cvtColor(image, cv2.COLOR_BGRA2RGBA)

            return image
        except:
            return None

    @staticmethod
    def PIL_load(file_name):
        try:
            pil_image = Image.open(file_name)
            dest_mode = "RGBA"
            if pil_image.mode == "RGB":
                dest_mode = "RGB"
            elif pil_image.mode == "RGBA":
                dest_mode = "RGBA"
            elif pil_image.mode == "CMYK":
                dest_mode = "RGBA"
            elif pil_image.mode == "P":
                dest_mode = "RGBA"
            elif pil_image.mode == "L":
                dest_mode = "L"
            elif pil_image.mode == "1":
                dest_mode = "L"

            if dest_mode != pil_image.mode:
                pil_image = pil_image.convert(dest_mode)

            return np.array(pil_image)
        except:
            return None
    
    @staticmethod
    def OpenEXR_load(file_name):
        try:
            pt = Imath.PixelType(Imath.PixelType.FLOAT)
            img_exr = OpenEXR.InputFile(file_name)

            dw = img_exr.header()['dataWindow']
            shape = (dw.max.y - dw.min.y + 1, dw.max.x - dw.min.x + 1)

            r_bytes, g_bytes, b_bytes = img_exr.channels('RGB', pt)
            r = np.frombuffer(r_bytes, dtype=np.float32).reshape(shape)
            g = np.frombuffer(g_bytes, dtype=np.float32).reshape(shape)
            b = np.frombuffer(b_bytes, dtype=np.float32).reshape(shape)
            return cv2.merge((r, g, b))
        except:
            return None
    
    @staticmethod
    def tone_mapping(image):
        gray = np.copy(image)

        channels = image.shape[2] if len(image.shape) > 2 else 1
        if channels == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        elif channels == 4:
            gray = cv2.cvtColor(image, cv2.COLOR_RGBA2GRAY)

        gray[gray>1] = 1 + np.tanh(gray[gray>1]-1)

        rows = gray.shape[0]
        cols = gray.shape[1]

        resize_rows = 64
        resize_cols = int(resize_rows / rows * cols)

        blur_rows = 3
        blur_radius = int(blur_rows / rows * cols)
        
        temp_gray = cv2.copyMakeBorder(gray, rows, rows, cols, cols, borderType=cv2.BORDER_WRAP)
        temp_gray = cv2.resize(temp_gray, (3*resize_cols, 3*resize_rows), interpolation=cv2.INTER_AREA)
        temp_gray = cv2.GaussianBlur(temp_gray, (2*blur_radius+1, 2*blur_radius+1), 0)
        temp_gray = cv2.resize(temp_gray, (3*cols, 3*rows))

        L = temp_gray[rows:-rows, cols:-cols]
        L = np.sqrt(L)

        if channels == 3:
            L = cv2.merge((L, L, L))
        elif channels == 4:
            L = cv2.merge((L, L, L, L))

        image = image/L / (1 + image/L)
        image /= image.max()
        image = np.sin(np.pi/2*image)

        return image