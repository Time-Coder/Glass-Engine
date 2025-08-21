import itertools
from typing import Dict, List


_attr_index_map = {
    'x': 0,
    'y': 1,
    'z': 2,
    'w': 3,
    'r': 0,
    'g': 1,
    'b': 2,
    'a': 3,
    's': 0,
    't': 1,
    'p': 2,
    'q': 3
}

def generate_swizzle(characters, min_length=1, max_length=4):
    result:Dict[str, List[int]] = {}
    
    for length in range(min_length, max_length + 1):
        for combo in itertools.product(characters, repeat=length):
            swizzle = ''.join(combo)
            result[swizzle] = []
    
    return result
