from .SingleShaderFilter import SingleShaderFilter

class SlitStretchFilter(SingleShaderFilter):
    def __init__(self):
        SingleShaderFilter.__init__(self, "../glsl/Filters/slit_stretch_filter.glsl")