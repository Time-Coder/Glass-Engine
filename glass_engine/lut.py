import numpy as np
import cv2
import re

def generate_standard_LUT(LUT_3D_size:int=64, dest_file_name:str=None):
    block_size = int(np.sqrt(LUT_3D_size))

    R = np.linspace(0, 1, LUT_3D_size)
    G = np.linspace(0, 1, LUT_3D_size)
    B = np.linspace(0, 1, LUT_3D_size)

    R, G = np.meshgrid(R, G)
    if block_size * block_size < LUT_3D_size:
        B = B.reshape((1, LUT_3D_size))
        R = np.tile(R, (1, LUT_3D_size))
        G = np.tile(G, (1, LUT_3D_size))
    else:
        B = B.reshape((block_size, block_size))
        R = np.tile(R, (block_size, block_size))
        G = np.tile(G, (block_size, block_size))

    B = np.repeat(B, LUT_3D_size, axis=0)
    B = np.repeat(B, LUT_3D_size, axis=1)
    
    result = np.stack((R, G, B), axis=-1)
    if dest_file_name is not None:
        out_image = (np.stack((B, G, R), axis=-1)*255).astype(np.uint8)
        cv2.imwrite(dest_file_name, out_image)
        
    return cv2.flip(result.astype(np.float32), 0)

def cube_info(cube_file_name:str):
    in_file = open(cube_file_name)
    content = in_file.read()
    in_file.close()

    lines = content.split("\n")
    data = []
    N = 0
    regx = re.compile(r"^\s*(?P<number1>[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?)\s+(?P<number2>[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?)\s+(?P<number3>[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?)\s*$")
    for line in lines:
        line = line.strip()

        if line.startswith("#"):
            continue

        if line.startswith("LUT_3D_SIZE"):
            N = int(line[len("LUT_3D_SIZE"):].strip())
        else:
            match = re.fullmatch(regx, line)
            if match is not None:
                data.append([float(match["number1"]), float(match["number2"]), float(match["number3"])])

    data = np.array(data)
    return N, data

def apply_cube(cube:(str, tuple), src_image:(str, np.ndarray), dest_file_name:str=None):
    N, data = None, None
    if isinstance(cube, str):
        N, data = cube_info(cube)
    else:
        N, data = cube

    N2 = N * N
    
    if isinstance(src_image, str):
        if dest_file_name is None:
            dest_file_name = src_image

        src_image = cv2.flip(cv2.cvtColor(cv2.imread(src_image, cv2.IMREAD_UNCHANGED), cv2.COLOR_BGR2RGB), 0)

    if "int" in str(src_image.dtype):
        src_image = src_image / 255.0

    src_image *= (N - 1)
    R = src_image[:, :, 0]
    G = src_image[:, :, 1]
    B = src_image[:, :, 2]

    r = {}
    r[0] = np.floor(R).astype(np.uint32)
    r[1] = np.ceil(R).astype(np.uint32)
    R_rear = R - r[0]
    R_rear = np.stack((R_rear, R_rear, R_rear), axis=-1)

    g = {}
    g[0] = np.floor(G).astype(np.uint32)
    g[1] = np.ceil(G).astype(np.uint32)
    G_rear = G - g[0]
    G_rear = np.stack((G_rear, G_rear, G_rear), axis=-1)

    b = {}
    b[0] = np.floor(B).astype(np.uint32)
    b[1] = np.ceil(B).astype(np.uint32)
    B_rear = B - b[0]
    B_rear = np.stack((B_rear, B_rear, B_rear), axis=-1)

    values = {}
    for i in range(2):
        for j in range(2):
            for k in range(2):
                index = r[i] + N*g[j] + N2*b[k]
                values[i, j, k] = data[index, :]

    for j in range(2):
        for k in range(2):
            values[0.5, j, k] = (1-R_rear) * values[0, j, k] + R_rear * values[1, j, k]

    values[0.5, 0.5, 0] = (1 - G_rear) * values[0.5, 0, 0] + G_rear * values[0.5, 1, 0]
    values[0.5, 0.5, 1] = (1 - G_rear) * values[0.5, 0, 1] + G_rear * values[0.5, 1, 1]
    values[0.5, 0.5, 0.5] = (1 - B_rear) * values[0.5, 0.5, 0] + B_rear * values[0.5, 0.5, 1]
    
    result = values[0.5, 0.5, 0.5]
    if dest_file_name is not None:
        out_image = cv2.flip(cv2.cvtColor((np.clip(result, 0, 1)*255).astype(np.uint8), cv2.COLOR_RGB2BGR), 0)
        cv2.imwrite(dest_file_name, out_image)

    return result.astype(np.float32)

def cube_to_LUT(cube_file_name:str, dest_file_name:str=None):
    N, data = cube_info(cube_file_name)
    return apply_cube((N,data), generate_standard_LUT(N), dest_file_name)
