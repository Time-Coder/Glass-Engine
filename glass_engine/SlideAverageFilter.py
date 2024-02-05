class SlideAverageFilter:

    def __init__(self, window_width: int = 10) -> None:
        self._current_sum = 0
        self._window_width = window_width
        self._data_list = []

    def __call__(self, new_value: (float, int)) -> float:
        if len(self._data_list) >= self._window_width:
            old_value = self._data_list.pop(0)
            self._current_sum -= old_value

        self._data_list.append(new_value)
        self._current_sum += new_value

        return self._current_sum / len(self._data_list)

    @property
    def window_width(self) -> int:
        return self._window_width

    @window_width.setter
    def window_width(self, window_width: int) -> None:
        self._window_width = window_width
