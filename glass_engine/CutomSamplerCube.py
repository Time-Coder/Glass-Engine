from glass import sampler2D

class CustomSamplerCube:
    def __init__(self):
        self.right = None # 0
        self.left = None # 1
        self.bottom = None # 2
        self.top = None # 3
        self.front = None # 4
        self.back = None # 5

    def __getitem__(self, index:int):
        if index == 0: return self.right
        elif index == 1: return self.left
        elif index == 2: return self.bottom
        elif index == 3: return self.top
        elif index == 4: return self.front
        elif index == 5: return self.back

    def __setitem__(self, index:int, value:sampler2D):
        if index == 0: self.right = value
        elif index == 1: self.left = value
        elif index == 2: self.bottom = value
        elif index == 3: self.top = value
        elif index == 4: self.front = value
        elif index == 5: self.back = value