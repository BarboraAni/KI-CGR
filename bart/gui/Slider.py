from PyQt5.QtWidgets import *


class Slider(QSlider):
    """Custom QSlider"""

    def __init__(
        self, position, parent, min_value: int, max_value: int, is_odd: bool = False
    ):
        super(QSlider, self).__init__(parent)
        self._is_odd = is_odd

        self.setMinimum(min_value)
        self.setMaximum(max_value)
        self.setOrientation(position)

    def reset(self):
        self.setValue(self.minimum())
