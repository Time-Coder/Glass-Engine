from .SingleShaderFilter import SingleShaderFilter

class WaterWaveFilter(SingleShaderFilter):
    def __init__(self):
        SingleShaderFilter.__init__(self, "../glsl/Filters/water_wave_filter.glsl")