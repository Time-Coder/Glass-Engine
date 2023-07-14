from .SingleShaderFilter import SingleShaderFilter
from glass.utils import checktype

from OpenGL import GL
import numpy as np

class KernelFilter(SingleShaderFilter):

    class Kernel:
        def __init__(self, kernel:np.ndarray):
            self.rows = kernel.shape[0]
            self.cols = kernel.shape[1]
            self.data = list(kernel.flatten())
            self._kernel = kernel

        @property
        def kernel(self):
            return self._kernel
        
        @kernel.setter
        def kernel(self, kernel:np.ndarray):
            self.rows = kernel.shape[0]
            self.cols = kernel.shape[1]
            self.data = list(kernel.flatten())
            self._kernel = kernel

    @checktype
    def __init__(self, kernel:np.ndarray):
        SingleShaderFilter.__init__(self, "../glsl/Filters/kernel_filter.glsl")
        self._kernel = KernelFilter.Kernel(kernel)
        self["Kernel"].bind(self._kernel)

    @property
    def kernel(self)->np.ndarray:
        return self._kernel.kernel
    
    @kernel.setter
    def kernel(self, kernel:np.ndarray):
        self._kernel.kernel = kernel
    