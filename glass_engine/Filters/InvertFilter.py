from .SingleShaderFilter import SingleShaderFilter

class InvertFilter(SingleShaderFilter):

    def __init__(self):
        SingleShaderFilter.__init__(self, "../glsl/Filters/invert_filter.glsl")
