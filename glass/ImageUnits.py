from .GLConfig import GLConfig


class ImageUnits:
    def __init__(self):
        self._unit_image_map = {}
        self._image_unit_map = {}

    def __getitem__(self, unit: int) -> tuple:
        key = (GLConfig.buffered_current_context, unit)
        if key not in self._unit_image_map:
            return None

        return self._unit_image_map[key]

    def __setitem__(self, unit: int, image: tuple):
        context = GLConfig.buffered_current_context

        unit_key = (context, unit)
        if unit_key in self._unit_image_map:
            old_image = self._unit_image_map[unit_key]
            if old_image != image:
                del self._image_unit_map[context, old_image]

        image_key = (context, image)
        if image_key in self._image_unit_map:
            old_unit = self._image_unit_map[image_key]
            if old_unit != unit:
                del self._unit_image_map[context, old_unit]

        self._unit_image_map[unit_key] = image
        self._image_unit_map[image_key] = unit

    def unit_of_image(self, image: tuple) -> int:
        key = (GLConfig.buffered_current_context, image)
        if key not in self._image_unit_map:
            return None

        return self._image_unit_map[key]

    @property
    def available_unit(self):
        context = GLConfig.buffered_current_context

        for i in range(GLConfig.max_image_units):
            key = (context, i)
            if key not in self._unit_image_map:
                return i

            if self._unit_image_map[key] == 0:
                return i

        return None


ImageUnits = ImageUnits()
