from .SingleShaderFilter import SingleShaderFilter

class StarFieldFilter(SingleShaderFilter):
    def __init__(self):
        SingleShaderFilter.__init__(self, "../glsl/Filters/star_field_filter.glsl")